from rest_framework import serializers
from .models import Client
from datetime import date
from programs.models import Program


class ClientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField(read_only=True)
    programs = serializers.SerializerMethodField()
    
    # For writing relationships
    program_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Program.objects.all(),
        source='programs',
        write_only=True,
        required=False
    )

    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'age',
            'gender', 'phone_number', 'county', 'sub_county', 'programs', 'program_ids', 'created_by', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'age', 'programs']
        extra_kwargs = {
            'date_of_birth': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'gender': {'required': True},
            'phone_number': {'required': True},
            'county': {'required': True},
            'sub_county': {'required': True}

        }

    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < 
            (obj.date_of_birth.month, obj.date_of_birth.day)
        )

    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

    def validate_program_ids(self, value):
        # Ensure user owns the programs they're trying to assign
        user = self.context['request'].user
        for program in value:
            if program.created_by != user:
                raise serializers.ValidationError(
                    f"You don't have permission to assign program {program.id}"
                )
        return value
    
    def get_programs(self, obj):
        from programs.serializers import ProgramSerializer
        return ProgramSerializer(obj.programs.all(), many=True).data