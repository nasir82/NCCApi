import enum


class AssistantsDesignation(str, enum.Enum):
    manager = "Manager"
    assistantManager = "Assistant Manager"
    officeAssistant = "Office Assistant"
    dataEntry = "Data Entry"
