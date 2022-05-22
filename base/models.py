from django.db import models

# Create your models here.

class Contact(models.Model):

    user_email = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(max_length=600, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_email)