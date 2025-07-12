from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os

from web.tasks import resize_avatar


class CustomUser(AbstractUser):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        old_avatar = None
        if self.pk:
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar

        super().save(*args, **kwargs)

        if self.avatar and self.avatar != old_avatar:
            resize_avatar.delay(self.avatar.path)
            if old_avatar and os.path.isfile(old_avatar.path) and old_avatar != self.avatar:
                os.remove(old_avatar.path)
