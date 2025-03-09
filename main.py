from typing import Union
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import logging
import time
import uvicorn
import json

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)


class Movie(BaseModel):
    id: int
    name: str
    watched: bool


class NewMovie(BaseModel):
    name: str
    watched: Union[bool, None]


def get_movies_from_file():
    file = open("./data/movies.json", "r")
    movies = json.load(file) # read from json file
    return movies

def update_movies_file(movies:list[Movie]):
    file = open("./data/movies.json", "w") # "w" to overwrite, "a" to append
    movies = json.dumps(movies) # transform dict -> json
    file.write(movies)
    file.close()



@app.get("/movies")
# curl -X 'GET' 'http://localhost:8000/movies'
def read_movies() -> list[Movie]:
    logging.debug("/movies fired")
    movies = get_movies_from_file()
    return movies


@app.get("/movies/{id}")
# curl -X 'GET' 'http://localhost:8000/movies/1740528382135'
def read_movie_id(id: int) -> Movie:
    logging.debug("incoming id: ", id)
    movies = get_movies_from_file()
    movie = next((m for m in movies if m["id"] == id), None)
    if not movie:
        raise HTTPException(
            status_code=404, detail=f"Movie with the id {id} does not exist."
        )
    return movie


@app.post("/movies")
# curl -X 'POST' 'http://localhost:8000/movies' -H 'Content-Type: application/json' -d '{"name": "Inception", "watched": false}'
def add_movie(movie: NewMovie) -> list[Movie]:
    movies = get_movies_from_file()
    if any(m["name"] == movie.name for m in movies):
        raise HTTPException(
            status_code=400, detail=f"Movie {movie.name} already exists in the list."
        )

    # transform model into a dictionary
    props = movie.model_dump()
    id = {"id":  int(time.time() * 1000)} # timestamp in ms

    # movie_dict["id"] = int(time.time() * 1000) # this sets id as the last prop of the object

    movie_dict = {**id, **props} # set proper sequence: id -> name -> watched
    movies.append(movie_dict)
    update_movies_file(movies)

    return movies


@app.put("/movies/{id}")
# curl -X 'PUT' 'http://localhost:8000/movies/1740528382135?watched=true' -H 'Content-Type: application/json'
def update_movie(id: int, watched: bool) -> Movie:
    movies = get_movies_from_file()
    idx = next(
        (i for i, m in enumerate(movies) if m["id"] == id), None
    )  # get index of the item in the array
    if idx is None:
        raise HTTPException(
            status_code=404, detail=f"Movie with the id {id} doesn't exist."
        )
    movies[idx]["watched"] = watched
    update_movies_file(movies)
    return movies[idx]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
