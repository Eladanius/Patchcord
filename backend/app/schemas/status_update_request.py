from pydantic import BaseModel


class StatusUpdateRequest(BaseModel):
    status_id: int
