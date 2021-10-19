from rest_framework.serializers import ModelSerializer, UUIDField, ReadOnlyField
from .models import School, Student


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    student_id = ReadOnlyField()

    class Meta:
        model = Student
        fields = '__all__'


class StudentSerializerWithoutSchoolField(ModelSerializer):
    student_id = ReadOnlyField()

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id')
