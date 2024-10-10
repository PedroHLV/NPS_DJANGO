from django.db import models
from .response import Response
from .question import Question

class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(max_length=255, blank=True, null=True)
    choice = models.CharField(max_length=10, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"(Respondido por: {self.response.respondent.name}) / Resposta da questão: {self.question.text}, vinculada ao Formulário: {self.response.survey.title}"