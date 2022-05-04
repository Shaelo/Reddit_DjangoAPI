from django.shortcuts import render

from django.contrib.auth import get_user_model
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from applications.user.serializers import *

User = get_user_model()


class AccountView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            msg = 'Вы успешно создали аккаунт! Вам отправлено письмо с активацией'
            return Response(msg, status=201)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def get(self, requests, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Вы успешно активировали аккаунт!', status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('Активационный код не найден', status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            Token.objects.filter(user=user).delete()
            return Response('Вы успешно вышли из аккаунта')
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class RecoveryPasswordView(APIView):


    def post(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.new_password()
            return Response("Ваш новый пароль отправлен вам на почту")
