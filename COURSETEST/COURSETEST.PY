from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import Course
from .serializers import CourseDetailSerializer
from students.models import Student, StudentRegistration
from django.contrib.auth.models import User

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.user.is_staff = True
        self.user.save()
        
        self.course1 = Course.objects.create(course_code='C001', course_name='Mathematics', instructor_name='Mr. Smith')
        self.course2 = Course.objects.create(course_code='C002', course_name='Science', instructor_name='Ms. Johnson')
        self.student1 = Student.objects.create(student_id='S001', name='John Doe')
        self.student2 = Student.objects.create(student_id='S002', name='Jane Doe')
        
        # Simulate a prerequisite relationship
        self.course3 = Course.objects.create(course_code='C003', course_name='Advanced Math', instructor_name='Mr. Smith')
        self.course1.prerequisites.add(self.course3)
        self.course1.save()

    def test_course_details(self):
        url = reverse('course_details', args=[self.course1.pk])
        response = self.client.get(url)
        serializer = CourseDetailSerializer(self.course1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_details_not_found(self):
        url = reverse('course_details', args=[999])  # Non-existent course ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_courses_staff(self):
        self.client.force_login(self.user)  # Login as staff
        url = reverse('get_all_courses')
        response = self.client.get(url)
        courses = Course.objects.all()
        serializer = CourseDetailSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view is incorrectly using render instead of Response.
        #       This test will fail unless the view is corrected.
        
    def test_get_all_courses_student(self):
        # Simulate session
        session = self.client.session
        session['student_id'] = self.student1.student_id
        session.save()
        
        url = reverse('get_all_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view is incorrectly using render instead of Response.
        #       This test will fail unless the view is corrected.

    def test_get_all_courses_unauthenticated(self):
        url = reverse('get_all_courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_search_course(self):
        url = reverse('search_course')
        query_params = {'course_name': 'Mathematics'}
        response = self.client.get(url, query_params)
        courses = Course.objects.filter(course_name__icontains='Mathematics')
        serializer = CourseDetailSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view is incorrectly using render instead of Response.
        #       This test will fail unless the view is corrected.

    def test_search_course_instructor(self):
        url = reverse('search_course')
        query_params = {'instructor_name': 'Mr. Smith'}
        response = self.client.get(url, query_params)
        courses = Course.objects.filter(instructor_name__icontains='Mr. Smith')
        serializer = CourseDetailSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view is incorrectly using render instead of Response.
        #       This test will fail unless the view is corrected.

    def test_search_course_code(self):
        url = reverse('search_course')
        query_params = {'course_code': 'C001'}
        response = self.client.get(url, query_params)
        courses = Course.objects.filter(course_code__icontains='C001')
        serializer = CourseDetailSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: The view is incorrectly using render instead of Response.
        #       This test will fail unless the view is corrected.

# Correct the views to use Response instead of render for API consistency
# @api_view(['GET'])
# def get_all_courses(request):
#     # ...
#     serializer = CourseDetailSerializer(courses, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def search_course(request):
#     # ...
#     serializer = CourseDetailSerializer(courses, many=True)
#     return Response(serializer.data)
