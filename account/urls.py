from django.urls import path
from .views import ListCreateAccountView, PatchAccountManagementView, PatchAccountView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # registar e listar usuario
    path("accounts/", ListCreateAccountView.as_view()),
    # logar usuario
    path("login/", obtain_auth_token),
    # listar usuarios do mais novo ao mais antigo
    path("accounts/newest/<num>/", ListCreateAccountView.as_view()),
    # atualizar dados de usuario
    path("accounts/<num>/", PatchAccountView.as_view()),
    # ativar/desativar conta (trocar is_active para False/True).
    path("accounts/<num>/management/", PatchAccountManagementView.as_view()),
]
