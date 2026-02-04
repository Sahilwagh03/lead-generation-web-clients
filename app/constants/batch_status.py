from enum import Enum

class BatchStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PROCESSED = "PROCESSED"

class LeadStatus(str, Enum):
    NEW = "NEW"                 # freshly scraped/imported
    CONTACTED = "CONTACTED"     # first message sent
    REMINDER = "REMINDER"       # follow-up pending
    RETARGET = "RETARGET"       # try again later
    INTERESTED = "INTERESTED"   # positive response
    NEGOTIATION = "NEGOTIATION" # discussing price/details
    ACCEPTED = "ACCEPTED"       # deal closed / converted
    REJECTED = "REJECTED"       # clearly not interested
    INVALID = "INVALID"         # wrong number/email/fake
    BLOCKED = "BLOCKED"         # user blocked or spam