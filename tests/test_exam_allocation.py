import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from exam_allocation.models import Exam, ExamCenter, Student, Allocation
from django.db.utils import IntegrityError
import pandas as pd
from exam_allocation.views import generate_allocation

class GenerateAllocationTest(APITestCase):
    def setUp(self):
        # Create an Exam
        self.exam = Exam.objects.create(
            exam_id=1,
            exam_name="Test Exam",
            exam_date=datetime.date(2024, 9, 15),
            instruction="Please read the instructions carefully."
        )
        
        # Create Exam Centers
        self.exam_center1 = ExamCenter.objects.create(
            exam_center_id=1,
            center_name="Center 1",
            total_capacity=2,
            exam_id=self.exam
        )
        self.exam_center2 = ExamCenter.objects.create(
            exam_center_id=2,
            center_name="Center 2",
            total_capacity=1,
            exam_id=self.exam
        )
        
        # Create Students
        self.student1 = Student.objects.create(
            student_id=1,
            first_name="John",
            last_name="Doe",
            aadhar_number="123456789012",
            date_of_birth="2000-01-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )
        self.student2 = Student.objects.create(
            student_id=2,
            first_name="Jane",
            last_name="Doe",
            aadhar_number="234567890123",
            date_of_birth="2000-02-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )
        self.student3 = Student.objects.create(
            student_id=3,
            first_name="Jim",
            last_name="Beam",
            aadhar_number="345678901234",
            date_of_birth="2000-03-01",
            exam_center_choice=self.exam_center2,
            exam_id=self.exam
        )
        
        self.client = APIClient()

    def test_generate_allocation_success(self):
        url = reverse(generate_allocation)  # Update this with the correct URL name
        response = self.client.post(url, {'exam_name': 'Test Exam'}, format='json')
        
        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the correct number of Allocations were created
        allocations = Allocation.objects.all()
        self.assertEqual(allocations.count(), 3)
        
        # Check if the allocation has the correct data
        for allocation in allocations:
            self.assertEqual(allocation.exam_name, "Test Exam")
            self.assertIn(allocation.exam_center_id, [self.exam_center1.exam_center_id, self.exam_center2.exam_center_id])
            self.assertIn(allocation.roll_number, [self.student1.roll_number, self.student2.roll_number, self.student3.roll_number])
            self.assertEqual(allocation.exam_date, self.exam.exam_date)

    def test_generate_allocation_too_many_students(self):
        # Create extra students to exceed the total capacity
        Student.objects.create(
            student_id=4,
            first_name="Extra",
            last_name="Student",
            aadhar_number="456789012345",
            date_of_birth="2000-04-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )
        Student.objects.create(
            student_id=5,
            first_name="Another",
            last_name="Extra",
            aadhar_number="567890123456",
            date_of_birth="2000-05-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )
        Student.objects.create(
            student_id=6,
            first_name="Another",
            last_name="Extra",
            aadhar_number="567890123456",
            date_of_birth="2000-05-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )
        Student.objects.create(
            student_id=7,
            first_name="Another",
            last_name="Extra",
            aadhar_number="567890123456",
            date_of_birth="2000-05-01",
            exam_center_choice=self.exam_center1,
            exam_id=self.exam
        )

        url = reverse(generate_allocation)  # Update this with the correct URL name
        response = self.client.post(url, {'exam_name': 'Test Exam'}, format='json')
        
        # Ensure the response is 400 Bad Request due to too many students
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_allocation_no_exam_name(self):
        url = reverse(generate_allocation)  # Update this with the correct URL name
        response = self.client.post(url, {}, format='json')
        
        # Ensure the response is 200 OK but no allocation should happen
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        allocations = Allocation.objects.all()
        self.assertEqual(allocations.count(), 0)

    def test_generate_allocation_invalid_exam_name(self):
        url = reverse(generate_allocation)  # Update this with the correct URL name
        response = self.client.post(url, {'exam_name': 'Invalid Exam'}, format='json')
        
        # Ensure the response is 500 Internal Server Error due to invalid exam name
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
