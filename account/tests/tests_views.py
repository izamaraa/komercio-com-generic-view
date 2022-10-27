from rest_framework.test import APITestCase
from rest_framework.views import status
from account.models import Account
from rest_framework.authtoken.models import Token
import ipdb

# Create your tests here.
class TestViewAccount(APITestCase):
    def setUp(self) -> None:
        pessoaSeller = {
            "username": "testeSeller",
            "password": "1234",
            "first_name": "Vamos testar",
            "last_name": "biruleibe",
            "is_seller": True,
        }
        self.seller = Account.objects.create_user(**pessoaSeller)

        pessoaAdm = {
            "username": "testeAdm",
            "password": "1234",
            "first_name": "Vamos testar",
            "last_name": "biruleibe",
            "is_seller": False,
        }
        self.admin = Account.objects.create_superuser(**pessoaAdm)

        pessoaComum = {
            "username": "testeComum",
            "password": "1234",
            "first_name": "Vamos testar",
            "last_name": "biruleibe",
            "is_seller": False,
        }
        self.comum = Account.objects.create_user(**pessoaComum)

    def test_seller_account_creation(self):
        """Criação de conta de vendedor"""
        pessoaSeller = {
            "username": "seller",
            "password": "1234",
            "first_name": "Vamos testar",
            "last_name": "biruleibe",
            "is_seller": True,
        }
        response = self.client.post("/api/accounts/", data=pessoaSeller)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_a_non_seller_account(self):
        """Criação de conta de não vendedor"""
        pessoaComum = {
            "username": "Comum",
            "password": "1234",
            "first_name": "Vamos testar",
            "last_name": "biruleibe",
            "is_seller": False,
        }
        response = self.client.post("/api/accounts/", data=pessoaComum)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wrong_keys_in_both_cases(self):
        """Chaves erradas em ambos os casos"""
        pessoaComum = {
            "usrname": "Comum2",
            "pasord": "1234",
            "fist_name": "Vamos testar",
            "lat_name": "biruleibe",
            "is_seler": False,
        }
        response = self.client.post("/api/accounts/", data=pessoaComum)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seller_login_returns_token(self):
        """Login vendedor retorna token"""
        # ipdb.set_trace()
        tokenSeller = Token.objects.create(user=self.seller)

        data = {"username": self.seller.username, "password": "1234"}

        response = self.client.post("/api/login/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": tokenSeller.key})

    def test_login_not_seller_returns_token(self):
        """Login não vendedor retorna token"""
        tokenComum = Token.objects.create(user=self.comum)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)

        data = {"username": self.comum.username, "password": "1234"}

        response = self.client.post("/api/login/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": tokenComum.key})

    def test_only_account_owner_can_update_data(self):
        """Somente dono da conta pode atualizar dados"""
        tokenComum = Token.objects.create(user=self.comum)
        # ipdb.set_trace()
        data = {"last_name": "tsunada"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)
        response = self.client.patch(f"/api/accounts/{self.seller.id}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_admin_can_disable_it(self):
        """Somente admininstrador pode desativá-la"""
        tokenAdmin = Token.objects.create(user=self.admin)
        # ipdb.set_trace()
        data = {"is_active": False}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenAdmin.key)
        response = self.client.patch(
            f"/api/accounts/{self.comum.id}/management/", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_admin_can_reactivate_accounts(self):
        """Somente administrador pode reativar contas."""
        tokenAdmin = Token.objects.create(user=self.admin)

        data = {"is_active": True}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenAdmin.key)
        response = self.client.patch(
            f"/api/accounts/{self.comum.id}/management/", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anyone_can_list_users(self):
        """Qualquer um pode listar usuários."""
        response = self.client.get("/api/accounts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
