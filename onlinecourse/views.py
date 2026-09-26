from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Question, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(
        request,
        "onlinecourse/course_list.html",
        {"courses": courses},
    )


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
        {
            "lesson": lesson,
            "questions": questions,
        },
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    lesson_id = request.POST.get("lesson_id")

    if lesson_id:
        lesson = get_object_or_404(
            Lesson,
            id=lesson_id,
            course=course,
        )
    else:
        lesson = course.lessons.first()

    if lesson is None:
        return redirect("course_details", course_id=course.id)

    questions = list(
        lesson.questions.prefetch_related("choices").all()
    )

    student_name = (
        request.POST.get("student_name", "Student").strip()
        or "Student"
    )

    score = 0
    total = sum(question.points for question in questions)

    first_submission = None

    for question in questions:
        selected_id = request.POST.get(
            f"question_{question.id}"
        )

        selected_choice = None

        if selected_id:
            selected_choice = question.choices.filter(
                id=selected_id
            ).first()

        is_correct = bool(
            selected_choice and selected_choice.is_correct
        )

        submission = Submission.objects.create(
            student_name=student_name,
            question=question,
            selected_choice=selected_choice,
            is_correct=is_correct,
        )

        if first_submission is None:
            first_submission = submission

        if is_correct:
            score += question.points

    if first_submission is None:
        return redirect("course_details", course_id=course.id)

    request.session["exam_result"] = {
        "course_id": course.id,
        "lesson_id": lesson.id,
        "submission_id": first_submission.id,
        "student_name": student_name,
        "score": score,
        "total": total,
    }

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=first_submission.id,
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        id=course_id,
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
    )

    lesson = submission.question.lesson

    submissions = Submission.objects.filter(
        student_name=submission.student_name,
        question__lesson=lesson,
    ).select_related(
        "question",
        "selected_choice",
    )

    total = sum(
        question.points
        for question in lesson.questions.all()
    )

    score = sum(
        item.question.points
        for item in submissions
        if item.is_correct
    )

    results = []

    for item in submissions:
        results.append(
            {
                "question": item.question,
                "selected_choice": item.selected_choice,
                "is_correct": item.is_correct,
                "correct_choice": item.question.choices.filter(
                    is_correct=True
                ).first(),
            }
        )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "lesson": lesson,
            "student_name": submission.student_name,
            "score": score,
            "total": total,
            "results": results,
        },
    )
