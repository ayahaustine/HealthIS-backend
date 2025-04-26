from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(
            client__created_by=self.request.user,
            program__created_by=self.request.user
        ).select_related('client', 'program')

    def perform_create(self, serializer):
        serializer.save(enrolled_by=self.request.user)
