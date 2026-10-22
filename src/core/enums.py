from enum import StrEnum

class TripRole(StrEnum):
    ORGANIZER = "organizer"
    MEMBER = "member"

class ChecklistScope(StrEnum):
    SHARED = "shared"
    PERSONAL = "personal"

class PollStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"