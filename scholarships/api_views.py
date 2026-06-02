from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Scholarship
from .serializers import ScholarshipSerializer, ScholarshipListSerializer
from accounts.permissions import IsAdminUser
from audits.utils import log_action


class ScholarshipListAPIView(generics.ListAPIView):
    """GET /api/scholarships/"""
    serializer_class = ScholarshipListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['deadline', 'created_at', 'amount']

    def get_queryset(self):
        queryset = Scholarship.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class ScholarshipDetailAPIView(generics.RetrieveAPIView):
    """GET /api/scholarships/<id>/"""
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticated]


class ScholarshipCreateAPIView(generics.CreateAPIView):
    """POST /api/scholarships/create/"""
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        scholarship = serializer.save(created_by=self.request.user)
        log_action(self.request.user, 'API_SCHOLARSHIP_CREATED', f'Created: {scholarship.title}')


class ScholarshipUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """PUT/PATCH/DELETE /api/scholarships/<id>/manage/"""
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        scholarship = serializer.save()
        log_action(self.request.user, 'API_SCHOLARSHIP_UPDATED', f'Updated: {scholarship.title}')

    def perform_destroy(self, instance):
        log_action(self.request.user, 'API_SCHOLARSHIP_DELETED', f'Deleted: {instance.title}')
        instance.delete()
