
import uuid

from django.contrib.auth.models import User
from django.db import models



class RedirectRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    redirect_url = models.CharField(null=False, max_length=450)
    is_private = models.BooleanField(default=False)
    redirect_identifier = models.CharField(null=False, max_length=16, unique=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="redirect_rules")

    def save(self, *args, **kwargs):
        """ Auto filling 'redirect_identifier' """
        if not self.redirect_identifier:
            self.redirect_identifier = self.generate_redirect_identifier()
        super().save(*args, **kwargs)


    @staticmethod
    def generate_redirect_identifier():
        """ Generating a random 16-digits unique identifier """
        return uuid.uuid4().hex[:16]

    def __str__(self):
        return f"{self.redirect_url} {'(Private)' if self.is_private else ''}: {self.redirect_identifier}"

    class Meta:
        db_table = "redirect_rules"