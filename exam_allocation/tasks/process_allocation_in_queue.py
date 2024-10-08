# tasks.py
from django.db import connection
from collections import deque
from exam_allocation.models import Student, Exam, Allocation
from exam_allocation.constants import TableAttributes, UtilityAttribues, RawSQL, ErrorMessage, SuccessMessage
from exam_allocation.utils import groupify
from here_debugger.debug import here_debug

def perform_allocation(exam_name):
    try:
        is_valid_exam = Exam.objects.filter(exam_name=exam_name).count()
        if not is_valid_exam:
            return ErrorMessage.EXAM_NOT_FOUND.value

        with connection.cursor() as cursor:
            cursor.execute(RawSQL.TRUNCATE_TABLE_ALLOCATION.value)

        exam_date = Exam.objects.values_list(TableAttributes.EXAM_DATE.value, flat=True)[0]
        processed_data = groupify.generate_student_group_data(TableAttributes.EXAM_CENTER_CHOICE.value)
        total_students = Student.objects.count()
        total_seats = 0
        shift = [UtilityAttribues.SHIFT_1.value, UtilityAttribues.SHIFT_2.value]

        for data in processed_data:
            total_seats += data[TableAttributes.TOTAL_CAPACITY.value]
            data[UtilityAttribues.ROLL_NUMBERS.value] = deque(data[UtilityAttribues.ROLL_NUMBERS.value])

        if (len(shift) * total_seats) < total_students:
            return ErrorMessage.TOO_MANY_STUDENTS.value

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
                    total_capacity -= 1

                remaining_allocation_schedule.append(
                    {
                        TableAttributes.EXAM_CENTER_ID.value: exam_center_id,
                        TableAttributes.TOTAL_CAPACITY.value: total_capacity,
                        UtilityAttribues.SHIFT_ID.value: shift_id
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
                        total_capacity -= 1

        Allocation.objects.bulk_create(final_allocation_list)
        return SuccessMessage.ALLOCATION_SUCCESSFUL.value
    
    except Exception as error:
        here_debug(error)
        return ErrorMessage.INTERNAL_SERVER_ERROR.value
