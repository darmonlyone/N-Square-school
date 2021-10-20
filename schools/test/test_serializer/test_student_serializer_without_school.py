from django.test import TestCase
from schools.serializer import StudentSerializerWithoutSchoolField, SchoolSerializer, StudentSerializer


class SchoolSerializerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        school = {"name": "Name", "max_student": 20}
        serializer = SchoolSerializer(data=school)
        if serializer.is_valid():
            serializer.save()

    def test_validate_student_serializer(self):
        student = {'last_name': "b", 'first_name': "a"}
        serializer = StudentSerializerWithoutSchoolField(data=student)
        self.assertTrue(serializer.is_valid())

    def test_validate_school_serializer_missing_field(self):
        school = {'last_name': "lastname"}
        serializer = StudentSerializerWithoutSchoolField(data=school)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'first_name'})

    @classmethod
    def tearDownClass(cls):
        pass
