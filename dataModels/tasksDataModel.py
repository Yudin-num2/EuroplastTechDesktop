from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: str
    task: str
    workers: List[str]
    status: str
    techcard: Optional[str] = None
    pathtophoto: Optional[str] = None
    createtime: str
    author: str
    spentrepairparts: Optional[str] = None
    checklist: Optional[str] = None
    comment: Optional[str] = None
    failed_element: Optional[str] = None

class Tasks(BaseModel):
    tasks: List[Task]
