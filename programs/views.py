from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Program
from .serializers import ProgramSerializer
from .permissions import IsCreatorOrReadOnly

class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def get_queryset(self):
        return Program.objects.filter(
            is_active=True,
            created_by=self.request.user).prefetch_related('clients')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False  # Soft delete
        instance.save()
