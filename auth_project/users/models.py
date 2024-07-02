from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  name = models.CharField(max_length=255)
  email = models.EmailField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  username = None #As it is required for the abstract user so we override it.

  USERNAME_FIELD = 'email' #we login with email,pass NOT with username,pass as django do
  REQUIRED_FIELDS = [] #we don't need to enter username while creating a user.