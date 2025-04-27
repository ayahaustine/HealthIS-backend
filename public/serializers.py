from rest_framework import serializers
from clients.models import Client
from enrollments.models import Enrollment
from programs.models import Program

class PublicProgramEnrollmentSerializer(serializers.Serializer):
    name = serializers.CharField(source='program.name')
    description = serializers.CharField(source='program.description')
    enrolled_at = serializers.DateTimeField()

class PublicClientSerializer(serializers.ModelSerializer):
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'uuid', 'first_name', 'last_name', 'dob',
            'county', 'sub_county', 'gender', 'created_at', 'programs'
        ]

    def get_programs(self, obj):
        enrollments = obj.enrollments.select_related('program').all()
        return PublicProgramEnrollmentSerializer(enrollments, many=True).data
