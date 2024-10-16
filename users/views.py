from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (CreateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import (SignupSerializer,)
from users.models import EmailConformationToken
from users.utils import send_confirmation_email


class SignupAPIView(CreateAPIView):

    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)


class UserInformationAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        email = user.email
        is_email_confirmed = user.is_email_confirmed
        payload = {'email': email, 'is_email_confirmed': is_email_confirmed}
        return Response(payload, status=status.HTTP_200_OK)


class SendEmailConfiramtionTokenAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        user = request.user
        token = EmailConformationToken.objects.create(user=user)
        send_confirmation_email(email=user.email, token_id=token.id, user_id=user.id)
        return Response(data=None, status=status.HTTP_201_CREATED)


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConformationToken.objects.get(id=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        data = {'is_email_confirmed': True}
        return render(request, 'confirm-email-view.html', context=data)

    except EmailConformationToken.DoesNotExist:
        data = {'is_email_confirmed': False}
        return render(request, 'confirm-email-view.html', context=data)
