from rest_framework import serializers
from .models import Program
from clients.serializers import ClientSerializer

class ProgramSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    id = serializers.CharField(read_only=True)

    
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_by', 'created_at']