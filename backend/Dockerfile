#backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Expose backend port
EXPOSE 8000

#Use bash script to start FastAPI
CMD [ "bash", "run.sh" ]
