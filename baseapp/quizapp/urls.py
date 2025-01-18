from . import views
from django.urls import path

urlpatterns = [
    path('batches/', views.BatchApiView.as_view(), name='batches'),
    path('student-data/', views.StudentFilterView.as_view(), name='student-filter'),
    path('student-update/', views.StudentFilterView.as_view(), name='student-update'),
    path('student-delete/<str:student_id>/', views.StudentFilterView.as_view(), name='student-delete'),
]