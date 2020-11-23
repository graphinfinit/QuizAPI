from rest_framework import serializers
from .models import *

import json


'''
Вложенный сериализатор для детализации опроса
'''
class AnswerBooleanViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerBoolean
        fields = ['id', 'answer', 'descript']

class AnswerTextViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerText
        fields = ['id', 'answer']


class QuestionViewSerializer(serializers.ModelSerializer):
    textanswers = AnswerTextViewSerializer(many=True)
    booleananswers = AnswerBooleanViewSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type_questions', 'booleananswers', 'textanswers']

class FullQuizViewSerializer(serializers.ModelSerializer):
    questions = QuestionViewSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'date_start', 'date_end', 'descript', 'questions']

    def save(self, *args, **kwargs):
        '''
        Сохраняем пройденный пользователем опрос
        id_пользователя post_user
        id_опроса quiz_id
        сам опрос в JSON quiz_data
        '''

        post_user = kwargs['post_user']
        quiz_id = kwargs['pk']
        quiz_data = json.dumps(self.data)

        user_indatabase, _ = Post_user.objects.get_or_create(post_id=post_user)
        res, created = Result.objects.get_or_create(user_id=Post_user.objects.get(post_id=post_user),
                                  quiz=Quiz.objects.get(id=quiz_id),
                                  quiz_data=quiz_data
                                  )
        if not created:
            raise NameError()


class QuizViewSerializer(serializers.ModelSerializer):
    '''
    Все опросы для пользователя =)
    '''
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    descript = serializers.CharField()
    class Meta:
        model = Quiz
        fields = ['id', 'name', 'date_start', 'date_end', 'descript']

'''
end

'''

class JsonReaderSerializer(serializers.Serializer):
    def to_representation(self, instance):
        instanse = json.loads(instance)
        return instanse

class ResultSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Post_user)
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz)
    quiz_data = JsonReaderSerializer()  # JsonFields??  если PostgresSQL

























