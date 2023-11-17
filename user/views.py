from django.http import HttpResponse
from django.views import View

from user.models import User


class UpdatePlain(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        user.update_plain()
        user.save()
        return HttpResponse(status=200)
