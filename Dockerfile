# docker rm -fv sample-django ; docker build --tag sample-django --no-cache . && winpty docker run --rm -it --tty --publish 5000:5000 --name sample-django sample-django

# docker rm -fv sample-django

# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/
COPY . .

# Install dependencies
# RUN pip install pipenv
# COPY ./Pipfile /code/Pipfile
# RUN pipenv install --system --skip-lock
RUN pip install -r requirements.txt

CMD ["python", "/app/flask_app.py"]