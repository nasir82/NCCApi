from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from app.models.models import AssistantsDesignation, EventStatus, EventType, ResourceType
from app.utils.utility import AdministrationDesignationType

class BannerBase(BaseModel):
    title: str
    image_url: str

class BannerCreate(BannerBase):
    title: str
    image_url: str

class BannerResponse(BannerBase):
    ref: str 
    image_url: str
    title: str
    model_config = ConfigDict(from_attributes=True)
    
    
class StudentBase(BaseModel):
    name: str
    mobile: str
    level: str
    year: str
    school: str
    address: str
    guardian_phone: str
    profile_image_url: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
    
    

class UserBase(BaseModel):
    name: str
    rule: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
    
    
class OfficialPersonBase(BaseModel):
    name: str
    phone: str
    email: str
    designation: AdministrationDesignationType = AdministrationDesignationType.NONE
    profile_link: str
    join_date: str
    end_date: str

class OfficialPersonCreate(OfficialPersonBase):
    pass

class OfficialPersonResponse(OfficialPersonBase):
    ref: str

    model_config = ConfigDict(from_attributes=True)
    
    
class AttendanceModelSchema(BaseModel):
    date: datetime
    subject: str
    teacherName: str
    attendanceByStudentId: Dict[str, bool]

class AttendanceTrackingBase(BaseModel):
    level: str
    year: str
    students: List[dict] # You can use StudentResponse here if you want strict validation
    attendance_records: List[AttendanceModelSchema]

class AttendanceTrackingCreate(AttendanceTrackingBase):
    pass

class AttendanceTrackingResponse(AttendanceTrackingBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
    
    
class EventBase(BaseModel):
    title: str
    type: EventType
    content: str
    published: datetime
    status: EventStatus = EventStatus.upcoming

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
    
class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    selection: str = ""
    correctAns: str
    mark: int = -1
    explanation: str = ""

class ExamBase(BaseModel):
    examTitle: str
    subject: str
    examTopics: List[str]
    examDate: datetime
    totalTime: int # Minutes
    questions: List[QuestionSchema]
    level: str
    isAttended: bool = False
    gainedNumber: int = 0

class ExamCreate(ExamBase):
    pass

class ExamResponse(ExamBase):
    ref: str
    model_config = ConfigDict(from_attributes=True)

class PaymentModelSchema(BaseModel):
    monthName: str
    paymentStatus: Dict[str, bool] # key = studentId, value = isPaid

class PaymentTrackingBase(BaseModel):
    level: str
    year: str
    students: List[dict] # Using raw dict to match StudentModel.toMap()
    payment_status_records: List[PaymentModelSchema]

class PaymentTrackingCreate(PaymentTrackingBase):
    pass

class PaymentTrackingResponse(PaymentTrackingBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class ResourceBase(BaseModel):
    title: str
    type: ResourceType
    link: str
    level: str = ""
    dateOfUpload: datetime

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: str
    model_config = ConfigDict(from_attributes=True)
    
    
class OfficePersonBase(BaseModel):
    name: str
    designation: AssistantsDesignation
    phone: str
    email: str
    image: str
    from_date: str = Field(..., alias="from") # Allows "from" in JSON
    to_date: str = Field("", alias="to")      # Allows "to" in JSON

    model_config = ConfigDict(populate_by_name=True)

class OfficePersonCreate(OfficePersonBase):
    pass

class OfficePersonResponse(OfficePersonBase):
    ref: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
class TeacherBase(BaseModel):
    name: str
    mobile: str
    email: EmailStr
    background: str
    profileImageUrl: str
    subjects: List[str] = []

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    id: str
    model_config = ConfigDict(from_attributes=True)