"""
Management command to create demo data for the scholarship portal.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from scholarships.models import Scholarship


class Command(BaseCommand):
    help = 'Seeds the database with demo users and scholarships'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        # Create superuser / admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@scholarportal.ph',
                password='Admin@1234',  # nosec B106
                first_name='System',
                last_name='Administrator',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('✅ Admin user created (admin / Admin@1234)'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write('ℹ️  Admin already exists')

        # Create reviewer
        if not User.objects.filter(username='reviewer1').exists():
            User.objects.create_user(
                username='reviewer1',
                email='reviewer@scholarportal.ph',
                password='Reviewer@1234',  # nosec B106
                first_name='Maria',
                last_name='Santos',
                role='reviewer',
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS('✅ Reviewer created (reviewer1 / Reviewer@1234)'))

        # Create applicants
        applicants_data = [
            ('juan.dela.cruz', 'Juan', 'Dela Cruz', 'juan@example.com'),
            ('maria.reyes', 'Maria', 'Reyes', 'maria@example.com'),
            ('pedro.garcia', 'Pedro', 'Garcia', 'pedro@example.com'),
        ]
        for username, fname, lname, email in applicants_data:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='Applicant@1234',  # nosec B106
                    first_name=fname,
                    last_name=lname,
                    role='applicant',
                    is_verified=True,
                )
        self.stdout.write(self.style.SUCCESS('✅ Applicants created (password: Applicant@1234)'))

        # Create scholarships
        scholarships = [
            {
                'title': 'EVSU Academic Excellence Scholarship',
                'description': 'A scholarship for outstanding students who demonstrate academic excellence and leadership.',
                'eligibility_criteria': '• Must be a Filipino citizen\n• Minimum GPA of 3.5\n• Must be enrolled in EVSU\n• No failing grades in previous semester\n• Must submit two letters of recommendation',
                'amount': 15000.00,
                'slots': 10,
                'category': 'merit',
                'deadline': timezone.now() + timedelta(days=30),
            },
            {
                'title': 'Regional STEM Scholarship Program',
                'description': 'Supporting future scientists, engineers, and technology leaders in Eastern Visayas.',
                'eligibility_criteria': '• Enrolled in STEM-related course\n• Minimum GPA of 3.2\n• Must be in 2nd year or higher\n• Financial need preferred',
                'amount': 20000.00,
                'slots': 5,
                'category': 'stem',
                'deadline': timezone.now() + timedelta(days=45),
            },
            {
                'title': 'Indigent Student Financial Assistance',
                'description': 'Financial support for deserving students from low-income families.',
                'eligibility_criteria': '• Family monthly income below ₱15,000\n• Must provide income certificate\n• Any course\n• Minimum GPA of 2.5',
                'amount': 10000.00,
                'slots': 20,
                'category': 'need',
                'deadline': timezone.now() + timedelta(days=60),
            },
            {
                'title': 'Athletes Scholarship Grant',
                'description': 'For student athletes who excel in regional and national competitions.',
                'eligibility_criteria': '• Must be an active varsity athlete\n• Must have competed in regional or national level\n• Minimum GPA of 2.0\n• Good moral character certificate required',
                'amount': 12000.00,
                'slots': 8,
                'category': 'sports',
                'deadline': timezone.now() + timedelta(days=20),
            },
        ]
        for data in scholarships:
            if not Scholarship.objects.filter(title=data['title']).exists():
                Scholarship.objects.create(created_by=admin, is_active=True, **data)
        self.stdout.write(self.style.SUCCESS(f'✅ {len(scholarships)} scholarships created'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write('\nDemo credentials:')
        self.stdout.write('  Admin:    admin / Admin@1234')
        self.stdout.write('  Reviewer: reviewer1 / Reviewer@1234')
        self.stdout.write('  Applicant: juan.dela.cruz / Applicant@1234')
