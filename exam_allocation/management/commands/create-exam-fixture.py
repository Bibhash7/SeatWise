from django.core.management import BaseCommand
from exam_allocation.models import Exam
from exam_allocation.constants import TableAttributes
from exam_allocation.constants import FilePaths
class Command(BaseCommand):
    help = "This will load data into a json file."
    def handle(self, *args, **kwargs):
        exam_list = []
        for data in Exam.objects.all():
            exam_list.append({
                TableAttributes.EXAM_ID.value: data.exam_id,
                TableAttributes.EXAM_NAME.value: data.exam_name,
                TableAttributes.EXAM_DATE.value: str(data.exam_date),
                TableAttributes.INSTRUCTION.value: data.instruction
            })
        with open(FilePaths.EXAM_PATH.value,'w') as f:
            f.write(str(exam_list))
            