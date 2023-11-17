from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import IndexView, RegisterView
from payment.views import PayView, PaymentsView

urlpatterns = [
    path('', PayView.as_view(), name='payment'),
    path('payments/', PaymentsView.as_view(), name='payments'),
]
