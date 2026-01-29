from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship


class VehicleBase(SQLModel):
    number_plate: str = Field(index=True)


class Vehicle(VehicleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    locations: list["Location"] = Relationship(back_populates="vehicle")


class VehicleCreate(VehicleBase):
    pass


class LocationBase(SQLModel):
    lat: float
    lon: float
    hae: float
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )


class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    vehicle: Vehicle = Relationship(back_populates="locations")
    vehicle_id: int = Field(foreign_key="vehicle.id")


class LocationCreate(LocationBase):
    pass
