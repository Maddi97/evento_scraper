from pydantic import BaseModel, Field
from typing import List, Optional, Union


class Address(BaseModel):
    plz: Optional[str] = Field(description="Plz an dem das Event stattfindet")
    street: Optional[str] = Field(
        description="Name der Strasse an dem das Event stattfindet"
    )
    city: Optional[str] = Field(description="Name der Stadt")
    streetNumber: Optional[str] = Field(
        description="Hausnummer in der Strasse in der das Event stattfindet"
    )


class Subcategory(BaseModel):
    name: Optional[str]
    iconPath: Optional[str]
    iconTemporaryURL: Optional[str]
    stockImagePath: Optional[str]
    stockTemporaryURL: Optional[str]


class Category(BaseModel):
    name: Optional[str]
    iconTemporaryURL: Optional[str]
    iconPath: Optional[str]
    stockImagePath: Optional[str]
    stockTemporaryURL: Optional[str]
    subcategories: Optional[List[Subcategory]]


class DateRange(BaseModel):
    start: Optional[str] = Field(description="Der Startdatum des Events")
    end: Optional[str] = Field(description="Der Enddatum des Events")


class Coordinates(BaseModel):
    lat: Optional[str]
    lon: Optional[str]


class Times(BaseModel):
    start: Optional[str] = Field(description="Uhrzeit zu der das Event beginnt")
    end: Optional[str] = Field(description="Uhrzeit zu der das Event endet")


class EventSchema(BaseModel):
    name: str = Field(description="Der Name des Events")
    # does not workorganizerName:  Optional[str]=Field(description="Der Name des Organisators des Events")
    link: Optional[str] = Field(
        description="Die Url unter der man die Eventseite erreicht"
    )
    price: Optional[str] = Field(description="Der Eintrittspreis")
    date: Optional[DateRange] = Field(description="Datum an dem das Event stattfindet")
    frequency: Optional[Union[dict, str, None]] = Field(
        description="Die Häufigkeit mit der das Event stattfindet"
    )
    address: Optional[Address] = Field(description="Die Adress des Events")
    times: Optional[Times] = Field(
        description="Die Uhrzeiten an denen das Event stattfindet"
    )
    description: Optional[str] = Field(description="Beschreibung des Events")
