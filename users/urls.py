from django.urls import path
from users.views import (SignupAPIView,
                         SendEmailConfiramtionTokenAPIView,
                         UserInformationAPIView,
                         confirm_email_view)
from rest_framework.authtoken.views import (obtain_auth_token,)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup_api_view'),
    path('login/', obtain_auth_token, name='login_api_view'),
    path('me/', UserInformationAPIView.as_view(), name='me_api_view'),
    path('send-confirmation-email/', SendEmailConfiramtionTokenAPIView.as_view(),
         name='send_email_confirmation_api_view'),
    path('confirm-email/', confirm_email_view, name='confirm_email_view')

]
