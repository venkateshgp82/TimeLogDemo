from django.urls import path
from .views import ProjectView, ProjectDetail, TimelogView, TimelogDetail, UserProfileView
urlpatterns = [
    path('project', ProjectView.as_view()),
    path('project/<str:project_id>', ProjectDetail.as_view()),
    path('timelog', TimelogView.as_view(), name='timelogs'),
    path('timelogdetail', TimelogDetail.as_view(), name='timelog-detail'),
    path('tag', UserProfileView.as_view()),
]