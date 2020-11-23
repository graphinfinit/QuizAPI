from django.db import models

'''
актуально для PostgresSQL
from django.contrib.postgres.fields import JSONField
'''

class Quiz(models.Model):
    name = models.CharField('Название', max_length=200)
    date_start = models.DateField('Начало опроса')
    date_end = models.DateField('Окончание опроса')
    descript = models.TextField('Описание опроса')
    is_active = models.BooleanField('Актуальность', default=True)

    def __str__(self):
        return '%s ' % (self.name)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


CATEGORY = ((1, 'Текстовый'),
            (2, 'С одним вариантом ответа'),
            (3, 'С несколькими вариантами ответа') )

class Question(models.Model):
    text = models.TextField('Текст вопроса')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    type_questions = models.IntegerField('Тип вопроса', choices=CATEGORY)

    def __str__(self):
        return '%s' % (self.quiz)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerText(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='textanswers')
    answer = models.TextField('Текстовый ответ', null=True, default=None)
    good_answer = models.TextField('Правильный текстовый ответ')

    def __str__(self):
        return '%s' % (self.question)

    class Meta:
        verbose_name = 'Текстовый ответ'
        verbose_name_plural = 'Текстовые ответы'

class AnswerBoolean(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='booleananswers')
    answer = models.BooleanField('Ответ', null=True)
    good_answer = models.BooleanField('Правильный ответ')
    descript = models.CharField('Описание пункта', max_length=50, default='Один из многих пунктиков...')

    def __str__(self):
        return '%s' % (self.descript)

    class Meta:
        verbose_name = 'Ответ вариант'
        verbose_name_plural = 'Ответ варианты'


class Post_user(models.Model):
    post_id = models.PositiveIntegerField('id пользователя', unique=True, primary_key=True)
    user_name = models.CharField('Имя пользователя', max_length=50, default='Anonymous')

    def __str__(self):
        return '%s' % (self.post_id)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'


class Result(models.Model):
    user_id = models.ForeignKey(Post_user, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_data = models.TextField()

    def __str__(self):
        return '%s' % (self.user_id)
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


