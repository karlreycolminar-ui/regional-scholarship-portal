from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Application, Document
from .forms import ApplicationForm, DocumentUploadForm, ReviewForm
from scholarships.models import Scholarship
from audits.utils import log_action


def applicant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_applicant:
            return HttpResponseForbidden('Only applicants can access this.')
        return view_func(request, *args, **kwargs)
    return wrapper


def reviewer_or_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_reviewer or request.user.is_admin):
            return HttpResponseForbidden('Access denied.')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@applicant_required
def apply_view(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, pk=scholarship_id)

    if not scholarship.is_open:
        messages.error(request, 'This scholarship is no longer accepting applications.')
        return redirect('scholarship_detail', pk=scholarship_id)

    if Application.objects.filter(user=request.user, scholarship=scholarship).exists():
        messages.warning(request, 'You have already applied for this scholarship.')
        return redirect('my_applications')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        doc_form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.scholarship = scholarship
            application.save()

            # Handle document uploads (multiple)
            files = request.FILES.getlist('file')
            file_types = request.POST.getlist('file_type')
            for i, f in enumerate(files):
                ft = file_types[i] if i < len(file_types) else 'other'
                Document.objects.create(application=application, file=f, file_type=ft)

            log_action(request.user, 'APPLICATION_SUBMITTED',
                       f'Applied for: {scholarship.title} (App #{application.id})')
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
        doc_form = DocumentUploadForm()

    return render(request, 'applications/apply.html', {
        'form': form,
        'doc_form': doc_form,
        'scholarship': scholarship,
    })


@login_required
@applicant_required
def my_applications(request):
    # Anti-IDOR: only return logged-in user's applications
    applications = Application.objects.filter(user=request.user).select_related('scholarship')
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'applications/my_applications.html', {
        'applications': applications,
        'status_filter': status_filter,
    })


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    # Anti-IDOR enforcement
    if not (request.user.is_admin or request.user.is_reviewer or application.user == request.user):
        return HttpResponseForbidden('You do not have permission to view this application.')
    return render(request, 'applications/detail.html', {'application': application})


@login_required
@reviewer_or_admin
def review_list(request):
    applications = Application.objects.select_related('user', 'scholarship').all()
    status_filter = request.GET.get('status', 'pending')
    if status_filter:
        applications = applications.filter(status=status_filter)
    scholarship_filter = request.GET.get('scholarship', '')
    if scholarship_filter:
        applications = applications.filter(scholarship_id=scholarship_filter)
    return render(request, 'applications/review_list.html', {
        'applications': applications,
        'status_filter': status_filter,
        'scholarship_filter': scholarship_filter,
        'scholarships': Scholarship.objects.all(),
    })


@login_required
@reviewer_or_admin
def review_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
            log_action(request.user, 'APPLICATION_REVIEWED',
                       f'Reviewed App #{application.id}: {app.status}')
            messages.success(request, f'Application marked as {app.get_status_display()}.')
            return redirect('review_list')
    else:
        form = ReviewForm(instance=application)
    return render(request, 'applications/review.html', {
        'application': application,
        'form': form,
    })


@login_required
def application_withdraw(request, pk):
    application = get_object_or_404(Application, pk=pk, user=request.user)
    if application.status != 'pending':
        messages.error(request, 'Only pending applications can be withdrawn.')
        return redirect('my_applications')
    if request.method == 'POST':
        scholarship_title = application.scholarship.title
        application.delete()
        log_action(request.user, 'APPLICATION_WITHDRAWN', f'Withdrew application for: {scholarship_title}')
        messages.success(request, 'Application withdrawn.')
        return redirect('my_applications')
    return render(request, 'applications/confirm_withdraw.html', {'application': application})
