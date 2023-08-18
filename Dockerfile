# pull python 3.9
FROM python:3.9-alpine

# set work directory in the container
WORKDIR /usr/src/app

#Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

#copy project requirements to the /usr/src/app in container
COPY ./requirements.txt .
#install requiremnets
RUN pip install -r requirements.txt


#copy all the project files to the /usr/src/app in container
copy . .