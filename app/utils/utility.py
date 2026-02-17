import enum

class AdministrationDesignationType(str, enum.Enum):
    NONE = "None"
    ADMIN = "Admin"
    CHAIRMAN = "Chairman"
    ASSISTANT_CHAIRMAN = "Assistant Chairman"
    EXECUTIVE_DIRECTOR = "Executive Director"
    DIRECTOR = "Director"