import uuid
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=20)
    max_student = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student_id = models.CharField(default=uuid.uuid4, max_length=36, editable=False, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name + self.last_name
