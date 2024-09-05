# views.py
import time
from django_rq import get_queue
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from here_debugger.debug import here_debug
from .tasks.process_allocation_in_queue import perform_allocation
from .constants import TableAttributes, ErrorMessage, SuccessMessage, UtilityAttribues, JobStatus
from rq.job import Job

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[TableAttributes.EXAM_NAME.value],
        properties={
            TableAttributes.EXAM_NAME.value: openapi.Schema(type=openapi.TYPE_STRING, description='Name of the exam'),
        },
    ),
    responses={200: 'OK'}
)

@api_view(['POST'])
def generate_allocation(request):
    """
        Allocates students based on their exam center preference.
    Args:
        request (str): The exam the students are appearing for

    Returns:
       Response ( HTTPResponse ): Success if successfully allocated students among exam centers. On failure, an appropriate error message.
    """
    try:
        exam_name = request.data.get(TableAttributes.EXAM_NAME.value, "")
        if not exam_name:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.INVALID_INPUT.value}, status=status.HTTP_400_BAD_REQUEST)
        
        queue = get_queue(UtilityAttribues.DEFAULT_QUEUE.value)
        job = queue.enqueue(perform_allocation, exam_name)
        return Response({JobStatus.JOB_ID.value: job.id}, status=status.HTTP_202_ACCEPTED)
    
    except Exception as error:
        here_debug(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVER_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_task_status(request):
    """
        Returns the task status for Django Redis Queue Task.
    Args:
        request ( str ): contains the job id

    Returns:
        Response ( HTTPResponse ): Returns the job status, (Successful, falied, queued)
    """
    job_id = request.data.get(JobStatus.JOB_ID.value)
    queue = get_queue(UtilityAttribues.DEFAULT_QUEUE.value)
    try:
        job = Job.fetch(job_id, connection=queue.connection)
        if job.is_finished:
           job_result = job.result 
           if job_result:
               if SuccessMessage.SUCCESS.value in job_result:
                   return Response(
                       {
                            JobStatus.STATUS.value: JobStatus.SUCCESSFUL.value,
                            SuccessMessage.SUCCESS.value: SuccessMessage.ALLOCATION_SUCCESSFUL.value
                       }, 
                       status=status.HTTP_201_CREATED
                    )
               elif ErrorMessage.TOO_MANY_STUDENTS.value in job_result:
                   return Response(
                       {
                            JobStatus.STATUS.value: JobStatus.SUCCESSFUL.value, 
                            ErrorMessage.ERROR.value: ErrorMessage.TOO_MANY_STUDENTS.value
                       }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
                
               elif ErrorMessage.EXAM_NOT_FOUND.value in job_result:
                   return Response(
                       {
                            JobStatus.STATUS.value: JobStatus.SUCCESSFUL.value, 
                            ErrorMessage.ERROR.value: ErrorMessage.EXAM_NOT_FOUND.value
                       }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
               
               else:
                   return Response({
                            JobStatus.STATUS.value: JobStatus.SUCCESSFUL.value, 
                            ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVER_ERROR.value
                       }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
        elif job.is_failed:
                here_debug(str(job.exc_info))
                return Response({
                        JobStatus.STATUS.value: JobStatus.FAILED.value, 
                        ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVER_ERROR.value
                    }, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        else:
            return Response({
                    JobStatus.STATUS.value: JobStatus.QUEUED.value,
                    ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVER_ERROR.value
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    except Exception as error:
        here_debug(error)
        return Response(
            {
                JobStatus.STATUS.value: JobStatus.FAILED.value, 
                ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVER_ERROR.value
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )