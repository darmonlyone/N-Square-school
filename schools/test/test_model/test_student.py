import unittest
from django.test import TestCase
from schools.models import Student, School


class StudentTestCase(TestCase):

    def setUp(self):
        self.school = School.objects.create(name="Test Name", max_student=30)
        self.school2 = School.objects.create(name="Test Name 2", max_student=20)
        Student.objects.create(school=self.school, first_name="Name 1", last_name="Last 1")
        Student.objects.create(school=self.school, first_name="Name 2", last_name="Last 2")
        Student.objects.create(school=self.school, first_name="Name 3", last_name="Last 3")
        Student.objects.create(school=self.school2, first_name="Name 4", last_name="Last 4")

    def test_create_school(self):
        """Test amount of set up school are create correctly"""
        schools = School.objects.all()
        self.assertEqual(schools.count(), 2)

    def test_create_student(self):
        """Test amount of set up student are create correctly"""
        students = Student.objects.all()
        self.assertEqual(students.count(), 4)

    @unittest.expectedFailure
    def test_create_student_with_first_name_exceed_20_char(self):
        """Test create school with first_name more than 20 character"""
        Student.objects.create(school=self.school, first_name="123456789012345678901", last_name="Last 5")

    @unittest.expectedFailure
    def test_create_student_with_last_name_exceed_20_char(self):
        """Test create school with last_name more than 20 character"""
        Student.objects.create(school=self.school, first_name="name", last_name="123456789012345678901")

    def test_student_id_are_generated(self):
        """Test student id are generated after create"""
        students = Student.objects.all()
        for student in students:
            self.assertTrue(len(student.student_id) > 0)

    def test_get_student(self):
        """Test get the student"""
        student = Student.objects.get(first_name="Name 1")
        self.assertEqual(student.first_name, "Name 1")
        self.assertEqual(student.last_name, "Last 1")
        self.assertEqual(student.school, self.school)

    def test_update_student(self):
        """Test update the student"""
        student = Student.objects.get(first_name="Name 1")
        student.first_name = "Tester"
        student.school = self.school2
        student.save()
        self.assertEqual(student.first_name, "Tester")
        self.assertEqual(student.school, self.school2)

    def test_delete_school(self):
        """Test delete the student"""
        student = Student.objects.get(first_name="Name 2")
        student.delete()
        students = Student.objects.all()
        self.assertEqual(students.count(), 3)
