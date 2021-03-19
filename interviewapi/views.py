import random
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
        #p1 = Poll.objects.get(pk=2)
        #Question.objects.filter(poll=p1).delete()
        #Question.objects.all().delete()
        #for i in range(1,10):
        #    type_question = int(round(random.random()*2+1))
        #    text_question='Вопрос номер %i'%i
        #    qi = Question(poll=p1, text_question=text_question, type_question=type_question)
        #    qi.save()
        #    if type_question>1:
        #        for j in range(2,int(round(random.random()*2+3))):
        #            oj = Option(question=qi, options='выбор %i'%j)
        #            oj.save()


        question = Question.objects.filter(poll=pk)
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

    def post(self, request, pk,  format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionEdit(APIView):
    def put(self, request, pk, format=None):
        question = Question.objects.get(pk=pk)
        if question:
            serializer = QuestionSerializer(poll, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Interviews(APIView):
    def get(self, request, format=None):
        #u=User.objects.get(pk=1)
        #p=Poll.objects.get(pk=2)
        #i=Interview(interviewee=u,poll=p)
        #i.save()
        #interview = Interview.objects.filter(interviewee=user)
        interview = Interview.objects.filter(interviewee__id=1)
        serializer = InterviewSerializer(interview, many=True)
        return Response(serializer.data)

class Interviewing(APIView):
    def get(self, request, pk, format=None):
        interview = Interview.objects.get(pk=pk)
        #question = Question.objects.filter(poll=interview.poll)
        #for q in question:
        #    a = Answer(question=q, interview=interview)
        #    a.save()
        #    if q.type_question==1:
        #        at = AnswerText(answer=a, text_answer='Ответ на вопрос '+q.text_question)   
        #        at.save()                 
        #    else:
        #        ao = AnswerOption(answer=a, option_answer=Option.objects.filter(question=q)[1])
        #        ao.save()
        answer = Answer.objects.filter(interview=interview)
        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        interview = Interview.objects.get(pk=pk)
        serializer = InterviewingSerializer(data=request.data)
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
        }) #'user_id': user.pk,'email': user.email
