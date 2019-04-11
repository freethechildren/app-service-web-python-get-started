# docker rm -fv sample-flask ; docker build --tag sample-flask --no-cache . && winpty docker run --rm -it --tty --publish 5000:80 --name sample-flask sample-flask

# docker rm -fv sample-django
FROM python:3.7-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "/app/application.py"]