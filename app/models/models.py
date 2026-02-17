import uuid
from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, Integer, String
from app.database.database import Base
from app.models.designations import AssistantsDesignation
from app.models.event_status import EventStatus
from app.models.types import EventType, ResourceType
from app.utils.utility import AdministrationDesignationType

class Banner(Base):
    __tablename__ = "banners"

    ref = Column(
        String(36), 
        unique=True, 
        index=True, 
        nullable=False, 
        default=lambda: str(uuid.uuid4()),
        primary_key=True
    )
    image_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    
    

class Student(Base):
    __tablename__ = "students"

    id = Column(
        String(36), 
        primary_key=True, 
        index=True, 
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    level = Column(String, nullable=False)
    year = Column(String, nullable=False)
    school = Column(String, nullable=False)
    address = Column(String, nullable=False)
    guardian_phone = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=True)
    
    
class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), 
        primary_key=True, 
        index=True, 
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    rule = Column(String, nullable=False)
    
    
    
class OfficialPerson(Base):
    __tablename__ = "official_persons"

    ref = Column(
        String(36), 
        primary_key=True, 
        index=True, 
        default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    designation = Column(
        Enum(AdministrationDesignationType), 
        default=AdministrationDesignationType.NONE,
        nullable=False
    )
    profile_link = Column(String, nullable=False)
    join_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    
    
    
class AttendanceTracking(Base):
    __tablename__ = "attendance_tracking"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    level = Column(String, nullable=False)
    year = Column(String(4), nullable=False)
    
    students = Column(JSON, nullable=False, default=[])
    attendance_records = Column(JSON, nullable=False, default=[])
    
    


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(Enum(EventType), default=EventType.text, nullable=False)
    content = Column(String, nullable=False)
    published = Column(DateTime, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.upcoming, nullable=False)
    
class Exam(Base):
    __tablename__ = "exams"

    ref = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    examTitle = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    examTopics = Column(JSON, nullable=False)
    examDate = Column(DateTime, nullable=False)
    totalTime = Column(Integer, nullable=False)
    questions = Column(JSON, nullable=False)
    isAttended = Column(Boolean, default=False)
    gainedNumber = Column(Integer, default=0)
    level = Column(String, nullable=False)
    
class PaymentTracking(Base):
    __tablename__ = "payment_tracking"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    level = Column(String, nullable=False)
    year = Column(String(4), nullable=False)
    
    students = Column(JSON, nullable=False, default=[])
    payment_status_records = Column(JSON, nullable=False, default=[])
    

class Resource(Base):
    __tablename__ = "resources"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    link = Column(String, nullable=False)
    level = Column(String, default="")
    dateOfUpload = Column(DateTime, nullable=False)
    

class OfficePerson(Base):
    __tablename__ = "office_staff"
    ref = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    designation = Column(Enum(AssistantsDesignation), nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    image = Column(String, nullable=False)
    from_date = Column(String, nullable=False)
    to_date = Column(String, default="")
    
    
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    background = Column(String, nullable=False)
    profileImageUrl = Column(String, nullable=False)
    subjects = Column(JSON, nullable=False, default=[])