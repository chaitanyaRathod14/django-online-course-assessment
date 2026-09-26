# Online Course - Django Final Project

This project implements the assessment/exam functionality required for the Online Course final project.

## Features
- Course and Lesson models
- Question, Choice and Submission models
- Django admin configuration with QuestionInline and ChoiceInline
- Course details page with Bootstrap
- Mock exam page
- Exam submission and result evaluation
- Congratulations result page
- SQLite database with sample course, lesson and questions

## Run the project

### Windows
```powershell
cd onlinecourse_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Course: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

The sample course is available on the home page.

## GitHub submission files
- onlinecourse/models.py
- onlinecourse/admin.py
- onlinecourse/templates/onlinecourse/course_details_bootstrap.html
- onlinecourse/views.py
- onlinecourse/urls.py

## Screenshots
For Task 3, open `/admin/` and capture the page showing:
- Authentication and Authorization
- OnlineCourse

Save as `03-admin-site.png`.

For Task 7, take the successful exam result page showing:
- Congratulations
- Score
- Exam results

Save as `07-final.png`.
