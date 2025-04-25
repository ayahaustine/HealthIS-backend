from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer
from programs.models import Program

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'first_name', 'last_name', 'id',
        'county', 'sub_county', 'phone_number'
    ]

    def get_queryset(self):
        return Client.objects.filter(
            is_active=True,
            created_by=self.request.user
        ).prefetch_related('programs')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
