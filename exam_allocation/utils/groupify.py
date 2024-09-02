import pandas as pd
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F
from exam_allocation.constants import TableAttributes
from exam_allocation.models import ExamCenter, Student



def generate_student_group_data(choice):
    """
        Group students accross exam centers and join the result with ExamCenter data.
    Args:
        choice (str): exam center attribute for the table. Keeping that for better scalability.

    Returns:
        list: grouped student joined with exam center and converted back to list.
    """
    center_students = list(Student.objects.values(choice).annotate(
                            roll_numbers=ArrayAgg(TableAttributes.ROLL_NUMBER.value, order_by=F(TableAttributes.ROLL_NUMBER.value)) 
                      ).order_by(TableAttributes.EXAM_CENTER_CHOICE.value))
            
    df_center_students = pd.DataFrame.from_dict(center_students)
    exam_center = list(ExamCenter.objects.values(TableAttributes.EXAM_CENTER_ID.value,TableAttributes.TOTAL_CAPACITY.value))
    df_exam_center = pd.DataFrame.from_dict(exam_center)
    df_merged = pd.merge(df_exam_center, df_center_students, left_on=TableAttributes.EXAM_CENTER_ID.value, right_on=TableAttributes.EXAM_CENTER_CHOICE.value, how="inner")
    processed_data = df_merged.to_dict(orient='records')
    return processed_data