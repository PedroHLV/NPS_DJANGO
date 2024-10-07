from django.db import models

class Respondent(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.email