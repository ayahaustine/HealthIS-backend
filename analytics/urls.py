from django.urls import path
from .views import TotalClientsView, ActiveProgramsView, EnrollmentsView

urlpatterns = [
    path('total_clients/', TotalClientsView.as_view(), name='total_clients'),
    path('active_programs/', ActiveProgramsView.as_view(), name='active_programs'),
    path('enrollments/', EnrollmentsView.as_view(), name='enrollments'),
]
