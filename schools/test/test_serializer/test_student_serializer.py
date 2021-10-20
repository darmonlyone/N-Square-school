from django.test import TestCase
from schools.serializer import StudentSerializer, SchoolSerializer
from schools.models import School


class StudentSerializerTestCase(TestCase):

    def setUp(self):
        school_data = {"name": "Name", "max_student": 20}
        serializer = SchoolSerializer(data=school_data)
        if serializer.is_valid():
            serializer.save()
        self.school = School.objects.get()

    def test_validate_student_serializer(self):
        """Test validate with correct student field and check weather its generate student_id"""
        student = {"school": self.school.id, "first_name": "firstname", "last_name": "lastname"}
        serializer = StudentSerializer(data=student)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(len(str(serializer.data['student_id'])) > 0)

    def test_validate_school_serializer_missing_field(self):
        """Test validate with incorrect missing field"""
        student = {"school": self.school.id}
        serializer = StudentSerializer(data=student)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'last_name', 'first_name'})

