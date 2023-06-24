from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class MeetUpUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')

    telegram_id = models.CharField(
        'Telegram id',
        max_length=50,
        db_index=True)

    is_speaker = models.BooleanField(
        default=False,
        verbose_name='Докладчик')

    phone = PhoneNumberField(
        'Номер телефона',
        null=True,
        blank=True,
        db_index=True)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Speach(models.Model):
    title = models.CharField(
        'Наименование',
        max_length=200,)

    description = models.TextField(
        'Описание', blank=True)

    speaker = models.ForeignKey(
        MeetUpUser,
        on_delete=models.CASCADE,
        related_name='speachs',
        verbose_name='Спикер')

    start_at = models.DateTimeField(
        verbose_name='Начало')

    end_at = models.DateTimeField(
        verbose_name='Окончание')


    def __str__(self):
        return self.title


class Qustion(models.Model):
    title = models.TextField(
        'Вопрос',)

    speach = models.ForeignKey(
        Speach,
        on_delete=models.CASCADE,
        related_name='qustions',
        verbose_name='К докладу',)

    user = models.ManyToManyField(
        User,
        related_name='qustions',
        verbose_name='Кто задал вопрос')

    def __str__(self):
        return self.title
