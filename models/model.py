from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class ErrorResponse(BaseModel):  
    error: str  
    detail: str 


class GenerationRequest(BaseModel):
    query: str


class GenerationResponse(BaseModel):
    answer: str
    dialog_state: str

class DateTimeModel(BaseModel):
    """
    The way the date should be structured and formatted
    """
    date: str = Field(..., description="Properly formatted datetime", pattern=r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')

    @field_validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', v):
            raise ValueError("The date should be in format 'DD-MM-YYYY HH:MM'")
        return v
    
class DateModel(BaseModel):
    """
    The way the date should be structured and formatted
    """
    date: str = Field(..., description="Properly formatted date", pattern=r'^\d{2}-\d{2}-\d{4}$')

    @field_validator("date")
    def check_format_date(cls, v):
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', v):
            raise ValueError("The date must be in the format 'DD-MM-YYYY'")
        return v

    
class IdentificationNumberModel(BaseModel):
    """
    The way the ID should be structured and formatted
    """
    id: int = Field(..., description="identification number as integer (7-8 digits)")

    @field_validator("id")
    def check_format_id(cls, v):
        # Convert to string to check length and ensure it's all digits
        id_str = str(v)
        if not (7 <= len(id_str) <= 8 and id_str.isdigit()):
            raise ValueError("The ID number should be a 7 or 8 digit integer")
        return v

# Primary Assistant
class ToPrimaryBookingAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle patient appointment booking, updates and cancellations."""

    request: str = Field(
        description="Any necessary followup questions the update appointment booking assistant should clarify before proceeding."
    )


class ToGetInfo(BaseModel):
    """Get information of doctor availability via name or specialization"""

    desired_date: DateModel = Field(
        description="The desired date for booking"
    )
    specialization: Optional[str] = Field(
        default=None, description="The desired specialization of the doctor"
    )
    doctor_name: Optional[str] = Field(
        default=None, description="The desired doctor name for booking"
    )
    request: str = Field(
        description="Any additional information or requests from the user regarding the appointment."
    )


class ToAppointmentBookingAssistant(BaseModel):
    """Transfer work to a specialized assistant to handle hotel bookings."""

    date:DateTimeModel = Field(
        description="The date for setting, cancel or rescheduling appointment"
    )
    identification_number: IdentificationNumberModel = Field(
        description="The id number of user."
    )
    doctor_number: str = Field(
        description="The name of the doctor"
    )
    request: str = Field(
        description="Any additional information or requests from the user regarding the hotel booking."
    )


class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
    who can re-route the dialog based on the user's needs."""

    cancel: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "cancel": True,
                "reason": "User changed their mind about the current task.",
            },
            "example 2": {
                "cancel": True,
                "reason": "I have fully completed the task.",
            },
            "example 3": {
                "cancel": False,
                "reason": "I need to search the user's date and time for more information.",
            },
        }
