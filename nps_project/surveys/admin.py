from django.contrib import admin
from .models.answer import Answer
from .models.question import Question
from .models.respondent import Respondent
from .models.response import Response
from .models.surveys import Survey
from .models.invitation import Invitation
from django.template.response import TemplateResponse
from .models.surveys import Survey
from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .utils.email_envio import send_survey_email
from django.contrib import messages, admin
from django.shortcuts import render, redirect

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_survey', 'question', 'text')
    readonly_fields = ('response', 'question', 'text')
    actions = None

    def get_survey(self, obj):
        return obj.response.survey.title
    get_survey.short_description = 'Formulário'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        return self.readonly_fields

    def get_actions(self, request):
        return []
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    filter_horizontal = ('questions',)
    ordering = ('-created_at',)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('respondent', 'survey', 'submitted_at')
    readonly_fields = ['respondent', 'survey', 'submitted_at']
    # inlines = [AnswerInline]

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False
class RespondentAdmin(admin.ModelAdmin):
    list_display = ( 'name','email')
    search_fields = ('email', 'name')
class MyAdminSite(admin.AdminSite):
    site_header = 'Administração do Sistema NPS'
    site_title = 'Admin NPS'
    index_title = 'Bem-vindo ao Admin do Sistema NPS'

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        # Verificar se o usuário é superusuário
        if request.method == 'POST':
            if not request.user.is_superuser:
                messages.error(request, "Você não tem permissão para enviar formulários.")
                return redirect('admin:index')

            # Processar o POST do formulário de envio
            respondent_ids = request.POST.getlist('respondent_ids[]')
            survey_id = request.POST.get('survey_id')

            # Validar os IDs
            if not respondent_ids or not survey_id:
                messages.error(request, "Respondente ou Formulário não selecionado.")
                return redirect('admin:index')

            try:
                respondents = Respondent.objects.filter(id__in=respondent_ids)
                survey = Survey.objects.get(id=survey_id)
            except Survey.DoesNotExist:
                messages.error(request, "Formulário inválido.")
                return redirect('admin:index')
            
            # Verificar se existem respondentes válidos
            if not respondents.exists():
                messages.error(request, "Nenhum respondente válido selecionado.")
                return redirect('admin:index')

            # Enviar os e-mails
            success_emails = []
            error_emails = []
            for respondent in respondents:
                try:
                    send_survey_email(survey, respondent)
                    success_emails.append(respondent.email)
                except Exception as e:
                    error_emails.append((respondent.email, str(e)))

            # Consolidar as mensagens de sucesso
            if success_emails:
                emails_str = "', '".join(success_emails)
                messages.success(request, f"Formulário '{survey.title}' enviado para '{emails_str}'.")

            # Exibir mensagens de erro individuais
            if error_emails:
                for email, error in error_emails:
                    messages.error(request, f"Ocorreu um erro ao enviar o e-mail para '{email}': {error}")

            return redirect('admin:index')

        # Para requisições GET, renderizar a página normalmente
        users = User.objects.all()
        surveys = Survey.objects.all()
        respondents = Respondent.objects.all()
        context = {
            **self.each_context(request),
            'users': users,
            'surveys': surveys,
            'respondents': respondents,
        }
        return TemplateResponse(request, 'admin/custom_index.html', context)

admin_site = MyAdminSite()
admin_site.register(User, UserAdmin)
admin_site.register(Respondent, RespondentAdmin)
admin_site.register(Response, ResponseAdmin)
admin_site.register(Answer, AnswerAdmin)
admin_site.register(Survey, SurveyAdmin)
admin_site.register(Question)