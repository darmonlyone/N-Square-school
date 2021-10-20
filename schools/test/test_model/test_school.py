import unittest
from django.test import TestCase
from schools.models import School


class SchoolTestCase(TestCase):

    def setUp(self):
        School.objects.create(name="Test Name", max_student=30)
        School.objects.create(name="Test Name 2", max_student=20)
        School.objects.create(name="Test Name 3", max_student=10)

    def test_create_school(self):
        """Test amount of set up school are create correctly"""
        schools = School.objects.all()
        self.assertEqual(schools.count(), 3)

    @unittest.expectedFailure
    def test_create_school_with_name_exceed_20_char(self):
        """Test create school with name more than 20 character"""
        School.objects.create(name="123456789012345678901", max_student=30)

    def test_get_school(self):
        """Test get the school"""
        school = School.objects.get(name="Test Name")
        self.assertEqual("Test Name", school.name)
        self.assertEqual(school.max_student, 30)

    def test_update_school(self):
        """Test update the school"""
        school = School.objects.get(name="Test Name")
        school.name = "New Name"
        school.max_student = 10
        school.save()
        self.assertEqual(school.name, "New Name")
        self.assertEqual(school.max_student, 10)

    def test_delete_school(self):
        """Test delete the school"""
        school = School.objects.get(name="Test Name")
        school.delete()
        schools = School.objects.all()
        self.assertEqual(schools.count(), 2)
