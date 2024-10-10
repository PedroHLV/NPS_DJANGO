from django.db import models
from .surveys import Survey

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Texto'),
        ('yes_no', 'Sim/Não'),
        ('rating', 'Nota (1-10)')
    ]
    # survey = models.ForeignKey(Survey, related_name='survey_questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=text)

    def __str__(self):
        return f"{self.text} ({self.get_question_type_display()})"
