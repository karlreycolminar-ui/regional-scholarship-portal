from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import Application, Document
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer,
    DocumentSerializer, ReviewDecisionSerializer
)
from accounts.permissions import IsApplicant, IsReviewerOrAdmin, IsAdminUser, IsOwnerOrAdmin
from audits.utils import log_action


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    """GET own apps (applicant) / POST new application"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ApplicationCreateSerializer
        return ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_reviewer:
            qs = Application.objects.all().select_related('user', 'scholarship')
            status_filter = self.request.query_params.get('status')
            if status_filter:
                qs = qs.filter(status=status_filter)
            return qs
        # Anti-IDOR: applicants only see their own
        return Application.objects.filter(user=user).select_related('scholarship')

    def perform_create(self, serializer):
        if not self.request.user.is_applicant:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only applicants can submit applications.")
        app = serializer.save(user=self.request.user)
        log_action(self.request.user, 'API_APPLICATION_SUBMITTED', f'Applied for: {app.scholarship.title}')

    def get_serializer_context(self):
        return {'request': self.request}


class ApplicationDetailAPIView(generics.RetrieveDestroyAPIView):
    """GET/DELETE specific application"""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_reviewer:
            return Application.objects.all()
        # Anti-IDOR enforcement
        return Application.objects.filter(user=user)

    def perform_destroy(self, instance):
        if instance.status != 'pending':
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Only pending applications can be withdrawn.")
        log_action(self.request.user, 'API_APPLICATION_WITHDRAWN', f'Withdrew app #{instance.id}')
        instance.delete()


class ReviewDecisionAPIView(APIView):
    """POST /api/applications/<id>/review/"""
    permission_classes = [IsReviewerOrAdmin]

    def post(self, request, pk):
        application = generics.get_object_or_404(Application, pk=pk)
        serializer = ReviewDecisionSerializer(data=request.data)
        if serializer.is_valid():
            application.status = serializer.validated_data['decision']
            application.review_notes = serializer.validated_data.get('review_notes', '')
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            log_action(request.user, 'API_APPLICATION_REVIEWED',
                       f'Reviewed App #{pk}: {application.status}')
            return Response({
                'message': f'Application {application.status}.',
                'application_id': pk,
                'status': application.status
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadAPIView(generics.CreateAPIView):
    """POST /api/applications/<id>/documents/"""
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        application = generics.get_object_or_404(Application, pk=self.kwargs['pk'])
        # Anti-IDOR: only owner can upload to their application
        if application.user != self.request.user and not self.request.user.is_admin:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot upload documents to this application.")
        doc = serializer.save(
            application=application,
            original_filename=serializer.validated_data['file'].name
        )
        log_action(self.request.user, 'DOCUMENT_UPLOADED',
                   f'Uploaded {doc.get_file_type_display()} for App #{application.id}')


class AdminApplicationListAPIView(generics.ListAPIView):
    """GET /api/admin/applications/ - full list for admin"""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Application.objects.all().select_related('user', 'scholarship', 'reviewed_by')
        status_f = self.request.query_params.get('status')
        scholarship_f = self.request.query_params.get('scholarship')
        if status_f:
            qs = qs.filter(status=status_f)
        if scholarship_f:
            qs = qs.filter(scholarship_id=scholarship_f)
        return qs
