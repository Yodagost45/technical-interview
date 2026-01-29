from sqlmodel import Field, SQLModel


class Vehicle(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    number_plate: str = Field(index=True)
