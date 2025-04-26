from rest_framework import serializers
from .models import Program
from clients.models import Client
from enrollments.models import Enrollment


class ClientMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['uuid', 'first_name', 'last_name', 'dob', 'phone_number', 'county', 'sub_county', 'gender', 'created_at']

class ProgramSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    clients = serializers.SerializerMethodField()
    total_enrolled_clients = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            'uuid',
            'name',
            'description',
            'status',
            'created_at',
            'created_by',
            'clients',             
            'total_enrolled_clients'  
        ]
        read_only_fields = ('uuid', 'created_by', 'created_at', 'clients', 'total_enrolled_clients')

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None
    
    
    def get_clients(self, obj):
        enrollments = obj.enrollments.select_related('client')
        clients = [enrollment.client for enrollment in enrollments]
        return ClientMiniSerializer(clients, many=True).data
    

    def get_total_enrolled_clients(self, obj):
        return obj.enrollments.count()