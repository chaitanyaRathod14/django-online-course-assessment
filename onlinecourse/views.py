from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Lesson, Question, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


def exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.prefetch_related("choices").all()
    return render(
        request,
        "onlinecourse/exam.html",
        {"lesson": lesson, "questions": questions},
    )


def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method != "POST":
        return redirect("exam", lesson_id=lesson.id)

    questions = list(lesson.questions.prefetch_related("choices").all())
    student_name = request.POST.get("student_name", "Student").strip() or "Student"

    score = 0
    total = sum(question.points for question in questions)
    results = []

    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected_choice = None

        if selected_id:
            selected_choice = question.choices.filter(id=selected_id).first()

        is_correct = bool(selected_choice and selected_choice.is_correct)

        Submission.objects.create(
            student_name=student_name,
            question=question,
            selected_choice=selected_choice,
            is_correct=is_correct,
        )

        if is_correct:
            score += question.points

        results.append(
            {
                "question": question,
                "selected_choice": selected_choice,
                "is_correct": is_correct,
                "correct_choice": question.choices.filter(is_correct=True).first(),
            }
        )

    request.session["exam_result"] = {
        "lesson_id": lesson.id,
        "student_name": student_name,
        "score": score,
        "total": total,
    }

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "lesson": lesson,
            "student_name": student_name,
            "score": score,
            "total": total,
            "results": results,
        },
    )


def show_exam_result(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    submissions = Submission.objects.filter(
        student_name=request.session.get("exam_result", {}).get(
            "student_name", "Student"
        ),
        question__lesson=lesson,
    ).select_related("question", "selected_choice")

    total = sum(question.points for question in lesson.questions.all())
    score = sum(s.question.points for s in submissions if s.is_correct)

    results = []
    for submission in submissions:
        results.append(
            {
                "question": submission.question,
                "selected_choice": submission.selected_choice,
                "is_correct": submission.is_correct,
                "correct_choice": submission.question.choices.filter(
                    is_correct=True
                ).first(),
            }
        )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "lesson": lesson,
            "student_name": request.session.get("exam_result", {}).get(
                "student_name", "Student"
            ),
            "score": score,
            "total": total,
            "results": results,
        },
    )
