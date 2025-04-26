from rest_framework import serializers
from .models import Client
from datetime import date
from programs.models import Program
from enrollments.models import Enrollment

class ProgramWithEnrollmentSerializer(serializers.Serializer):
    uuid = serializers.CharField(source='program.uuid')
    name = serializers.CharField(source='program.name')
    description = serializers.CharField(source='program.description')
    status = serializers.CharField(source='program.status')
    enrolled_at = serializers.DateTimeField()

class ClientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'uuid', 
            'first_name', 
            'last_name', 
            'dob', 
            'phone_number', 
            'county', 
            'sub_county',
            'gender', 
            'age', 
            'programs', 
            'created_at', 
            'created_by'
        ]
        read_only_fields = ('uuid', 'created_by', 'created_at', 'age', 'programs')

    def get_age(self, obj):
        today = date.today()
        if obj.dob:
            return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))
        return None

    def get_created_by(self, obj):
        return obj.created_by.email if obj.created_by else None

    def get_programs(self, obj):
        enrollments = obj.enrollments.select_related('program')
        return ProgramWithEnrollmentSerializer(enrollments, many=True).data
