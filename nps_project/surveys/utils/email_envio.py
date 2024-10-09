from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from urllib.parse import urljoin
from ..models.invitation import Invitation
from django.core.mail import EmailMultiAlternatives


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
        f"Esperamos que esteja bem!\n\n"
        f"Estamos realizando uma pesquisa para melhorar nossos serviços e gostaríamos muito de contar com a sua participação.\n\n"
        f"A sua opinião é extremamente valiosa para nós e nos ajudará a entender melhor suas necessidades e expectativas.\n\n"
        f"Para participar, clique no link abaixo:\n"
        f"{survey_url}\n\n"
        f"Este formulário permanecerá disponível por tempo limitado, então não perca a oportunidade de contribuir.\n\n"
        f"Agradecemos antecipadamente pela sua colaboração!\n\n"
        f"Atenciosamente,\n"
        f"Sua Empresa/Equipe"
    )

    
    # Enviar o e-mail
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [respondent.email],
        fail_silently=False,
    )
