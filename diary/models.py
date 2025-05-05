from django.db import models
from django.conf import settings

DAYS_OF_WEEK = [
    ('Monday', 'Понеділок'),
    ('Tuesday', 'Вівторок'),
    ('Wednesday', 'Середа'),
    ('Thursday', 'Четвер'),
    ('Friday', 'Пʼятниця'),
]

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name if full_name else self.user.username

class Schedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    time = models.TimeField()

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.day_of_week} {self.time})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.value}"
