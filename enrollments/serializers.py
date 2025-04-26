from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    program_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['uuid', 'client', 'program', 'enrolled_at', 'client_name', 'program_name']
        read_only_fields = ('uuid', 'enrolled_at', 'client_name', 'program_name')

    def get_client_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"

    def get_program_name(self, obj):
        return obj.program.name
    
    def validate(self, attrs):
        request = self.context['request']
        client = attrs.get('client')
        
        # Make sure the client belongs to the current user
        if client.created_by != request.user:
            raise serializers.ValidationError("You can only enroll clients you created.")

        return attrs