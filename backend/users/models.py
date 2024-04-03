from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def full_name(self):
        return self.get_full_name()
