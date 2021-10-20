from django.test import TestCase
from schools.views import SchoolViewSet
from rest_framework.test import APIRequestFactory
from schools.models import School


class SchoolViewSetTestCase(TestCase):

    def test_get_school(self):
        """Test get single school"""
        request = APIRequestFactory().get('/schools/')
        school_detail = SchoolViewSet.as_view({'get': 'retrieve'})
        school = School.objects.create(name="name", max_student=20)
        response = school_detail(request, pk=school.pk)
        self.assertEqual(response.status_code, 200)

    def test_get_list_school(self):
        """Test get list of school"""
        request = APIRequestFactory().get('/schools/')
        school_detail = SchoolViewSet.as_view({'get': 'list'})
        response = school_detail(request)
        self.assertEqual(response.status_code, 200)

    def test_create_school(self):
        """Test create a school"""
        data = {"name": "name", "max_student": 20}
        request = APIRequestFactory().post("/schools/", data=data)
        school_detail = SchoolViewSet.as_view({'post': 'create'})
        response = school_detail(request)
        self.assertEqual(response.status_code, 201)

    def test_update_school(self):
        """Test update a school"""
        school = School.objects.create(name="name", max_student=20)
        data = {"name": "Nameer", "max_student": 30}
        request = APIRequestFactory().put(f"/schools/{school.pk}", data=data)
        school_detail = SchoolViewSet.as_view({'put': 'update'})
        response = school_detail(request, pk=school.pk)
        self.assertEqual(response.status_code, 200)

        updated_school = School.objects.get()
        self.assertEqual(updated_school.name, "Nameer")
        self.assertEqual(updated_school.max_student, 30)

    def test_delete_school(self):
        """Test delete a school"""
        school = School.objects.create(name="name", max_student=20)
        request = APIRequestFactory().delete(f"/schools/{school.pk}")
        school_detail = SchoolViewSet.as_view({'delete': 'destroy'})
        response = school_detail(request, pk=school.pk)
        self.assertEqual(response.status_code, 204)

        updated_school = School.objects.all()
        self.assertEqual(updated_school.count(), 0)

