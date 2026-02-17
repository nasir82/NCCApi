import enum


class EventType(str, enum.Enum):
    image = "image"
    video = "video"
    text = "text"
    pdf = "pdf"
    
class ResourceType(str, enum.Enum):
    books = "books"
    notes = "notes"
    videos = "videos"
    exams = "exams"
    routines = "routines"
    assignments = "assignments"
    results = "results"
