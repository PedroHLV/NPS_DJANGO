from django.db import models
import uuid

class Respondent(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.email
