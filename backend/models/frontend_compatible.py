from pydantic import BaseModel


class FrontendVehicle(BaseModel):
    plate: str


class FrontendDriver(BaseModel):
    driver_name: str
