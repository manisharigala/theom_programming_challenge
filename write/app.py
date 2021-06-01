
from rabbit import getRabbitChannel
from solr import getSolrFields, createNewFieldsFromFileContent, createDocInSOLR, waitForSolrStartup
import sys,os,json

#callback function executed when a message is pulled out of the write queue
def callback(ch, method , properties, body):
    doc=json.loads(body)
    print(doc)
    # req=json.loads(body)
    typ=doc['__type']
    del doc['__type']
    #Fetching the fields in SOLR Schema
    fields = getSolrFields()
    #create fields from doc that don't already exist in schema
    createNewFieldsFromFileContent(fields, doc)
    #add the document to SOLR
    createDocInSOLR(doc)

def main():
    #wait for SOLR instance to be UP
    waitForSolrStartup()

    #read 4 files from sample folder and add them to SOLR as initial docs
    path = os.getcwd() + '/sample'
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            content = f.read()
            parsed = json.loads(content)
            print(parsed)
            parsed["raw"] = str(parsed)
            parsed["__type"]="json"
            parsed["filename"] = filename
            parsed=json.dumps(parsed)
            callback(None, None, None, parsed)
    print("created sample files")
    
    #Connect to Rabbit MQ - 'upload' queue 
    channel = getRabbitChannel()
    channel.queue_declare(queue=os.environ["QUEUE_NAME"])
    channel.basic_consume(queue='upload', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)