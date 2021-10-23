from uuid import UUID

from pydantic import BaseModel


class Kernel(BaseModel):
    id: UUID
    connection_info_file: str
