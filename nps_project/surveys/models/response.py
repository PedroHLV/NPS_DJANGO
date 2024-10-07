from django.db import models
from .respondent import Respondent
from .surveys import Survey

class Response(models.Model):
    respondent = models.ForeignKey(Respondent, related_name='responses', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response by {self.respondent.email} to {self.survey.title}'
