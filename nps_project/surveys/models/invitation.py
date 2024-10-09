import uuid
from django.db import models
from .respondent import Respondent
from .surveys import Survey

class Invitation(models.Model):
    respondent = models.ForeignKey(Respondent, related_name='invitations', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='invitations', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Convite para {self.respondent.email} - Formulário: {self.survey.title}'
