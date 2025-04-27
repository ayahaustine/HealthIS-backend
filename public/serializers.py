from rest_framework import serializers
from clients.models import Client
from enrollments.models import Enrollment
from programs.models import Program

class PublicProgramMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['name', 'description']

class PublicClientSerializer(serializers.ModelSerializer):
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'uuid', 'first_name', 'last_name', 'dob',
            'county', 'sub_county', 'gender', 'created_at', 'programs'
        ]

    def get_programs(self, obj):
        enrollments = obj.enrollments.select_related('program')
        programs = [enrollment.program for enrollment in enrollments]
        return PublicProgramMiniSerializer(programs, many=True).data
