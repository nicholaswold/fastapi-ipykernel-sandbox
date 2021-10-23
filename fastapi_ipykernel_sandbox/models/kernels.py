from pydantic import BaseModel
from typing import Dict
from uuid import UUID
from jupyter_client.connect import KernelConnectionInfo


class Kernel(BaseModel):
    id: UUID
    connection_info_file: str