from . import views
from django.urls import path

urlpatterns = [
    path('batches/', views.BatchApiView.as_view(), name='batches'),
    path('sections/', views.SectionApiView.as_view(), name='section'),
    path('quiz/student-data/', views.StudentFilterView.as_view(), name='student-data'),
    path('quiz/student-update/', views.StudentFilterView.as_view(), name='student-update'),
    path('quiz/student-delete/<str:student_id>/', views.StudentFilterView.as_view(), name='student-delete'),
    path('quiz/create-quiz/',views.QuizApiView.as_view(), name="create-quiz"),
    path('quiz/quizmarks/',views.StudentQuizResultsView.as_view(), name="create-quiz"),
]