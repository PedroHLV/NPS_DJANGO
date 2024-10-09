from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from urllib.parse import urljoin
from ..models.invitation import Invitation

def send_survey_email(survey, respondent):
    # Criar uma nova instância de Invitation
    invitation = Invitation.objects.create(respondent=respondent, survey=survey)
    
    # Gerar a URL completa do formulário utilizando o token da Invitation
    path = reverse('survey_response', args=[survey.id, invitation.token])
    survey_url = urljoin(settings.FRONTEND_URL, path)
    
    # Assunto do e-mail
    subject = f"Você foi convidado a participar da pesquisa: {survey.title}"
    
    # Mensagem do e-mail
    message = (
        f"Olá {respondent.name or respondent.email},\n\n"
        f"Por favor, participe da nossa pesquisa:\n{survey_url}\n\n"
        f"Obrigado!"
    )
    
    # Enviar o e-mail
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [respondent.email],
        fail_silently=False,  # Defina como True se não quiser que exceções sejam levantadas
    )
