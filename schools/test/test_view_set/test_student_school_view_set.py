from django.test import TestCase
from schools.views import StudentSchoolViewSet
from rest_framework.test import APIRequestFactory
from schools.models import Student, School


class StudentViewSetTestCase(TestCase):

    def setUp(self):
        self.school = School.objects.create(name="name", max_student=20)

    def test_get_student_by_school(self):
        """Test get a single of student where school was exit"""
        request = APIRequestFactory().get(f'school/{self.school.pk}/students/')
        student_detail = StudentSchoolViewSet.as_view({'get': 'retrieve'})
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        response = student_detail(request, pk=student.pk, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_list_student_by_school(self):
        """Test get a list of student where school was exit"""
        request = APIRequestFactory().get(f'school/{self.school.pk}/students/')
        student_detail = StudentSchoolViewSet.as_view({'get': 'list'})
        Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        response = student_detail(request, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 200)

    def test_create_student_by_school(self):
        """Test create a student where school was exit"""
        data = {"last_name": "lnamee", "first_name": "fnamee"}
        request = APIRequestFactory().post(f'school/{self.school.pk}/students/', data=data)
        student_detail = StudentSchoolViewSet.as_view({'post': 'create'})
        response = student_detail(request, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 201)

    def test_create_validate_max_students_school(self):
        """Test create a student with max student on the school"""
        school = School.objects.create(name="name", max_student=1)
        Student.objects.create(first_name="fname", last_name="lname", school=school)
        data = {"last_name": "lnamee", "first_name": "fnamee"}
        request = APIRequestFactory().post(f'school/{self.school.pk}/students/', data=data)
        student_detail = StudentSchoolViewSet.as_view({'post': 'create'})
        response = student_detail(request, schools_pk=school.pk)
        self.assertEqual(response.status_code, 409)

    def test_create_student_school_does_not_exit(self):
        """Test create a student with un exiting school"""
        data = {"last_name": "lnamee", "first_name": "fnamee"}
        request = APIRequestFactory().post("/students/", data=data)
        student_detail = StudentSchoolViewSet.as_view({'post': 'create'})
        response = student_detail(request, schools_pk=-1)
        self.assertEqual(response.status_code, 400)

    def test_update_student_by_school(self):
        """Test update a student"""
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        data = {"first_name": "Nameer", "last_name": "lnameeeee"}
        request = APIRequestFactory().put(f"school/{self.school.pk}/students/{student.pk}", data=data)
        student_detail = StudentSchoolViewSet.as_view({'put': 'update'})
        response = student_detail(request, pk=student.pk, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 200)

        updated_school = Student.objects.get()
        self.assertEqual(updated_school.first_name, "Nameer")
        self.assertEqual(updated_school.last_name, "lnameeeee")

    def test_patch_student_by_school(self):
        """Test patch a student where school was exit"""
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        data = {"first_name": "Nameer"}
        request = APIRequestFactory().put(f"school/{self.school.pk}/students/{student.pk}", data=data)
        student_detail = StudentSchoolViewSet.as_view({'put': 'partial_update'})
        response = student_detail(request, pk=student.pk, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 200)

        updated_school = Student.objects.get()
        self.assertEqual(updated_school.first_name, "Nameer")
        self.assertEqual(updated_school.last_name, "lname")

    def test_delete_student_by_school(self):
        """Test delete a student where school was exit"""
        student = Student.objects.create(first_name="fname", last_name="lname", school=self.school)
        request = APIRequestFactory().delete(f"school/{self.school.pk}/students/{student.pk}")
        student_detail = StudentSchoolViewSet.as_view({'delete': 'destroy'})
        response = student_detail(request, pk=student.pk, schools_pk=self.school.pk)
        self.assertEqual(response.status_code, 204)

        updated_student = Student.objects.all()
        self.assertEqual(updated_student.count(), 0)
