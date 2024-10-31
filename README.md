# user-crud
Python FastAPI RESTful API interface for User Database

## How to use:

The below commands will use docker to compose and start the application.
```
sh start.sh compose
sh start.sh start
```
Once started you can interact with the service by running the below command:
```
sh runner.sh
```
This will allow you to run CRUD operations on the service.

The service is currently running on FastAPI and utilizes Redis but can easily be migrated to use SQL services - Postgres is currently integrated.
Given the limited use case, Redis is the most straightforward to use here.

Once the service is running you can also check the API documentation by going to [http://localhost:8000/docs].

The current CI/CD pipeline in place utilizes Github Actions and is designed to check unit tests upon PR creation. This can and should be extended to include things like, test coverage, pylint or sonarqube and security checks.

Once this application is ready to deploy, additional workflows can be added to create the docker images and push them to a service like AWS ECR in order to run them in a cloud environment. 


For observability, logging can and should be added to the service using the builtin python Logger for basic structured logging.

Performance based logging was added and can be scraped via the ```GET /metrics``` endpoint



