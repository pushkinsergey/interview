import jwt
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class Poll(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    description = models.TextField(default='')


class Question(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    text_question = models.TextField()
    type_question = models.SmallIntegerField(choices=(
        (1, "ответ текстом"),
        (2, "ответ с выбором одного варианта"),
        (3, "ответ с выбором нескольких вариантов")), default=1)


class Option(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    options = models.TextField(default='')


class Interview(models.Model):
    interviewee = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)


class Answer(models.Model):
    interview = models.ForeignKey('Interview', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)


class AnswerText(models.Model):
    answer = models.OneToOneField('Answer', on_delete=models.CASCADE)
    text_answer = models.TextField(default='')


class AnswerOption(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    option_answer = models.ForeignKey('Option', on_delete=models.CASCADE)
