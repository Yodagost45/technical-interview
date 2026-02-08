from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
import geopy.distance


class VehicleBase(SQLModel):
    number_plate: str = Field(index=True)


class Vehicle(VehicleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    locations: list["Location"] = Relationship(back_populates="vehicle")

    

    def calculate_average_speed(self):
        average_speed = 0
        previous_lat = 0
        previous_lon = 0
        previous_time_utc = 0
        
        for location in self.locations:
            if previous_lat != 0 and previous_lon != 0 and previous_time_utc != 0:
                coords_1 = (previous_lat, previous_lon)
                coords_2 = (location.lat, location.lon)
                seconds_passed = self._timestamp_to_utc(location.timestamp) - self._timestamp_to_utc(previous_time_utc)
                #(distance(km)/seconds_passed)*3600=km/hr
                average_speed += (geopy.distance.geodesic(coords_1, coords_2, ellipsoid='WGS-84').km/seconds_passed)*3600
                print(average_speed)
            previous_lat = location.lat
            previous_lon = location.lon
            previous_time_utc = location.timestamp
        average_speed /= len(self.locations)
        print(average_speed)
        return str(average_speed)
    
    def _timestamp_to_utc(self, timestamp):
        TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
        d1 = datetime.strptime(str(timestamp), TIME_FORMAT)
        return float(d1.strftime("%s.%f"))

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
