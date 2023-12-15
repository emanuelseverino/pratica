from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from payment.views import WebHook
from user.api.viewsets import CustomAuthToken, RegisterViewSet


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('cadastro/', RegisterViewSet.as_view(), name='auth_register'),
                  path('', include('core.urls')),
                  path('perfil/', include('perfil.urls')),
                  path('usuarios/', include('user.urls')),
                  path('payment/', include('payment.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('webhook/', WebHook.as_view(), name='webhook', ),
                  path('login/', CustomAuthToken.as_view()),
                  path('jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
