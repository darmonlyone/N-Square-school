from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.SimpleRouter()
router.register('schools', views.SchoolViewSet)
router.register('students', views.StudentViewSet)

student_router = routers.NestedSimpleRouter(router, 'schools', lookup='schools')
student_router.register('students', views.StudentSchoolViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(student_router.urls)),
]
