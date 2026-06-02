from rest_framework import serializers
from .models import Application, Document
from scholarships.serializers import ScholarshipListSerializer


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'file_type', 'original_filename', 'uploaded_at']
        read_only_fields = ['id', 'original_filename', 'uploaded_at']

    def validate_file(self, value):
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if hasattr(value, 'content_type') and value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must not exceed 10MB.")
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    scholarship_detail = ScholarshipListSerializer(source='scholarship', read_only=True)
    applicant_name = serializers.SerializerMethodField()
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id', 'user', 'scholarship', 'scholarship_detail',
            'status', 'gpa', 'school_name', 'year_level', 'course', 'essay',
            'reviewed_by', 'review_notes', 'reviewed_at',
            'date_submitted', 'updated_at',
            'documents', 'applicant_name', 'reviewer_name'
        ]
        read_only_fields = ['id', 'user', 'status', 'reviewed_by', 'reviewed_at', 'date_submitted', 'updated_at']

    def get_applicant_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_reviewer_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name() or obj.reviewed_by.username
        return None

    def validate_scholarship(self, value):
        from django.utils import timezone
        if not value.is_active or value.deadline <= timezone.now():
            raise serializers.ValidationError("This scholarship is no longer accepting applications.")
        return value


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['scholarship', 'gpa', 'school_name', 'year_level', 'course', 'essay']

    def validate_scholarship(self, value):
        from django.utils import timezone
        if not value.is_active or value.deadline <= timezone.now():
            raise serializers.ValidationError("This scholarship is closed.")
        request = self.context.get('request')
        if request and Application.objects.filter(user=request.user, scholarship=value).exists():
            raise serializers.ValidationError("You have already applied for this scholarship.")
        return value


class ReviewDecisionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=['approved', 'rejected', 'under_review'])
    review_notes = serializers.CharField(required=False, allow_blank=True)
