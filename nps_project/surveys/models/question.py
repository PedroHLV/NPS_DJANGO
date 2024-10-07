from django.db import models
from .surveys import Survey

class Question(models.Model):
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text
