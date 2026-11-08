from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PasswordResetCode

User = get_user_model()


class UserFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="paola",
            email="paola@example.com",
            password="senha123"
        )

    # Cadastro de usuário.
    def test_register_user(self):
        response = self.client.post(reverse("cadastro"), {
            "username": "novo_user",
            "email": "novo@example.com",
            "nome_completo": "Usuário Teste",
            "telefone": "12345",
            "password1": "SenhaForte123",
            "password2": "SenhaForte123",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="novo_user").exists())

    # Login com credenciais válidas.
    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "paola@example.com",
            "password": "senha123"
        })

        self.assertEqual(response.status_code, 302)

    # Login com senha incorreta.
    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "username": "paola@example.com",
            "password": "senha_errada"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, entre com um email  e senha corretos")

    # Encerramento da sessão.
    def test_logout(self):
        self.client.login(username="paola@example.com", password="senha123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200) 
        
    # Atualização dos dados da conta.
    def test_update_profile(self):
        self.client.login(username="paola@example.com", password="senha123")

        response = self.client.post(reverse("alterar_dados"), {
            "username": "paola_new",
            "email": "novoemail@example.com",
            "nome_completo": "Novo Nome",
            "telefone": "99999"
        })

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "paola_new")
        self.assertEqual(self.user.email, "novoemail@example.com")

    # Alteração de senha com sessão ativa.
    def test_change_password(self):
        self.client.login(username="paola@example.com", password="senha123")

        response = self.client.post(reverse("alterar_senha"), {
            "modo": "senha",
            "campo_verificacao": "senha123",
            "nova_senha": "NovaSenha123",
            "confirmar_senha": "NovaSenha123"
        })

        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NovaSenha123"))