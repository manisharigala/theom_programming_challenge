import pika, sys, os,json,requests,time
import os
def callback(ch, method , properties, body):
    print("inside callback 1")
    # print(properties,method)
    #parsing message request
    frequest=json.loads(body)
    print(frequest)
    # req=json.loads(body)
    typ=frequest['__type']
    del frequest['__type']
    req=frequest
    #Fetching the schema
    print("inside callback 2")
    
    coreName=os.environ['CORE_NAME']
    solrAddress=os.environ['SOLR_ADDRESS']

    # coreName="core1"
    # solrAddress="localhost"
    resp = requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/schema/fields?wt=json")
    
    print("inside callback 3")

    # #Fetching the fields

    fields = json.loads(resp.text)['fields']
    print(fields)

    print("inside callback 4")

    #checking out what fields to create
    toCreate=[]
    existingFields=set()
    for i in fields:
        if i['name'] in req:
            existingFields.add(i['name'])
    for i in req:
        if i not in existingFields:
            curField={}
            curField["name"]=str(i)
            curField["type"]="text_general"
            curField["indexed"]=str(i) != 'raw'
            curField["stored"]=True
            toCreate.append(curField)
    # print(toCreate)
    # #creating the fields
    data = {
    "add-field": toCreate
        }

    print("inside callback 5")
    
    # print(data)
    if len(toCreate)!=0:
        res=requests.post("http://"+solrAddress+":8983/solr/"+coreName+"/schema",str(data))
        print(res)
    


    print("inside callback 6")

    # print(req)
    #inserting documents

    headers={"Content-Type":"application/json"}

    


    docs=[{k:v for k,v in req.items()}]
    print(docs)
    print("inside callback 7")

    res=requests.post("http://"+solrAddress+":8983/solr/core1/update?commit=true",str(docs),headers=headers)
    print("inside callback 8")

    print(res.text)


def main():
    connection,channel=None,None
    count=0
    while True:
        try:
            # check for solr
            coreName=os.environ['CORE_NAME']
            solrAddress=os.environ['SOLR_ADDRESS']
            # coreName="core1"
            # solrAddress="localhost"
            res=requests.get("http://"+solrAddress+":8983/solr/admin/cores?action=STATUS&core="+coreName+"&wt=json")
            p = json.loads(res.text)['status'][coreName]['uptime']
            break
        except:
            print("trying to connect to SOLR.....")
            if count>10:
                raise Exception("Cannot establish connection to SOLR!")
                exit(0)
            time.sleep(5)
            count+=1
            continue
    print("connected to SOLR")
    
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_ADDRESS']))
            # connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            break
        except:
            print("trying to connect to rabbit.....")
            if count>5:
                raise Exception("Cannot establish connection to Rabbit!")
                exit(0)
            time.sleep(5)
            count+=1
            continue
    print("connected to Rabbit")
    #read 4 files and call callback(None,None,None, data)
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

    channel.queue_declare(queue=os.environ["QUEUE_NAME"])

 
        
        # print(toCreate)


        # print(req)
        # print(" [x] Received %r" % body)


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