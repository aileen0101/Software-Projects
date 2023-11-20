FROM python:3.9

 #run command in docker terminal
RUN mkdir usr/app

#create directory - working in this directory, copy code into here
WORKDIR usr/app

COPY . . 

#install python modules, building environment

RUN pip3 install -r requirements.txt

#running main application
CMD python3 app.py