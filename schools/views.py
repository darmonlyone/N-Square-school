from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import School, Student
from .serializer import SchoolSerializer, StudentSerializer, StudentSerializerWithoutSchoolField
from rest_framework.response import Response


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Override method create to validate maximum student of the school
        """
        if 'school' in request.data:
            student = Student.objects.filter(school_id=request.data['school'])
            try:
                student_school = School.objects.get(id=request.data['school'])
            except School.DoesNotExist:
                return Response("School does not exit", status=status.HTTP_400_BAD_REQUEST)

            if student.count() >= student_school.max_student:
                return Response("Maximum number of student reached", status=status.HTTP_409_CONFLICT)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSchoolViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = StudentSerializerWithoutSchoolField

        return serializer_class

    def get_queryset(self):
        return Student.objects.filter(school=self.kwargs['schools_pk'])

    def create(self, request, *args, **kwargs):
        """
        Override method create to validate maximum student of the school
        """
        if 'schools_pk' in kwargs:
            student = self.get_queryset()
            try:
                student_school = School.objects.get(id=kwargs['schools_pk'])
            except School.DoesNotExist:
                return Response("School does not exit", status=status.HTTP_400_BAD_REQUEST)

            if student.count() >= student_school.max_student:
                return Response("Maximum number of student reached", status=status.HTTP_409_CONFLICT)

            if '_mutable' is request.data:
                # unmutable before add school data
                _mutable = request.data._mutable
                request.data._mutable = True

            request.data.update({'school': student_school.id})

            if '_mutable' in request.data:
                # set mutable back after set data
                request.data._mutable = _mutable

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
