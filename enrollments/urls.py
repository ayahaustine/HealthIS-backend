from django.urls import path
from .views import (
    EnrollmentCreateView,
    EnrollmentListView,
    EnrollmentRetrieveView,
    EnrollmentDeleteView,
)

urlpatterns = [
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/<uuid:pk>/', EnrollmentRetrieveView.as_view(), name='enrollment-retrieve'),
    path('enrollments/<uuid:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment-delete'),
]
