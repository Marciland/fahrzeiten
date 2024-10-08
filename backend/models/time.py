from datetime import datetime

from pydantic import BaseModel


class Timespan(BaseModel):
    start: datetime
    end: datetime
