from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from here_debugger.debug import here_debug
from collections import deque
import pandas as pd
from .models import Student, Exam, ExamCenter, Allocation
from .constants import TableAttributes, ErrorMessage, SuccessMessage, UtilityAttribues, RawSQL

# Create your views here.

@api_view(['POST'])
def generate_allocation(request):
    try:
        exam_name = request.data.get(TableAttributes.EXAM_NAME.value,"")
        if exam_name:
            with connection.cursor() as cursor:
                cursor.execute(RawSQL.TRUNCATE_TABLE_ALLOCATION.value)
            exam_date = Exam.objects.values_list(TableAttributes.EXAM_DATE.value, flat=True)[0]
            exam_id = Exam.objects.filter(exam_name=exam_name).values_list(TableAttributes.EXAM_ID.value, flat=True)[0]
            
            center_students = list(Student.objects.values(TableAttributes.EXAM_CENTER_CHOICE.value).annotate(
                roll_numbers=ArrayAgg(TableAttributes.ROLL_NUMBER.value, order_by=F(TableAttributes.ROLL_NUMBER.value)) 
            ).order_by(TableAttributes.EXAM_CENTER_CHOICE.value))
            
            df_center_students = pd.DataFrame.from_dict(center_students)
            exam_center = list(ExamCenter.objects.values(TableAttributes.EXAM_CENTER_ID.value,TableAttributes.TOTAL_CAPACITY.value))
            df_exam_center = pd.DataFrame.from_dict(exam_center)
            df_merged = pd.merge(df_exam_center, df_center_students, left_on=TableAttributes.EXAM_CENTER_ID.value, right_on=TableAttributes.EXAM_CENTER_CHOICE.value, how="inner")
            processed_data = df_merged.to_dict(orient='records')
            
            total_students = Student.objects.count()
            total_seats = 0
            shift = [UtilityAttribues.SHIFT_1.value, UtilityAttribues.SHIFT_2.value]
            
            for data in processed_data:
                total_seats+=data[TableAttributes.TOTAL_CAPACITY.value]
                data[UtilityAttribues.ROLL_NUMBERS.value] = deque(data[UtilityAttribues.ROLL_NUMBERS.value])
                
            if(len(shift)*total_seats < total_students):
                return Response({ErrorMessage.ERROR.value: ErrorMessage.TOO_MANY_STUDENTS.value}, status=status.HTTP_400_BAD_REQUEST)
            
            final_allocation_list = []
            remaining_allocation_schedule = []
            
            for data in processed_data:
                exam_center_id = data[TableAttributes.EXAM_CENTER_ID.value]
                roll_numbers = data[UtilityAttribues.ROLL_NUMBERS.value]
                for shift_id in shift:
                    total_capacity = data[TableAttributes.TOTAL_CAPACITY.value]
                    while roll_numbers:
                        roll = roll_numbers[0]
                        if total_capacity == 0:
                            break
                        allocation_object = Allocation(
                            exam_name=exam_name,
                            exam_center_id=exam_center_id,
                            roll_number=roll,
                            exam_date=exam_date,
                            exam_time=shift_id
                        )
                        final_allocation_list.append(allocation_object)
                        roll_numbers.popleft()
                        total_capacity-=1
                    
                    remaining_allocation_schedule.append(
                        {
                            TableAttributes.EXAM_CENTER_ID.value: exam_center_id,
                            TableAttributes.TOTAL_CAPACITY.value: total_capacity,
                            UtilityAttribues.SHIFT_ID.value : shift_id
                        }
                    )
                    
            for data in processed_data:
                roll_numbers = data[UtilityAttribues.ROLL_NUMBERS.value]
                exam_center_id = data[TableAttributes.EXAM_CENTER_ID.value]
                if roll_numbers:
                    for allocation in remaining_allocation_schedule:
                        total_capacity = allocation[TableAttributes.TOTAL_CAPACITY.value]
                        shift_id = allocation[UtilityAttribues.SHIFT_ID.value]
                        exam_center_id = allocation[TableAttributes.EXAM_CENTER_ID.value]
                        while roll_numbers:
                            roll = roll_numbers[0]
                            if total_capacity == 0:
                                break
                            allocation_object = Allocation(
                            exam_name=exam_name,
                            exam_center_id=exam_center_id,
                            roll_number=roll,
                            exam_date=exam_date,
                            exam_time=shift_id
                            )
                            final_allocation_list.append(allocation_object)
                            roll_numbers.popleft()
                            total_capacity-=1

            Allocation.objects.bulk_create(final_allocation_list)
        return Response({SuccessMessage.SUCCESS.value: SuccessMessage.ALLOCATION_SUCCESSFUL.value}, status=status.HTTP_200_OK)
    
    except Exception as error:
        here_debug(error)
        return Response({ErrorMessage.ERROR.value : ErrorMessage.INTERNAL_SERVER_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
    


