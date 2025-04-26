from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Program
from .serializers import ProgramSerializer

class ProgramCreateView(generics.CreateAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ProgramListView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        return Program.objects.filter(created_by=self.request.user).prefetch_related('enrollments__client')

class ProgramRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Program.objects.filter(created_by=self.request.user).prefetch_related('enrollments__client')

class ProgramUpdateView(generics.UpdateAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Program.objects.filter(created_by=self.request.user)

class ProgramDeleteView(generics.DestroyAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Program.objects.filter(created_by=self.request.user)
