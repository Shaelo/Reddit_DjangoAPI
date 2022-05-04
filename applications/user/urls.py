from django.urls import path
from applications.user.views import *

urlpatterns = [
    path('all/', AccountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<uuid:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('recovery/password/', RecoveryPasswordView.as_view()),
]