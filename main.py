from fastapi import FastAPI, Path, Body, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())
people = [Person("Ilya", 33), Person("Robert", 43), Person("Marta", 53)]


def find_person(id):
    for person in people:
        if person.id == id:
            return person
    return None


app = FastAPI()

@app.get("/")
async def main():
    return FileResponse("public/index.html")

@app.get("/api/users")
def get_people():
    return people

@app.get("/api/users/{id}")
def get_person(id):
    person = find_person(id)
    print (person)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message":"Пользователь не найден!"}
        )
    return person

@app.post("/api/users")
def create_person(data = Body()):
    person = Person(data["name"], data["age"])
    people.append(person)
    return person

@app.put("/api/users")
def edit_person(data = Body()):
    person = find_person(data["id"])
    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден!"}
        )
    person.age = data["age"]
    person.name = data["name"]
    return person

@app.delete("/api/users/{id}")
def delete_person(id):
    person = find_person(id)

    if person == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден!"}
        )
    people.remove(person)
    return person



# class Person(BaseModel):
#     name:str
#     age: int | None = None

# app = FastAPI()
# @app.get("/")
# def root():
#     return FileResponse("public/index.html")

# @app.post("/hello")
# def hello(person: Person):
#     if person.age == None:
#         return {"message": f"Прюует! {person.name}"}
#     else:
#         return {"message": f"Прюует! {person.name}, твой возраст:{person.age}"}






# @app.get("/")
# def root():
#     return FileResponse("public/index.html")
 
# @app.post("/hello")
# def hello(
#     name:str = Body(embed=True, min_length=3, max_length=20), 
#     age:int = Body(embed=True, ge=18, lt=100)):
#     return {"message": f"{name}, ваш возраст - {age}"}




# app.mount("/static", StaticFiles(directory="public"))


# @app.get("/users/{name}/{age}")
# def users(name:str  = Path(min_length=3, max_length=20), 
#             age: int = Path(ge=18, lt=111)):
#     return {"name": name, "age": age}


# @app.get("/")
# def read_root():
#     html_content = "<h1>Мой первый FastAPI</h1>"
#     return HTMLResponse(content=html_content)

# @app.get("/users/{name}")
# def users(name:str = Path(min_length=3, max_length=20)):
#     return {"name":name}  # {"name":"ilya"}

