from django.db import models
# standard base classes for overriding the default django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import  PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# we importing the settings from the django project
from django.conf import settings


# creating a custom manager, which can handle users with email and not
# the defaut username
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        #the half part of emails in theory can be case sensitive
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # security reason, passwords should be stored as hash in
        # the database. The .set_password function is the default encryption
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        #self is automatically passed in in class functions
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Specify the model manager we will use. It is neede, bcause we will
    # use our custom user model with the django cli
    objects = UserProfileManager()

    # this overrides the default USERNAME_FIELD, which is username instead of
    # email, what we want here
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    #custom functions needed for django
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name # we are returning the same here

    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    #linking different models --> foreign key
    user_profile = models.ForeignKey(
        #best practice is to import the model from the settings, because
        # if it would be changed in the future, foreign keys would have to be
        # changed manually
        settings.AUTH_USER_MODEL,
        # specify here what should be done with the feed items, if the relational
        # item is deleted (user is deleted). Cascade: cascade the change
        on_delete=models.CASCADE
    )
    # contains the text of the feed update
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
