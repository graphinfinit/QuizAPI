
'''
Функционал для пользователей системы:
- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID,
 по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов.
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя
'''

from datetime import datetime

from .models import *
from .serializers import FullQuizViewSerializer, QuizViewSerializer, ResultSerializer, QuestionViewSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



class UserViewQuiz(viewsets.ViewSet):
    serializer_class = QuizViewSerializer
    queryset = Quiz.objects.all()

    def filter_activequizes(self, request):
        '''
        Все опросы для пользователя =)
        '''
        quizes = Quiz.objects.filter(is_active=True, date_end__gte=datetime.now().date())
        serializer = QuizViewSerializer(quizes, many=True)
        return Response(serializer.data)

class UserPostQuiz(viewsets.ViewSet):
    queryset = Quiz.objects
    serializer_class = FullQuizViewSerializer

    def get_foruser(self,request, pk):
        quiz = Quiz.objects.get(id= pk)
        serializer = FullQuizViewSerializer(quiz)
        return Response(serializer.data)

    def create_foruser(self, request, pk):
        quiz = request.data
        serializer = FullQuizViewSerializer(data=quiz)

        if serializer.is_valid():
            # SAVE
            try:
                serializer.save(self, post_user=request.GET['post_user'], pk=pk)
                return Response({'OK': 'Данные опроса сохранены в базе!'}, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(
                    {'error':
                         'Не удалось сохранить опрос. Пользователь с id = {} уже прошел опрос'.format(request.GET['post_user'])})
        else:
            raise ValidationError(serializer.errors)

class UserDetailQuiz(viewsets.ViewSet):
    queryset = Result.objects
    serializer_class = ResultSerializer

    def get_quizesdetail(self, request, pk):
        results = Result.objects.filter(user_id=Post_user.objects.get(post_id=pk))
        serializer = ResultSerializer(results, many=True)
        return Response({'results':serializer.data})

'''
Функционал для администратора системы:
- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. 
Атрибуты опроса: название, дата старта, дата окончания, описание. 
После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе.
 Атрибуты вопросов: текст вопроса, тип вопроса 
 (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)
'''

class CreateUpdateDestroyQuiz(viewsets.ModelViewSet):
    serializer_class = QuizViewSerializer
    queryset = Quiz.objects
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
            try:
                queryset = self.queryset.get(id = pk)
            except ObjectDoesNotExist:
                return Response({'ObjectDoesNotExist': 'Объект не найден!'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        try:
            quiz = self.queryset.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'ObjectDoesNotExist': 'Объект не найден!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'ObjectDoesNotExist': 'Объект не найден!'}, status=status.HTTP_400_BAD_REQUEST)
        quiz.delete()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUpdateDestroyQuestion(viewsets.ModelViewSet):
    serializer_class = QuestionViewSerializer
    queryset = Question.objects
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            queryset = self.queryset.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'ObjectDoesNotExist': 'Объект не найден!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)



































