from . import views
from django.urls import path

urlpatterns = [
    path('batches/', views.BatchApiView.as_view(), name='batches'),
    path('sections/', views.SectionApiView.as_view(), name='section'),
    path('quiz/subject/', views.SubjectApiView.as_view(), name='subject'),
    path('quiz/create-student/', views.StudentApiView.as_view(), name='student-data-create'),
    path('quiz/student-update/', views.StudentApiView.as_view(), name='student-update'),
    path('quiz/student-delete/<str:student_id>/', views.StudentApiView.as_view(), name='student-delete'),
    path('quiz/create-quiz/',views.QuizApiViews.as_view(), name="create-quiz"),
    #path('quiz/quizmarks/',views.StudentQuizResultsView.as_view(), name="create-quiz"),
]