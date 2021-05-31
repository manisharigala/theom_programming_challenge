# Programming Challenge - Indexing And Search

## Goal
Design and develop a micro-service web application to store, parse, index and query documents (JSON/text). The client can interact with the application via a simple front end interface that communicates with the backend APIs. While writes can be expesnisve operations, read must be quick for any input text/phrase query to fetch most relevant documents found within the storage.

## Assumptions
Below mentioned points pertain to the certain assumptions and/or constraints:
- No more than 100 files can be indexed.
- Each JSON file will be UTF-8 encoded and not exceed 10 MB.
- POST API is not a bulk upload but rather a single file upload operation.
- Any existing open source solutions can be leverage for indexing and searching text within documents.
- Solution is to be deployed via Docker containers.

## Design and Implementation
The solution is implemented via three docker containers conforming to a micro-service architecture. Flask is is used an API layer while Solr indexes documents with respect to a pre-defined schema.
1. **REST Controller** : Clients submit GET/POST request via the front end which are mapped to the REST controller. Based on request type, API calls are made to concerned micro-service. Failure and exception handling is implemented.
2. **Rabbit MQ** : Keeping in mind to build a scalable and fault tolerant solution, Rabbit MQ is utilized as in intermediate messaging queue for indexing documents. Also, this is particularly helpful in order to not keep the client waiting during situations of long backend processing times. A consumer continuosly polls for new messages and completes the operation of indexing.
3. **Solr Indexing** : Open source framework to index documents based on provided configurations. Documents can be persisted and queried via SDK APIs which are then relayed back to the client.

<<<**INSERT DIAGRAM**>>>

## Dependencies
<<<Add info on imported packages like Flask, RMQ, Solr etc, along with version numbers and any useful links>>>
| Dependency    | Version   | Link  |
| ------------- |:-------------:|:-----:|
| Flask     | .... | https://flask.palletsprojects.com/en/2.0.x/ |
| Pika      | ..... | https://www.rabbitmq.com/tutorials/tutorial-one-python.html |
| Solr | .... |    $1 |

## Deployment
All three docker containers are deployed to the same network and would talk to each other via the container name (internal DNS lookup for actual IP address), this achieved via settings configured within the docker file.
### REST Docker
Add command to invoke docker
```
command
```

### RMQ Docker
Add command to invoke docker
```
command
```

### Solr Docker
Add command to invoke docker
```
command
```
**High level Solr Configuration**
......

## API Documention

- **GET /**
    - Landing page, dummy.
- **POST /upload**
    - Upload JSON ot TXT file that is to be indexed for efficient search operations.
    - Data is uploaded via a form on the frontend where body contains the input fie contents.
    - Return a sucess `200 OK` once data is publihed to Rabbit MQ.
    
- **GET /search**
    - Request body will contain the "query" as the key with value being the "Solr search query" that is to be executed.
    - Return `200 OK` on sucess, `500` on Invalid Query

