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
- All search operations are case insensitive.
- Results are displayed for partial match too.
- Max. of 10 documents displayed after searching

## Design and Implementation
The solution is implemented via five components in docker containers conforming to a micro-service architecture as shown in the architecture diagram. 
1. **UI Server** : The User Interface is built using React.js to make the application available to the cliens. The client can upload documents (JSON/text) using file upload button. The client can search text using a search bar with option of choosing from a list of indexed fields or all indexed fields.
2. **REST Server** : The REST Server is built using Flask. Clients submit GET/POST request via the front end which are mapped to the REST Server. Based on request type, API calls are made to concerned micro-service. Failure and exception handling is implemented.
3. **Rabbit MQ** : Keeping in mind to build a scalable and fault tolerant solution, Rabbit MQ is utilized as a messaging queue for write process of documents. Also, this is particularly helpful in order to not keep the client waiting during situations of long backend processing times. The documents to be uploaded are pushed to the Rabbit MQ. the consumer(Write Server) continuosly polls for new documents and completes the operation of indexing.
4. **Write Server** : The consumer(Write Server) continuosly polls for new documents in Rabbit MQ and completes the operation of inserting into Solr.
5. **Solr** : Open source framework to index and search documents based on provided configurations. ElasticSearch was another popular option, however its better suits for streaming and timeseries data. Solr, better fits this project's use case. If the input document is JSON, all the fields are indexed and if the input document is txt, then its converted to JSON format by creating a text field that is indexed and all the text data is stored as value. Documents can be persisted and queried via SDK APIs which are then relayed back to the client.


## Architecture Diagram
![alt text](https://github.com/manisharigala/theom_programming_challenge/blob/main/Images/architecture.png)

## Dependencies

| Dependency    | Link  |
| ------------- |-----:|
| Flask     |  https://flask.palletsprojects.com/en/2.0.x/ |
| Flask-CORS    | https://flask-cors.readthedocs.io/en/latest/ |
| Pika      | https://www.rabbitmq.com/tutorials/tutorial-one-python.html |
| Solr |  https://solr.apache.org/  |
| React.js | https://reactjs.org/ |
| RabbitMQ | https://www.rabbitmq.com/ |
| pipenv   | https://pypi.org/project/pipenv/ |
| unittest | https://docs.python.org/3/library/unittest.html |

## Deployment
All five docker containers are deployed to the same network (fulltextsearch) and would talk to each other via the container name (internal DNS lookup for actual IP address), this achieved via the docker compose file. All the docker images are built and then are uploaded to Docker hub(<https://hub.docker.com/u/marigala>). The docker compose file spawns all the containers. 

## API Documention

- **GET /**
    - Ping check to check REST Server is up
    - Request
        None
    - Response
        msg: String

- **POST /upload**
    - Upload a file to SOLR
    - Request
        file : File [ByteArray, {.json, .txt}]
    - Response
        status : Number [200 OK, 400 Bad Request]
    
- **POST /search**
    - Search key in docs and return list of matching docs
    - Request
        fields : String[] 
        key: String
    - Response
        docs : Object[]

- **GET /fields**
    - Get list of indexed fields in SOLR Schema from uploaded docs
    - Request 
        None
    - Response
        fields : Object[].

## Instructions to Invoke Application
1. Clone the github repository.
2. Open terminal in the root folder where the docker_compose.yaml file is present and run the following commands.
    * `docker-compose build`
    * `docker-compose up -d `
3. After the above commands are run and the services are spawned, please wait for about a minute because establishing connections to Solr and RabbitMQ might take a while.
4. After waiting for a minute, navigate to `localhost:3000` to go to the application,
5. Upload files using upload file buttion.
6. Select the search tab to go to the search section.
7. Select the index field to search on and enter the text to search in the search bar. Press Enter or click search icon to search.
8. You can view the raw document for each result by clicking on the down arrow.

## Unit Testing
1. Tested the entire application using Python's unittest framework.
2. The test.py file can be found at root/rest/test.py
3. To the run the unit tests, please go to the path of test.py in the terminal.
4. Make sure the docker containers are built and up.
5. Enter `pipenv install`.
6. Enter pipenv environment by entering `pipenv shell`.
7. Export environmental variales
    * `export RABBIT_ADDRESS=localhost`
    * `export CORE_NAME=core1`
    * `export SOLR_ADDRESS=localhost`
8. Run `python3 test.py`.



## Note
1. By default, four Sample JSON documents are inserted at the start of the application and the same files can be found at the root directory named **Initial_input_docs.zip**.
2. More sample docs can be found in **Sample_docs**
3. To view all documents present in Solr please select 'Any' in the field attribute and type '*' in search box and search.



