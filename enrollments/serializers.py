from rest_framework import serializers
from .models import Enrollment
from clients.serializers import ClientSerializer
from programs.serializers import ProgramSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    client_details = ClientSerializer(source='client', read_only=True)
    program_details = ProgramSerializer(source='program', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'client', 'program', 'status', 'enrollment_date',
            'completed_date', 'notes', 'client_details', 'program_details'
        ]
        read_only_fields = ['id', 'enrolled_by', 'enrollment_date']
        extra_kwargs = {
            'client': {'write_only': True},
            'program': {'write_only': True}
        }

    def validate(self, data):
        """
        Ensure client and program belong to requesting user
        """
        user = self.context['request'].user
        if data['client'].created_by != user:
            raise serializers.ValidationError("You don't own this client")
        if data['program'].created_by != user:
            raise serializers.ValidationError("You don't own this program")
        return data