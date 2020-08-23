from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):

    TODO_STATUS = [('C', 'Created'), ('P', 'In progress'), ('D', 'Done')]

    title = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey('Organization', related_name='tasks', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TODO_STATUS, default='C', max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('creation_date',)


class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


# Create custom user model with email as main field
class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    email = models.EmailField('email address', unique=True)
    organizations = models.ManyToManyField('Organization')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
