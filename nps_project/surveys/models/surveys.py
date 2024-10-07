from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField('Question', related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.title