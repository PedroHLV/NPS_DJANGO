from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_survey_email(survey, respondent):
    survey_url = f"{settings.FRONTEND_URL}{reverse('survey_response', args=[survey.id, respondent.email])}"
    subject = f"Você foi convidado a participar da pesquisa: {survey.title}"
    message = f"Olá {respondent.name or respondent.email},\n\nPor favor, participe da nossa pesquisa:\n{survey_url}\n\nObrigado!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [respondent.email])
