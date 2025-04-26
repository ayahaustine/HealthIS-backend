from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer

# Create
class ClientCreateView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# List
class ClientListView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'uuid', 'county', 'sub_county']

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user).prefetch_related('enrollments__program')

# Retrieve
class ClientRetrieveView(generics.RetrieveAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

# Update
class ClientUpdateView(generics.UpdateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)

# Delete
class ClientDeleteView(generics.DestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)
