from solr import getDocuments, getSchemaFields
from rabbit import connectToRabbitMQ, publishToQueue
from file_utils import file_sanity_check, readFile
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello_world():
    return 'Theom.ai programming challenge - Searching and Indexing'

# API to upload a document into SOLR for indexing 
@app.route('/upload', methods = ['POST'])
@cross_origin()
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return make_response("Bad Request",400)
    file = request.files['file']
    # check file file is of correct format 
    sanityStatus = file_sanity_check(file)
    if sanityStatus:
        print("HERE 1")
        parsed = readFile(file)
        print("HERE 2")
        publishToQueue('upload', str(parsed))
        print("HERE 3")
        return make_response("Upload success ==" + str(parsed),200)
    else:
        return make_response("File format not in required format",400)

# API to search documents from SOLR based on search key
@app.route('/search' , methods = ['POST'])
@cross_origin()
def search():
    fields=request.json['fields']
    key=request.json['key']
    for i in range(len(fields)):
        fields[i] = fields[i] + ":*" + key + "*"
    query = ' OR '.join(fields)
    limit = "10"
    resp = getDocuments(query, limit)
    return make_response(jsonify(resp),200)

# API to get all fields in the SOLR schema (UI Specific)
@app.route('/fields')
@cross_origin()
def getFields():
    fields = getSchemaFields()
    return make_response(jsonify(fields),200)

if __name__ == "__main__":
    app.run("0.0.0.0", port=3001, debug=True)
    ch = connectToRabbitMQ()
