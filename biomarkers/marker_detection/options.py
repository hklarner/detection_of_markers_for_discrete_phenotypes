

from typing import List, Optional

from pydantic import BaseModel


class Options(BaseModel):
    forbidden: List[int] = []
    enable_one_to_one: bool = False
    marker_size_min: int = 1
    marker_size_max: Optional[int] = None
