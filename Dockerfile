FROM python:3.9

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install "fastapi[standard]"

EXPOSE 8000

CMD ["fastapi", "dev", "main.py"]