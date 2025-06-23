from django.shortcuts import render
from .models import Schedule, Grade, Student
from collections import defaultdict

def get_schedule_with_grades(request):
    student = Student.objects.get(user=request.user)
    schedule = Schedule.objects.filter(student=student).order_by('day_of_week', 'time')
    grades = Grade.objects.filter(student=student)

    # Розклад по днях
    schedule_by_day = defaultdict(list)
    for item in schedule:
        schedule_by_day[item.day_of_week].append(item)

    # Оцінки: { 'Monday': { 'Math': [5,4], 'Physics': [3] }, ... }
    grades_by_day_subject = defaultdict(lambda: defaultdict(list))
    for grade in grades:
        day = grade.date.strftime("%A")
        grades_by_day_subject[day][grade.subject.name].append(str(grade.value))

    # Всі предмети для колонок у шаблоні
    all_subjects = sorted(set(g.subject.name for g in grades))

    # Середні бали
    subject_averages = {}
    total = 0
    count = 0
    for subject in all_subjects:
        subject_grades = [g.value for g in grades if g.subject.name == subject]
        avg = sum(subject_grades) / len(subject_grades)
        subject_averages[subject] = avg
        total += sum(subject_grades)
        count += len(subject_grades)

    total_average = total / count if count > 0 else 0

    # Впорядкування днів тижня
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule_by_day = {day: schedule_by_day[day] for day in ordered_days if day in schedule_by_day}
    grades_by_day_subject = {day: grades_by_day_subject[day] for day in ordered_days if day in grades_by_day_subject}

    context = {
        'student': student,
        'schedule_by_day': dict(schedule_by_day),
        'grades_by_day_subject': dict(grades_by_day_subject),
        'subject_averages': subject_averages,
        'total_average': total_average,
        'all_subjects': all_subjects,
    }

    return render(request, 'diary/schedule_with_grades.html', context)
