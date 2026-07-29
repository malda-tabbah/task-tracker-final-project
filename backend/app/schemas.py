"""
Pydantic response schemas.
Currently defines only the /health response shape.
CRUD-related schemas (TaskCreate, TaskUpdate, TaskResponse, etc.)
will be added when the task endpoints are implemented.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response returned by GET /health."""
    status: str
    timestamp: str