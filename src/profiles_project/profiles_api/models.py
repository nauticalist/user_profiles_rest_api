from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)


class UserProfileManager(BaseUserManager):
    """
    Make django to use our new user model
    """
    def create_user(self, email, name, password=None):
        """
        Creates a new user profile object
        """
        if not email:
            raise ValueError("You must define an email address!")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Create and saves a new super user with given details
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom user profile model
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """
        Return user full name
        """
        return self.name

    def get_short_name(self):
        """
        Returns users short name
        """
        return self.name

    def __str__(self):
        """
        Return email address as string when class called
        """
        return self.email


class ProfileFeedItem(models.Model):
    """
    Profile status update
    """
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
