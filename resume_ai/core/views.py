import os
import pypdf
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import logout
from dotenv import load_dotenv
from .models import PDFHistory, PasswordResetCode 
from google import genai
from google.genai.errors import APIError
from .forms import CadastroForm, UpdateUserForm, ChangePasswordForm 
from django.core.files.base import ContentFile
from fpdf import FPDF
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
import random


# O cliente é inicializado uma vez para reutilizar a configuração nas requisições.
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print(">>> Cliente Gemini inicializado com sucesso.")
    except Exception as e:
        # Sem um cliente válido, a view retorna indisponibilidade do serviço.
        print(f">>> ERRO CRÍTICO: Falha ao inicializar o cliente Gemini. Detalhe: {e}")
else:
    print(">>> ERRO DE CONFIGURAÇÃO: GEMINI_API_KEY não foi encontrada no .env.")

User = get_user_model()


@login_required
def index(request):
    return render(request, 'index.html', {'titulo': 'Página Inicial'})

@login_required
def configuracoes_conta_view(request):
    """Renderiza o painel de configurações para alterar/excluir conta."""
    return render(request, 'configuracoes.html', {'titulo': 'Configurações de Conta'})

@login_required
def alterar_dados_view(request):
    user = request.user

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados alterados com sucesso!")
            return redirect('alterar_dados')
    else:
        form = UpdateUserForm(instance=user)

    return render(request, 'alterar_dados.html', {'form': form})

@login_required
def excluir_conta_view(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()

        return redirect("conta_excluida")

    return render(request, "confirmar_exclusao.html")

def conta_excluida_view(request):
    return render(request, "conta_excluida.html")


@login_required
def historico_resumos(request):
    historicos = PDFHistory.objects.filter(user=request.user).order_by('-enviado_em')
    return render(request, 'historico.html', {'historicos': historicos})

@login_required
def deletar_pdf(request, id):
    pdf = get_object_or_404(PDFHistory, id=id, user=request.user)

    # Remove o arquivo do disco antes de apagar o registro.
    if pdf.arquivo and os.path.exists(pdf.arquivo.path):
        os.remove(pdf.arquivo.path)

    pdf.delete()

    return redirect("historico")


class CadastroView(CreateView):
    model = User
    form_class = CadastroForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('login')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index') 
        return super().dispatch(request, *args, **kwargs)


def logout_page_view(request):
    logout(request)  
    return render(request, 'logout.html')


@login_required
def resumir_pdf_view(request):
    """Exibe o formulário e processa o PDF enviado para gerar o resumo."""
    
    # Verifica se a chave da API foi configurada
    if client is None:
        if request.method == 'POST':
            return JsonResponse({'error': 'O serviço de IA está indisponível. Verifique a chave de API.'}, status=503)
        return render(request, 'resumir_pdf.html')

    if request.method == 'POST':
        # Recebe o arquivo e o idioma escolhido no formulário.
        uploaded_file = request.FILES.get('pdf_file')
        language = request.POST.get('language', 'Português')

        if not uploaded_file:
            return JsonResponse({'error': 'Nenhum arquivo PDF enviado.'}, status=400)

        # A API recebe o texto extraído, não o arquivo PDF.
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

        except Exception as e:
            return JsonResponse({'error': f'Erro ao processar PDF (pypdf): {e}'}, status=500)

        if not text.strip():
            return JsonResponse({'error': 'O PDF não contém texto legível.'}, status=400)

        # Monta o prompt e solicita o resumo ao Gemini.
        try:
            prompt = (
                f"Resuma o seguinte texto de um documento PDF. "
                f"O resumo deve ser conciso, com 3 a 5 parágrafos, no idioma **{language}**.\n\n"
                f"{text}"
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            resumo = response.text

            if not resumo:
                return JsonResponse({'error': 'A API retornou uma resposta vazia.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'Erro ao gerar resumo: {e}'}, status=500)

        # Gera um PDF com o conteúdo retornado pela IA.
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for linha in resumo.split("\n"):
            pdf.multi_cell(0, 10, linha)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        pdf_file = ContentFile(pdf_bytes)

        nome_pdf = f"resumo_{uploaded_file.name.replace('.pdf','')}.pdf"

        # O FileField salva o arquivo e atualiza o registro.
        registro = PDFHistory.objects.create(user=request.user)
        registro.arquivo.save(nome_pdf, pdf_file)

        # A tela recebe o resumo em formato JSON.
        return JsonResponse({'summary': resumo}, status=200)

    
    return render(request, 'resumir_pdf.html')


@login_required
def alterar_senha(request):
    user = request.user

    # Gera um código temporário e envia para o e-mail da conta.
    if "esqueci" in request.GET:
        codigo = str(random.randint(100000, 999999))
        expira = timezone.now() + timezone.timedelta(minutes=10)

        reset_obj, created = PasswordResetCode.objects.get_or_create(user=user)
        reset_obj.code = codigo
        reset_obj.expires_at = expira
        reset_obj.save()

        send_mail(
            "Código de verificação - Alteração de senha",
            f"Seu código de verificação é: {codigo}",
            None,
            [user.email],
        )

        messages.info(request, "Código enviado para seu e-mail!")
        return render(request, "alterar_senha.html", {"modo": "codigo"})

    if request.method == "POST":
        modo = request.POST.get("modo")
        campo = request.POST.get("campo_verificacao")
        nova = request.POST.get("nova_senha")
        confirmar = request.POST.get("confirmar_senha")

        if nova != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "alterar_senha.html", {"modo": modo})

        # Alteração usando a senha atual.
        if modo == "senha":
            if not user.check_password(campo):
                messages.error(request, "Senha atual incorreta.")
                return render(request, "alterar_senha.html", {"modo": "senha"})

            user.set_password(nova)
            user.save()
            messages.success(request, "Senha alterada com sucesso!")
            return render(request, "alterar_senha.html", {"modo": "senha"})

        # Recuperação usando o código enviado por e-mail.
        else:
            try:
                reset = PasswordResetCode.objects.get(user=user)
            except PasswordResetCode.DoesNotExist:
                messages.error(request, "Nenhum código encontrado. Clique em 'Esqueci minha senha'.")
                return redirect("alterar_senha")

            if not reset.is_valid():
                messages.error(request, "Código expirado. Gere outro.")
                reset.delete()
                return redirect("alterar_senha")

            if campo != reset.code:
                messages.error(request, "Código incorreto.")
                return render(request, "alterar_senha.html", {"modo": "codigo"})

            user.set_password(nova)
            user.save()
            reset.delete()

            messages.success(request, "Senha alterada com sucesso!")
            return render(request, "alterar_senha.html", {"modo": "senha"})

    return render(request, "alterar_senha.html", {"modo": "senha"})
