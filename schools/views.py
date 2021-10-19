from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import School, Student
from .serializer import SchoolSerializer, StudentSerializer
from rest_framework.response import Response


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def create(self, request, *args, **kwargs):
        schools = School.objects.all()
        max_student_of_school = School.objects.get(id=request.data['school'])

        if schools.count() >= max_student_of_school.max_student:
            return Response("Maximum number of student reached", status=status.HTTP_409_CONFLICT)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class StudentSchoolViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_queryset(self):
        return Student.objects.filter(school=self.kwargs['schools_pk'])

    def create(self, request, *args, **kwargs):
        schools = School.objects.all()
        max_student_of_school = School.objects.get(id=kwargs['schools_pk'])
        request.data['school'] = kwargs['schools_pk']

        if schools.count() >= max_student_of_school.max_student:
            return Response("Maximum number of student reached", status=status.HTTP_409_CONFLICT)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
