Name: Aileen Huang
NetID: aeh245

Challenges Attempted (Tier I/II/III):
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: 
https://hub.docker.com/repositories/aeh245

Questions:
Explain the concept of containerization in your own words.
Containerization is the process of compressing together code, dependencies,
 so our app can run in different environments. 

What is the difference between a Docker image and a Docker container?
A Docker image serves as the 'blueprint' for running our app: Images are built according
to the Dockerfile from source code and dependencies. A Docker container is the what the 
Docker image is run as aka a 'live instance of application'. 
We build images, and run images as containers. 

What is the command to list all Docker images?
docker images

What is the command to list all Docker containers?
docker ps

What is a Docker tag and what is it used for?
A Docker tag is used to identify a Docker image. For instance, the Docker tag 
I created was aeh245/demos5:v1

What is Docker Hub and what is it used for?
Docker Hub is a place to push and pull Docker images to run on isolated servers.

What is Docker compose used for?
Docker compose is associated with of running applications of a single
or mulit-container applications. We can make a yaml file for this.  

What is the difference between the RUN and CMD commands?
RUN installs the libraries/modules and constructs the environments. 
CMD refers to the 'main function' or code that is executed. 