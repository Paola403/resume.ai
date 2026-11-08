from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as core_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),

    # Acesso e cadastro
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user = True), name='login'),
    path('cadastro/', core_views.CadastroView.as_view(), name='cadastro'),

    # Encerramento da sessão
    path('logout/', core_views.logout_page_view, name='logout'),

    # Página inicial
    path('', core_views.index, name='index'), 

    # Upload e resumo de PDFs
    path('resumir/', core_views.resumir_pdf_view, name='resumir_pdf'), 

    # Configurações da conta
    path('configuracoes/', core_views.configuracoes_conta_view, name='configuracoes_conta'),

    # Histórico de arquivos
    path('historico/', core_views.historico_resumos, name='historico'),

    # Exclusão de arquivo do histórico
    path("historico/deletar/<int:id>/", core_views.deletar_pdf, name="deletar_pdf"),

    # Edição dos dados da conta
    path('alterar-dados/', core_views.alterar_dados_view, name='alterar_dados'),

    # Alteração de senha
    path("alterar-senha/", core_views.alterar_senha, name="alterar_senha"),

    # Exclusão da conta
    path("excluir-conta/", core_views.excluir_conta_view, name="excluir_conta"),

    # Confirmação da exclusão
    path("conta-excluida/", core_views.conta_excluida_view, name="conta_excluida"),
]
# Disponibiliza os arquivos enviados quando DEBUG está ativo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)