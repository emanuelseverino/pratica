from django.db import models

from user.models import User

STATUS_CHOICES = [
    ("pending", "Pendente"),
    ("approved", "Aprovado"),
    ("cancelled", "Cancelado"),
]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    status_detail = models.CharField(max_length=30, null=True, blank=True)
    create_in = models.CharField(max_length=30, null=True, blank=True)
    update_in = models.CharField(max_length=30, null=True, blank=True)
    payment_in = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=30, null=True, blank=True)
    qr_code = models.CharField(max_length=10000, null=True, blank=True)
    qr_code64 = models.CharField(max_length=6000, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return '%s - %s | %s' % (self.user, self.payment_id, self.status)


class Cobranca(models.Model):
    id_web = models.CharField(max_length=50, null=True, blank=True)
    mensagem = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.id_web, self.mensagem)
