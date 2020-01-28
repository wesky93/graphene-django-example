from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    meeting_cycle = models.CharField(max_length=200)

    def __str__(self):
        try:
            return f"<소모임:{self.id}:{self.name[:20]}>"
        except Exception:
            return super().__str__()


class Organizer(models.Model):
    name = models.CharField(max_length=100)
    slack_id = models.CharField(max_length=100)
    organized_groups = models.ManyToManyField(UserGroup)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        try:
            return f"<오거나이저:{self.id}:{self.slack_id}>"
        except Exception:
            return super().__str__()
