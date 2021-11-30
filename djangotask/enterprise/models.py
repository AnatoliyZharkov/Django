from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import jwt
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + settings.JWT_TOKEN_LIFETIME

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Department(models.Model):
    name_of_dep = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    head = models.CharField(max_length=255)

    def __str__(self):
        return self.name_of_dep


class Positions(models.Model):
    name = models.CharField(max_length=100)
    salary = models.FloatField(default=0)
    num_of_vac_days = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name


class Worker(models.Model):
    full_name = models.CharField(max_length=255)
    passport_data = models.TextField()
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    depart = models.ForeignKey(Department, related_name='workers', on_delete=models.CASCADE)
    pos = models.ForeignKey(Positions, related_name='workers', on_delete=models.CASCADE)
    experience = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(50)])
    salary = models.FloatField(default=0)
    status = models.CharField(max_length=7)  # 'vac' or 'not_vac'

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        for i in Positions.objects.filter(name__exact=self.pos):
            right_sal = (i.salary * ((1 + 0.012)**self.experience))
            right_sal = float('{:.2f}'.format(right_sal))
            if self.salary != right_sal:
                raise ValidationError(_(f'Wrong salary, according to worker experience it should be {right_sal}'))
        if Worker.objects.filter(depart__exact=self.depart).count() >= 20:
            raise ValidationError(_('The department can have a maximum of 20 workers'))
        counter = 0
        for j in Worker.objects.filter(depart__exact=self.depart):
            if j.status == 'vac':
                counter += 1
                if counter >= 5:
                    raise ValidationError(_('The department can have a maximum of 5 workers in vacation'))
        super(Worker, self).save(*args, **kwargs)


class PosHistory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    worker_pos = models.ForeignKey(Positions, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.worker


class VacHistory(models.Model):
    worker = models.ForeignKey(Worker, related_name='vacations', on_delete=models.CASCADE)
    start_date = models.DateField()
    that_time_pos = models.ForeignKey(Positions, on_delete=models.CASCADE)
    num_of_days = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.worker

    def save(self, *args, **kwargs):
        for i in PosHistory.objects.filter(worker__exact=self.worker):
            if i.end_date:
                if i.start_date <= self.start_date < i.end_date:
                    if self.that_time_pos != i.worker_pos:
                        raise ValidationError(_(f'Wrong position, that time position should be {i.worker_pos}'))
            else:
                if i.start_date <= self.start_date:
                    if self.that_time_pos != i.worker_pos:
                        raise ValidationError(_(f'Wrong position, that time position should be {i.worker_pos}'))
        for i in Positions.objects.filter(name__exact=self.that_time_pos):
            if self.num_of_days != i.num_of_vac_days:
                raise ValidationError(_(f'Wrong number of days, it should be {i.num_of_vac_days}'))
        super(VacHistory, self).save(*args, **kwargs)
