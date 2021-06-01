from flask import Flask, request, jsonify, make_response
import json,requests,os
import pika
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = ['json', 'txt']

def file_sanity_check(file):
    is_valid_format = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return is_valid_format, file.filename.rsplit('.', 1)[1].lower()


@app.route('/')
@cross_origin()
def hello_world():
    return 'Theom.ai programming challenge - Searching and Indexing'

@app.route('/upload', methods = ['POST'])
@cross_origin()
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return make_response("Bad Request",400)
    file = request.files['file']
    sanity, format = file_sanity_check(file)
    if sanity:
        #push to MQ
        content = file.read()
        parsed = None
        if(format == 'json'):
            parsed = json.loads(content)
            parsed["raw"] = str(parsed)
            parsed["__type"]="json"
            parsed["filename"] = file.filename
            parsed=json.dumps(parsed)
            # print(parsed)
        else:
            parsed = {"Text": content.decode("utf-8"),"__type":"text"}
            parsed["raw"] = content.decode("utf-8")
            parsed["filename"] = file.filename
            parsed=json.dumps(parsed)
        #

        connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_ADDRESS']))
        channel = connection.channel()
        channel.queue_declare(queue='upload')
        channel.basic_publish(exchange='',
                      routing_key='upload',
                      body=str(parsed))
        return make_response("Upload success ==" + str(parsed),200)
    else:
        return make_response("File format not in required format",400)


@app.route('/search' , methods = ['POST'])
@cross_origin()
def search():
    coreName=os.environ["CORE_NAME"]
    solrAddress=os.environ["SOLR_ADDRESS"]
    fields=request.json['fields']
    key=request.json['key']
    for i in range(len(fields)):
        fields[i] = fields[i] + ":*" + key + "*"
    query = ' OR '.join(fields)
    limit = "10"
    res=requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/select?q="+query+"&wt=json"+"&rows="+limit)
    return make_response(jsonify(json.loads(res.text)),200)


@app.route('/fields')
@cross_origin()
def getFields():
    coreName=os.environ["CORE_NAME"]
    solrAddress=os.environ["SOLR_ADDRESS"]
    resp = requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/schema/fields?wt=json")
    fields = json.loads(resp.text)['fields']
    return make_response(jsonify(fields),200)

if __name__ == "__main__":
    app.run("0.0.0.0", port=3001, debug=True)
