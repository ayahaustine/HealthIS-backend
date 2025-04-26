from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(client__created_by=self.request.user)

class EnrollmentRetrieveView(generics.RetrieveAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(client__created_by=self.request.user)

class EnrollmentDeleteView(generics.DestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(client__created_by=self.request.user)
