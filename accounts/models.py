from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, first_name, email, password, mobile, role, **kwargs):
        if not first_name:
            raise ValueError("First Name is required") 
        if not email:
            raise ValueError("Email is required")
        if not mobile:
            raise ValueError("Mobile number is required")
        if not password:
            raise ValueError("Password is required")
        if not role:
            raise ValueError("Role is required")
        email = self.normalize_email(email)
        user = self.model(mobile=mobile, email=email, role=role, first_name=first_name, **kwargs)
        user.set_password(password)
        user.save()
        return user

        
    def create_user(self, first_name, email, password, mobile, role, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(first_name, email, password, mobile, role, **kwargs)

    def create_superuser(self, first_name, email, password, mobile, role, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self._create_user(first_name, email, password, mobile, role, **kwargs)

# Create your models here.
class User(AbstractUser):
    username = None
    ROLES = (
        (1, 'Administrator'),
        (2, 'Support Staff'),
        (3, 'Distributor'),
        (4, 'Retailer'),
        (5, 'Salesman')
    )
    mobile = models.CharField(max_length=10, unique=True)
    role = models.IntegerField(default=1, choices=ROLES)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = ['first_name', 'email', 'role']

    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class State(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=32)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
