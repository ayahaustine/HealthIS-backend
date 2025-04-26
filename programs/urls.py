# programs/urls.py
from django.urls import path
from .views import (
    ProgramCreateView,
    ProgramListView,
    ProgramRetrieveView,
    ProgramUpdateView,
    ProgramDeleteView,
)

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/create/', ProgramCreateView.as_view(), name='program-create'),
    path('programs/<str:uuid>/', ProgramRetrieveView.as_view(), name='program-retrieve'),
    path('programs/<str:uuid>/update/', ProgramUpdateView.as_view(), name='program-update'),
    path('programs/<str:uuid>/delete/', ProgramDeleteView.as_view(), name='program-delete'),
]
