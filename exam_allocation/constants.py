from enum import Enum

class TableAttributes(Enum):
    EXAM_ID = "exam_id"
    EXAM_NAME = "exam_name"
    EXAM_DATE = "exam_date"
    INSTRUCTION = "instruction"
    EXAM_CENTER_ID = "exam_center_id"
    CENTER_NAME = "center_name"
    TOTAL_ROOMS = "total_rooms"
    TOTAL_CAPACITY = "total_capacity"
    STUDENT_ID = "student_id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    ROLL_NUMBER = "roll_number"
    AADHAR_NUMBER = "aadhar_number"
    DATE_OF_BIRTH = "date_of_birth"
    EXAM_CENTER_CHOICE = "exam_center_choice"
    
    
class UtilityAttribues(Enum):
    SHIFT_ID = "shift_id"
    ROLL_NUMBERS = "roll_numbers"
    SHIFT_1 = "10.00 AM"
    SHIFT_2 = "2.00 PM"
    DEFAULT_QUEUE = "default"
    
    
class SuccessMessage(Enum):
    SUCCESS = "Success"
    ALLOCATION_SUCCESSFUL = "Successfully allocated students."
    
class ErrorMessage(Enum):
    ERROR = "Error"
    UNSUCCESSFUL_ALLOCATION = "Not enough seats."
    EXAM_NOT_FOUND = "The exam name is invalid. Please check the exam name and try again."
    INTERNAL_SERVER_ERROR = "Internal server error."
    TOO_MANY_STUDENTS = "The total number of student exceeds seat limit in 2 shifts for one day. Add a new exam center and try again."
    
class RawSQL(Enum):
    TRUNCATE_TABLE_ALLOCATION = "truncate table exam_allocation_allocation"
    
class FilePaths(Enum):
    EXAM_PATH = "fixtures\exam.json"
    
class JobStatus(Enum):
    STATUS = "Job Status"
    SUCCESSFUL = "Success"
    FAILED = "Failed"
    QUEUED = "Queued"
    JOB_ID = "job_id"
    
    
    
    