from fastapi import FastAPI, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models import Vehicle, Location, LocationCreate, VehicleCreate

app = FastAPI()


@app.get("/vehicles", response_model=list[Vehicle])
def get_vehicles(session: SessionDep):
    return session.exec(select(Vehicle)).all()


@app.post("/vehicles", response_model=Vehicle)
def create_vehicle(session: SessionDep, vehicle: VehicleCreate):
    db_vehicle = Vehicle.model_validate(vehicle)
    session.add(db_vehicle)
    session.commit()
    session.refresh(db_vehicle)
    return db_vehicle


@app.post("/vehicles/{vehicle_id}/locations", response_model=Location)
def create_location(session: SessionDep, vehicle_id: int, location: LocationCreate):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db_location = Location.model_validate(location, update={"vehicle_id": vehicle_id})
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@app.get("/vehicles/{vehicle_id}/locations", response_model=list[Location])
def get_vehicle_locations(session: SessionDep, vehicle_id: int):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle.locations

@app.get("/vehicles/{vehicle_id}/speed", response_model=str)
def get__average_vehicle_speed(session: SessionDep, vehicle_id: int):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return str(vehicle.calculate_average_speed()) + " km/hr"