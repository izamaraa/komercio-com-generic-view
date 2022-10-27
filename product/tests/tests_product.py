from rest_framework.test import APITestCase
from rest_framework.views import status
from product.models import Product
from account.models import Account
from rest_framework.authtoken.models import Token
import ipdb


class TestViewProduct(APITestCase):
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

        produto = {"description": "teste1000", "price": 100.99, "quantity": 5}
        self.produto = Product.objects.create(**produto, seller_id=self.seller.id)

    def test_only_seller_can_create_product(self):
        """Somente vendedor pode criar produto."""
        tokenComum = Token.objects.create(user=self.comum)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)
        produto1 = {"description": "teste1000", "price": 100.99, "quantity": 5}
        response = self.client.post("/api/products/", data=produto1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_the_seller_of_the_product_can_update_it(self):
        """Somente o vendedor do produto pode atualizá-lo."""
        tokenComum = Token.objects.create(user=self.comum)
        data = {"description": "tsunada"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)
        response = self.client.patch(f"/api/accounts/{self.seller.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anyone_can_list_and_filter_products(self):
        """Qualquer um pode listar e filtrar produtos."""
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_specific_return_for_listing(self):
        """Retorno específico para listagem"""
        response = self.client.get(f"/api/products/{self.produto.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_keys(self):
        """Chaves erradas"""
        tokenSeller = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenSeller.key)
        produto = {"descron": "teste1000", "pre": 100.99, "quant": 5}
        response = self.client.post("/api/products/", data=produto)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_negative_quantity(self):
        """Criar produto com quantidade negativa"""
        tokenSeller = Token.objects.create(user=self.seller)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenSeller.key)
        produto1 = {"description": "teste1000", "price": 100.99, "quantity": -5}
        response = self.client.post(f"/api/products/", data=produto1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
