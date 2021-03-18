from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from interviewapi.models import Poll
from interviewapi.models import Question
from interviewapi.models import Option
from interviewapi.models import Interview
from interviewapi.models import Answer
from interviewapi.models import AnswerText
from interviewapi.models import AnswerOption
from interviewapi.serializers import PollSerializer
from interviewapi.serializers import QuestionSerializer
from interviewapi.serializers import OptionSerializer
from interviewapi.serializers import InterviewSerializer
from interviewapi.serializers import AnswerSerializer
from interviewapi.serializers import AnswerTextSerializer
from interviewapi.serializers import AnswerOptionSerializer
from interviewapi.serializers import UserSerializer


class PollList(APIView):
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        poll = Poll.objects.all()
        serializer = PollSerializer(poll, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollEdit(APIView):
    def get(self, request, pk, format=None):
        poll = Poll.objects.get(pk=pk)
        if poll:
            serializer = PollSerializer(poll)
            return Response(serializer.data)

    def put(self, request, pk, format=None):
        poll = Poll.objects.get(pk=pk)
        if poll:
            serializer = PollSerializer(poll, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        poll = Poll.objects.get(pk=pk)
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionList(APIView):
    def get(self, request, pk,  format=None):
        #p1 = Poll.objects.get(pk=1)
        #q1 = Question(poll=p1, text_question="Второй вопрос", type_question=1)
        #q1.save()
        question = Question.objects.filter(poll=pk)
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request, pk,  format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
