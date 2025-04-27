from rest_framework import generics, filters
from clients.models import Client
from public.serializers import PublicClientSerializer
from rest_framework.permissions import AllowAny

class PublicClientListView(generics.ListAPIView):
    serializer_class = PublicClientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'uuid', 'county', 'sub_county']

    def get_queryset(self):
        return Client.objects.prefetch_related('enrollments__program').order_by('-created_at')

class PublicClientRetrieveView(generics.RetrieveAPIView):
    serializer_class = PublicClientSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Client.objects.prefetch_related('enrollments__program')
