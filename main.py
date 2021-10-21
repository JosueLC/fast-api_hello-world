#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models

#Person model
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hello": "world"}

#Request and Response Body
@app.post("/person/new")
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
        description="This is a person name. It's between 1 and 50 characters."
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the age of the person. It's required."
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
        description="This is a person id. It's a number greater than zero."
        )
):
    return {person_id : "It exists."}