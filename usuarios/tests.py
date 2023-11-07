from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse  # Importe reverse daqui

class LogarViewTest(TestCase):
    def setUp(self):
        # Crie um usuário de teste válido
        self.user_valid = User.objects.create_user(username='admin', password='123')

    def test_logar_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logar_post_usuario_invalido(self):
        # Envie uma solicitação POST com credenciais inválidas
        response = self.client.post(reverse('login'), {'nome': 'usuario_inexistente', 'senha': 'senha_errada'})
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Usuário ou senha inválidos')
