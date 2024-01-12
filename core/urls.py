from django.urls import path
from core.views.accounts import AccountViewset, SignIn
from core.views.profile import ProfileViewset
from core.views.services import ServiceViewset
from core.views.notification import NotificationViewset
from core.views.reset_password import PasswordResetViewset
from core.views.transactions import PaymentViewset
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('accounts/create/', AccountViewset.as_view({'post': 'create'})),
    path('accounts/verify-account/', AccountViewset.as_view({'post': 'verify_email'})),
    path('accounts/resend-verification-pin/', AccountViewset.as_view({'post': 'send_verification_email'})),
    #profile
    path('profile/', ProfileViewset.as_view({'get': 'list'})),
    path('profile/create/', ProfileViewset.as_view({'post': 'create'})),
    path('profile/update/', ProfileViewset.as_view({'post': 'update'})),
    path('profile/retrieve/', ProfileViewset.as_view({'get': 'retrieve'})),
    #login
    path('login/', SignIn.as_view({'post':'post'}), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #password reset
    path('accounts/password-reset/', PasswordResetViewset.as_view({'post': 'password_reset_request'})),
    path('accounts/password-reset-confirm/', PasswordResetViewset.as_view({'post': 'password_reset_confirm'})),
    #service
    path('service/all/', ServiceViewset.as_view({'get': 'list_service'})),
    path('service/create/', ServiceViewset.as_view({'post': 'create_service'})),
    path('service/update/<uuid:id>/', ServiceViewset.as_view({'post': 'update_service'})),
    path('service/delete/<uuid:id>/', ServiceViewset.as_view({'delete': 'delete_service'})),
    path('service/retrieve/<uuid:id>/', ServiceViewset.as_view({'get': 'retrieve'})),
    path('service/book/', PaymentViewset.as_view({'post': 'initialize_transaction'})),
    path('service/verify-payment/', PaymentViewset.as_view({'post': 'verify_transaction'})),
    path('service/booked-user-service/<uuid:id>/', ServiceViewset.as_view({'get': 'list_booked_service_by_customer'})),
    path('service/service-feedback/<uuid:id>/', ServiceViewset.as_view({'post': 'service_feedback'})),
    path('service/provider-services/', ServiceViewset.as_view({'get':'get_service_provider_services'})),
    ##Notification
    path('notification/all/', NotificationViewset.as_view({'get': 'list'})),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)