from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Scholarship
from .forms import ScholarshipForm
from audits.utils import log_action


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponseForbidden('Access denied.')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def scholarship_list(request):
    scholarships = Scholarship.objects.filter(is_active=True).order_by('deadline')
    category = request.GET.get('category', '')
    if category:
        scholarships = scholarships.filter(category=category)
    search = request.GET.get('q', '')
    if search:
        scholarships = scholarships.filter(title__icontains=search)
    return render(request, 'scholarships/list.html', {
        'scholarships': scholarships,
        'category': category,
        'search': search,
        'categories': Scholarship.CATEGORY_CHOICES,
    })


@login_required
def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    from applications.models import Application
    already_applied = False
    if request.user.is_applicant:
        already_applied = Application.objects.filter(
            user=request.user, scholarship=scholarship
        ).exists()
    return render(request, 'scholarships/detail.html', {
        'scholarship': scholarship,
        'already_applied': already_applied,
    })


@login_required
@admin_required
def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            scholarship = form.save(commit=False)
            scholarship.created_by = request.user
            scholarship.save()
            log_action(request.user, 'SCHOLARSHIP_CREATED', f'Created scholarship: {scholarship.title}')
            messages.success(request, f'Scholarship "{scholarship.title}" created.')
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'scholarships/form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def scholarship_edit(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            log_action(request.user, 'SCHOLARSHIP_UPDATED', f'Updated scholarship: {scholarship.title}')
            messages.success(request, f'Scholarship updated.')
            return redirect('scholarship_list')
    else:
        form = ScholarshipForm(instance=scholarship)
    return render(request, 'scholarships/form.html', {'form': form, 'action': 'Edit', 'scholarship': scholarship})


@login_required
@admin_required
def scholarship_delete(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        title = scholarship.title
        scholarship.delete()
        log_action(request.user, 'SCHOLARSHIP_DELETED', f'Deleted scholarship: {title}')
        messages.success(request, f'Scholarship deleted.')
        return redirect('scholarship_list')
    return render(request, 'scholarships/confirm_delete.html', {'scholarship': scholarship})
