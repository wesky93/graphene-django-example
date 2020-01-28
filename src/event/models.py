from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from group.models import UserGroup

User = get_user_model()


class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        try:
            return f"<장소:{self.id}:{self.name[:20]}>"
        except Exception:
            return super().__str__()


class MeetUp(models.Model):
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=50)
    d_day = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        try:
            return f"<밋업:{self.id}:{self.title[:20]}>"
        except Exception:
            return super().__str__()


class Topic(models.Model):
    meetup = models.ForeignKey(MeetUp, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        try:
            return f"<주제:{self.id}:{self.title[:20]}>"
        except Exception:
            return super().__str__()


class Comment(models.Model):
    text = models.TextField(null=True, blank=True)
    meetup = models.ForeignKey(MeetUp, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f"<댓글:{self.id}:밋업:{self.meetup_id}:작성자:{self.user_id}>"
        except Exception:
            return super().__str__()
