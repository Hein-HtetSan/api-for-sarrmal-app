from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta

class Chat(BaseModel):
    user_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    message: str
    response: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    delete_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(days=3))

    
    @validator("updated_at", pre=True, always=True)
    def set_updated_at(cls, v):
        return v or datetime.utcnow()
    def save(self, update: bool = False):
        if update:
            self.updated_at = datetime.utcnow()
            
# user request model to make an api request to open ai chat bot
class RequestModel(BaseModel):
    message: str

# for the user message editing
class ResponseModel(BaseModel):
    response: str