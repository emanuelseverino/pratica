from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('core.urls')),
                  path('perfil/', include('perfil.urls')),
                  path('payment/', include('payment.urls')),
                  path('accounts/', include("django.contrib.auth.urls")),
                  path('login/', views.obtain_auth_token),
                  path('login/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('login/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
