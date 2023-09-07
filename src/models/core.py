from pydantic import BaseModel

class IDModelMixin(BaseModel):
    id: int