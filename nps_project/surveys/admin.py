from django.contrib import admin
from .models.answer import Answer
from .models.question import Question
from .models.respondent import Respondent
from .models.response import Response
from .models.surveys import Survey
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

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
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
    list_display = ('email', 'name')
    search_fields = ('email', 'name')
class MyAdminSite(admin.AdminSite):
    site_header = 'Administração do Sistema NPS'
    site_title = 'Admin NPS'
    index_title = 'Bem-vindo ao Admin do Sistema NPS'

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def index(self, request, extra_context=None):
        if not request.user.is_superuser:
            messages.error(request, "Você não tem permissão para acessar esta página.")
            return redirect('admin:login')

        if extra_context is None:
            extra_context = {}

        # Processar o POST do formulário de envio
        if request.method == 'POST':
            respondent_id = request.POST.get('respondent_id')
            survey_id = request.POST.get('survey_id')

            # Validar os IDs
            if not respondent_id or not survey_id:
                messages.error(request, "Respondente ou Formulário não selecionado.")
                return redirect('admin:index')

            try:
                respondent = Respondent.objects.get(id=respondent_id)
                survey = Survey.objects.get(id=survey_id)
            except (Respondent.DoesNotExist, Survey.DoesNotExist):
                messages.error(request, "Respondente ou Formulário inválido.")
                return redirect('admin:index')

            # Enviar o e-mail
            try:
                send_survey_email(survey, respondent)
                messages.success(request, f"Formulário '{survey.title}' enviado para '{respondent.email}'.")
            except Exception as e:
                messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {e}")
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
admin_site.register(Respondent)
admin_site.register(Question)
admin_site.register(Response)
admin_site.register(Answer)
admin_site.register(Survey, SurveyAdmin)