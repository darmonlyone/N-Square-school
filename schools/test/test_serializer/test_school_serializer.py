from django.test import TestCase
from schools.serializer import SchoolSerializer


class SchoolSerializerTestCase(TestCase):

    def test_validate_school_serializer(self):
        """Test validate serializer with correct field"""
        school = {"name": "Name", "max_student": 20}
        serializer = SchoolSerializer(data=school)
        self.assertTrue(serializer.is_valid())

    def test_validate_school_serializer_missing_max_student(self):
        """Test validate serializer with correct value missing max student"""
        school = {"name": "Name"}
        serializer = SchoolSerializer(data=school)
        self.assertTrue(serializer.is_valid())

    def test_validate_school_serializer_missing_name(self):
        """Test validate serializer with missing field name"""
        school = {"max_student": 20}
        serializer = SchoolSerializer(data=school)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'name'})
