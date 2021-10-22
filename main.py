#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, HttpUrl
#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

#Person model
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    email : EmailStr = Field(...)
    password : str = Field(..., min_length=8)
    website: HttpUrl = Field(default=None)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example" : {
                "first_name" : "Josue",
                "last_name" : "Lopez",
                "age" : "40",
                "email" : "josueflopez@fedora.com",
                "password" : "klafkl098304",
                "website" : "http://www.josue.com",
                "hair_color" : "black",
                "is_married" : True
            }
        }
class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    email : EmailStr = Field(...)
    website: HttpUrl = Field(default=None)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

#Location model
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=100
        )
    state: str = Field(
        ...,
        min_length=2,
        max_length=100
        )
    country: str = Field(
        ...,
        min_length=2,
        max_length=100
        )
    class Config:
        schema_extra = {
            "example" : {
                "city" : "Palmira",
                "state" : "Valle",
                "country" : "Colombia"
            }
        }

@app.get("/")
def home():
    return {"Hello": "world"}

#Request and Response Body
@app.post("/person/new",response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person name",
        description="This is a person name. It's between 1 and 50 characters.",
        example="Mathias"   #Query parameters example.
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the age of the person. It's required.",
        example=19
        )           #Obligatorio (no es lo ideal, debería ser un path parameter)
):
    return {name : age}

#Validaciones: Path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is a person id. It's a number greater than zero.",
        example=19
        )
):
    return {person_id : "It exists."}

#Validaciones: Request body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person id",
        description="This is a person id.",
        gt=0,
        example=19
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

#Tipos de datos exóticos
# - Enum   - HttpUrl    - FilePath    - DirectoryPath   - EmailStr
# - PaymentCardNumber   - IPvAnyAddress     - NegativeFloat     - PositiveFloat
# - NegativeInt     - PositiveInt