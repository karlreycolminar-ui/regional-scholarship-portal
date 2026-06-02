from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2', 'phone', 'address', 'date_of_birth']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            message = "The two entries do not match."
            raise serializers.ValidationError({"password": message})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'applicant'
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Safe serializer - masks sensitive fields"""
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'address', 'date_of_birth',
            'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'role', 'is_verified', 'created_at']

    def get_email(self, obj):
        """Field-level masking for email"""
        request = self.context.get('request')
        if request and (request.user == obj or request.user.is_admin):
            return obj.email
        # Mask email for other users
        parts = obj.email.split('@')
        if len(parts) == 2:
            masked = parts[0][:2] + '***@' + parts[1]
            return masked
        return '***'


class UserAdminSerializer(serializers.ModelSerializer):
    """Full admin serializer - no masking"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'address', 'date_of_birth',
            'is_verified', 'is_active', 'created_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'last_login']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            message = "The two entries do not match."
            raise serializers.ValidationError({"new_password": message})
        return attrs
