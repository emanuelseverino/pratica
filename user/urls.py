from django.urls import path, include
from rest_framework import routers

from user.api.viewsets import ChangePasswordView

router = routers.DefaultRouter()
# router.register(r'mudar-senha', ChangePasswordView)

urlpatterns = [
    path('', include(router.urls)),
]
