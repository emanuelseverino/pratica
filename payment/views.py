import requests
import json
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from payment.models import Payment, Cobranca, Texto


def formate_date(date):
    date_format = datetime.fromisoformat(date.replace('Z', '+00:00'))
    return date_format.strftime('%H:%M:%S - %d/%m/%Y')


class PayView(LoginRequiredMixin, View):
    login_url = '/accounts/login'

    def get(self, request, *args, **kwargs):

        payments = Payment.objects.filter(user=self.request.user)
        for payment in payments:
            if payment.status == 'pending':
                payment = Payment.objects.get(id=payment.pk)
                if payment:
                    context = {
                        'payment': payment,
                        'user': self.request.user,
                    }
                    payment.save()
                    return render(request, 'payment/sucess.html', context=context)
        return render(request, 'payment/pay.html')

    def post(self, request, *args, **kwargs):
        data = {
            "transaction_amount": 27.9,
            "description": "Renovação de Plano - EstudeAPI",
            "payment_method_id": "pix",
            "payer": {
                "email": self.request.user.email,
                "first_name": self.request.POST.get('first_name'),
                "last_name": self.request.POST.get('last_name'),
                "identification": {
                    "type": "CPF",
                    "number": self.request.POST.get('cpf').replace('.', '').replace('-', '')
                },
                "address": {
                    "zip_code": "28300000",
                    "street_name": "Rua Maria Otalia Boechat",
                    "street_number": "177",
                    "neighborhood": "Aeroporto",
                    "city": "Itaperuna",
                    "federal_unit": "RJ"
                }
            }
        }
        headers = {
            'Authorization': 'Bearer APP_USR-7893702088637531-012618-cd9f06ef47c005273a3cd983a2ce2902-119438936'
            # 'Authorization': 'Bearer APP_USR-1114375702126269-120713-a25141d610bf54c4370c3eacd1e76fce-1005708872'
            # 'Authorization': 'Bearer APP_USR-660711714671368-111714-aebe3a78fc8927e8cd0b79cb46bd5b65-119438936',
            # 'x-idempotency-key': '123',
        }

        response = requests.post('https://api.mercadopago.com/v1/payments', json=data, headers=headers)

        data = json.loads(response.content)

        print(data)

        if response.status_code == 201:
            cob = Payment.objects.create(
                user=self.request.user,
                payment_id=data['id'],
                status=data['status'],
                status_detail=data['status_detail'],
                create_in=formate_date(data['date_created']),
                description=data['description'],
                qr_code=data['point_of_interaction']['transaction_data']['qr_code'],
                qr_code64=data['point_of_interaction']['transaction_data']['qr_code_base64'],
                url=data['point_of_interaction']['transaction_data']['ticket_url'])
            if cob:
                cob.save()
                payment = Payment.objects.get(id=cob.pk)
                if payment:
                    context = {
                        'payment': payment,
                        'user': self.request.user,
                        'cpf': self.request.POST.get('cpf').replace('.', '').replace('-', '')
                    }
                    payment.save()
                    return render(request, 'payment/sucess.html', context=context)

            return render(request, 'payment/erro.html', )
        else:
            return render(request, 'payment/erro.html', )


class PaymentsView(LoginRequiredMixin, ListView):
    template_name = 'payment/payments.html'
    context_object_name = "payments"
    queryset = Payment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


def readHook(url):
    headers = {
        'Authorization': 'Bearer APP_USR-7893702088637531-012618-cd9f06ef47c005273a3cd983a2ce2902-119438936'
        # 'Authorization': 'Bearer APP_USR-1114375702126269-120713-a25141d610bf54c4370c3eacd1e76fce-1005708872'
        # 'Authorization': 'Bearer APP_USR-660711714671368-111714-aebe3a78fc8927e8cd0b79cb46bd5b65-119438936',
        # 'x-idempotency-key': '123'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            body = response.json()
            payment = Payment.objects.get(payment_id=body['collection']['id'])
            payment.status = body['collection']['status']
            payment.status_detail = body['collection']['status_detail']
            if body['collection']['last_modified']:
                payment.update_in = formate_date(body['collection']['last_modified'])
            if body['collection']['date_approved']:
                payment.payment_in = formate_date(body['collection']['date_approved'])
            if body['collection']['status'] == 'approved':
                payment.user.update_plain()

            payment.save()
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return True


@method_decorator(csrf_exempt, name='dispatch')
class WebHook(View):

    def post(self, request, *args, **kwargs):
        Texto.objects.create(texto='DIR: %s' % str(self.request.body))
        # body = json.loads(self.request.body)
        # if body['resource']:
        #     readHook(body['resource'])
        return HttpResponse(status=200)

