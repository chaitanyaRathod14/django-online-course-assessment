from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice


class Command(BaseCommand):
    help = "Create demo course, lesson, questions and choices."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Python and Django Fundamentals",
            defaults={
                "description": (
                    "Learn Python fundamentals and build web applications "
                    "with Django."
                )
            },
        )

        lesson, _ = Lesson.objects.get_or_create(
            course=course,
            title="Django Assessment",
            defaults={
                "content": "Test your understanding of Django basics.",
                "order": 1,
            },
        )

        questions = [
            (
                "Which file normally contains Django URL patterns?",
                [
                    ("urls.py", True),
                    ("models.py", False),
                    ("admin.py", False),
                    ("settings.css", False),
                ],
            ),
            (
                "Which command starts the Django development server?",
                [
                    ("python manage.py runserver", True),
                    ("python manage.py startserver", False),
                    ("django start", False),
                    ("python server.py", False),
                ],
            ),
            (
                "Which Django component is used to define database tables?",
                [
                    ("Models", True),
                    ("Templates", False),
                    ("URLs", False),
                    ("Static files", False),
                ],
            ),
            (
                "Which template language is commonly used by Django templates?",
                [
                    ("Django Template Language", True),
                    ("SQL Template Language", False),
                    ("C++ Templates", False),
                    ("Java Template Language", False),
                ],
            ),
            (
                "Which command creates migration files from model changes?",
                [
                    ("python manage.py makemigrations", True),
                    ("python manage.py makechanges", False),
                    ("python manage.py migratefiles", False),
                    ("python manage.py buildmodels", False),
                ],
            ),
        ]

        for text, choices in questions:
            question, _ = Question.objects.get_or_create(
                lesson=lesson,
                text=text,
                defaults={"points": 1},
            )
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(
                    question=question,
                    text=choice_text,
                    defaults={"is_correct": is_correct},
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created. Course ID: %s, Lesson ID: %s"
                % (course.id, lesson.id)
            )
        )
