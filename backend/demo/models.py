from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    # See https://docs.djangoproject.com/en/2.1/ref/models/fields/#model-field-types
    content = models.CharField(max_length=512)
    add_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
