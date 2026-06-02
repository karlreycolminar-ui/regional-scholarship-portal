from rest_framework import serializers
from .models import Scholarship


class ScholarshipSerializer(serializers.ModelSerializer):
    is_open = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Scholarship
        fields = [
            'id', 'title', 'description', 'eligibility_criteria',
            'amount', 'slots', 'category', 'deadline',
            'is_active', 'is_open', 'days_remaining',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return 'System'

    def validate_deadline(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value


class ScholarshipListSerializer(serializers.ModelSerializer):
    is_open = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Scholarship
        fields = ['id', 'title', 'category', 'amount', 'slots',
                  'deadline', 'is_active', 'is_open', 'days_remaining']
