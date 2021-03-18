from datetime import datetime
from datetime import timedelta
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
        current_date = datetime.now()
        poll = Poll.objects.filter(start_date__lte=current_date).filter(
            end_date__gte=current_date)
        #poll = Poll.objects.all()
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
        #p1 = Poll.objects.get(pk=5)
        #q1 = Question(poll=p1, text_question="Третий вопрос", type_question=2)
        # q1.save()
        #o1 = Option(question=q1, options='выбор 1')
        # o1.save()
        #o2 = Option(question=q1, options='выбор 2')
        # o2.save()
        #o3 = Option(question=q1, options='выбор 3')
        # o3.save()

        question = Question.objects.filter(poll=pk)
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request, pk,  format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Interviews(APIView):
    def get(self, request, format=None):
        #u=User.objects.get(pk=1)
        #p=Poll.objects.get(pk=5)
        #i=Interview(interviewee=u,poll=p)
        #i.save()
        #interview = Interview.objects.filter(interviewee=user)
        interview = Interview.objects.filter(interviewee__id=1)
        serializer = InterviewSerializer(interview, many=True)
        return Response(serializer.data)


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
