from django.test import TestCase
from schools.views import StudentViewSet
from rest_framework.test import APIRequestFactory
from schools.models import Student, School


class StudentViewSetTestCase(TestCase):

    def setUp(self):
        self.school = School.objects.create(name="name", max_student=20)

    def test_get_student(self):
        """Test get a single of student"""
        request = APIRequestFactory().get('/students/')
        student_detail = StudentViewSet.as_view({'get': 'retrieve'})
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        response = student_detail(request, pk=student.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_list_student(self):
        """Test get a list of student"""
        request = APIRequestFactory().get('/students/')
        student_detail = StudentViewSet.as_view({'get': 'list'})
        Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        response = student_detail(request)
        self.assertEqual(response.status_code, 200)

    def test_create_student(self):
        """Test create a student"""
        data = {"last_name": "lnamee", "first_name": "fnamee", "school": self.school.id}
        request = APIRequestFactory().post("/students/", data=data)
        student_detail = StudentViewSet.as_view({'post': 'create'})
        response = student_detail(request)
        self.assertEqual(response.status_code, 201)

    def test_create_validate_max_students_school(self):
        """Test create a student with max student on the school"""
        school = School.objects.create(name="name", max_student=1)
        Student.objects.create(first_name="fname", last_name="lname", school=school)
        data = {"last_name": "lnamee", "first_name": "fnamee", "school": school.id}
        request = APIRequestFactory().post("/students/", data=data)
        student_detail = StudentViewSet.as_view({'post': 'create'})
        response = student_detail(request)
        self.assertEqual(response.status_code, 409)

    def test_update_student(self):
        """Test update a student"""
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        data = {"first_name": "Nameer", "last_name": "lnameeeee", "school": self.school.pk}
        request = APIRequestFactory().put(f"/students/{student.pk}", data=data)
        student_detail = StudentViewSet.as_view({'put': 'update'})
        response = student_detail(request, pk=student.pk)
        self.assertEqual(response.status_code, 200)

        updated_school = Student.objects.get()
        self.assertEqual(updated_school.first_name, "Nameer")
        self.assertEqual(updated_school.last_name, "lnameeeee")

    def test_delete_student(self):
        """Test delete a student"""
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        request = APIRequestFactory().delete(f"/students/{student.pk}")
        student_detail = StudentViewSet.as_view({'delete': 'destroy'})
        response = student_detail(request, pk=student.pk)
        self.assertEqual(response.status_code, 204)

        updated_student = Student.objects.all()
        self.assertEqual(updated_student.count(), 0)
