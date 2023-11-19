from django.contrib import admin

from payment.models import Payment, Texto, Cobranca

admin.site.register(Payment)
admin.site.register(Cobranca)
admin.site.register(Texto)
