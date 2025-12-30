from typing import Optional

from pydantic import BaseModel


class Statistics(BaseModel):
    hsh: Optional[int] = 0
    msh: Optional[int] = 0
    lsh: Optional[int] = 0
    hg: Optional[int] = 0
    mg: Optional[int] = 0
    lg: Optional[int] = 0
    a: Optional[int] = 0
    gb: Optional[int] = 0
    t: Optional[int] = 0
    ct: Optional[int] = 0
    p: Optional[int] = 1
    k: Optional[int] = 0
    ms: Optional[int] = 0
    hga: Optional[int] = 0
    mga: Optional[int] = 0
    lga: Optional[int] = 0
    hgs: Optional[int] = 0
    mgs: Optional[int] = 0
    lgs: Optional[int] = 0
    fow: Optional[int] = 0
    fol: Optional[int] = 0
