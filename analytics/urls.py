from django.urls import path
from .views import *

urlpatterns = [
    path('total_clients/', TotalClientsView.as_view(), name='total_clients'),
    path('active_programs/', ActiveProgramsView.as_view(), name='active_programs'),
    path('enrollments/', EnrollmentsView.as_view(), name='enrollments'),
    path('monthly_enrollments/', MonthlyEnrollmentsView.as_view(), name='monthly_enrollment'),
    path('monthly_clients_programs/', MonthlyClientsAndProgramsView.as_view(), name='monthly_clients_programs'),
]
