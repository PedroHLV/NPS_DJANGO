from django.db import models
from .response import Response
from .question import Question

class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'(Respondido por: {self.response.respondent.name}) / Resposta da questão: {self.question.text}, vinculada ao Formulário: {self.response.survey.title}'