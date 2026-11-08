from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CadastroForm(UserCreationForm):
    
    nome_completo = forms.CharField(max_length=150, required=True)
    telefone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "nome_completo",
            "telefone",
            "password1",
            "password2",
        ]

    # Evita cadastrar o mesmo e-mail em mais de uma conta.
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    # Copia os campos extras antes de salvar o usuário.
    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.nome_completo = self.cleaned_data["nome_completo"]
        user.telefone = self.cleaned_data["telefone"]

        if commit:
            user.save()

        return user
    
# Formulário de edição dos dados da conta.
class UpdateUserForm(forms.ModelForm):
    # Mantém o campo username com as regras usadas pela aplicação.
    username = forms.CharField(
        required=True,
        label="Nome de Usuário",
        max_length=150,
        strip=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    
    class Meta:
        model = User
        fields = ['username', 'nome_completo', 'telefone', 'email']

        # Oculta os textos de ajuda padrão nos campos.
        help_texts = {
            'username': '',
            'email': '',
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        user_id = self.instance.id  # Usuário atual

        if not email or email.strip() == "":
            raise forms.ValidationError("Campo obrigatório vazio.")

        # O e-mail pode continuar igual ao da conta atual.
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username or username.strip() == "":
            raise forms.ValidationError("Campo obrigatório vazio.")

        return username
    
# Campos usados nos dois fluxos de alteração de senha.

class ChangePasswordForm(forms.Form):
    modo = forms.CharField(widget=forms.HiddenInput(), initial="password")  
    # Indica se a validação será feita pela senha atual ou por código.

    campo_verificacao = forms.CharField(
        required=False,
        label="Senha Atual",
        widget=forms.PasswordInput(),
    )

    nova_senha = forms.CharField(
        required=True,
        label="Nova Senha",
        widget=forms.PasswordInput(),
    )

    confirmar_senha = forms.CharField(
        required=True,
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned = super().clean()

        nova = cleaned.get("nova_senha")
        confirmar = cleaned.get("confirmar_senha")

        if nova != confirmar:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned

