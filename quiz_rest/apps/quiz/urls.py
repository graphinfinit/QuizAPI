from django.urls import path, re_path

from . import views
from .views import *


urlpatterns = [
    path('adm/quiz/<int:pk>', CreateUpdateDestroyQuiz.as_view({'get':'get',
                                                               'post':'create',
                                                               'delete':'destroy',
                                                               'put':'update'}), name='adm_quiz'),

    path('adm/quiz/question/<int:pk>', CreateUpdateDestroyQuestion.as_view({'get':'get',
                                                               'post':'create',
                                                               'delete':'destroy',
                                                               'put':'update'}), name='adm_quest'),


    path('user/quiz/all', UserViewQuiz.as_view({'get':'filter_activequizes'}), name='all_quizes'),
    path('user/quiz/<int:pk>', UserPostQuiz.as_view({'get':'get_foruser', 'post':'create_foruser'}), name='us_quiz'),
    path('user/quiz/detail/<int:pk>', UserDetailQuiz.as_view({'get':'get_quizesdetail'}), name='detail')

]

