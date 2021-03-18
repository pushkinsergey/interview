from rest_framework import serializers
from django.contrib.auth.models import User
from interviewapi.models import Poll
from interviewapi.models import Question
from interviewapi.models import Option
from interviewapi.models import Interview
from interviewapi.models import Answer
from interviewapi.models import AnswerText
from interviewapi.models import AnswerOption


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'poll', 'text_question', 'type_question')


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'question', 'options')


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ('id', 'interviewee', 'poll')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'interview', 'question')


class AnswerTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerText
        fields = ('id', 'answer', 'text_answer')


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ('id', 'answer', 'option_answer')


class UserSerializer(serializers.ModelSerializer):
    #interview = serializers.PrimaryKeyRelatedField(
    #    many=True, queryset=Interview.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
