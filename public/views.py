from rest_framework import generics, filters
from clients.models import Client
from public.serializers import PublicClientSerializer
from rest_framework.permissions import AllowAny

class PublicClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = PublicClientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'uuid', 'county', 'sub_county']

class PublicClientRetrieveView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = PublicClientSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
