import express from "express";

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const movies = [
  { id: 1740528382134, name: "Some movie 1", watched: false },
  { id: 1740528382135, name: "Some movie 2", watched: true },
  { id: 1740528382136, name: "Some movie 3", watched: false },
];

app.get("/movies", (req, res) => {
  res.status(200).json(movies);
});

app.get("/movies/:id", (req, res, next) => {
  const id = Number(req.params.id);
  const movieTarget = movies.find((movie) => movie.id === id);
  if (!movieTarget) {
    const err = { status: 404, message: `Movie with the id ${id} is not found.` };
    return next(err);
  }
  res.status(200).json(movieTarget);
});

app.post("/movies", (req, res, next) => {
  console.log(req.headers);
  const id = Date.now();
  const { name, watched = false } = req.body;
  const isExist = movies.find((movie) => movie.name === name);
  if (isExist) {
    const err = { status: 400, message: `Movie with the name ${name} already exists.` };
    return next(err);
  }
  const newMovie = {
    id,
    name,
    watched,
  };
  movies.push(newMovie);
  res.status(200).json(movies);
});

app.put("/movies", (req, res, next) => {
  const id = Number(req.query.id);
  const watched = req.query.watched || false;
  console.log(req.query);
  const idx = movies.findIndex((movie) => movie.id === id);
  if (idx === -1) {
    const err = { status: 404, message: `Movie doesn't exist with id ${id}.` };
    return next(err);
  }
  movies[idx] = { ...movies[idx], watched };
  res.status(201).json(movies);
});

// global error handler
app.use((err, req, res, next) => {
  const { status = 500, message = "Some error occured" } = err;
  res.status(status).json({ message });
});

app.listen(3000, () => console.log("App is running on 3000..."));
