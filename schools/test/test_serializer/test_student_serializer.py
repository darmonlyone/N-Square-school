from django.test import TestCase
from schools.serializer import StudentSerializer, SchoolSerializer


class SchoolSerializerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        school = {"name": "Name", "max_student": 20}
        serializer = SchoolSerializer(data=school)
        if serializer.is_valid():
            serializer.save()

    def test_validate_student_serializer(self):
        student = {"school": 1, "first_name": "firstname", "last_name": "lastname"}
        serializer = StudentSerializer(data=student)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(len(str(serializer.data['student_id'])) > 0)

    def test_validate_school_serializer_missing_field(self):
        student = {"school": 1}
        serializer = StudentSerializer(data=student)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'last_name', 'first_name'})

    @classmethod
    def tearDownClass(cls):
        pass
