import pika, sys, os,json,requests,time

def main():
    connection,channel=None,None
    count=0
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_ADDRESS']))
            channel = connection.channel()
            break
        except:
            print("trying.....")
            if count>5:
                raise Exception("Cannot establish connection!")
                exit(0)
            time.sleep(2)
            count+=1
            continue

    channel.queue_declare(queue=os.environ["QUEUE_NAME"])

    def callback(ch, method, properties, body):


        print(properties,method)

        #parsing message request
        frequest=json.loads(body)
        print(frequest)
        # req=json.loads(body)

        typ=frequest['__type']

        del frequest['__type']
        req=frequest

        #Fetching the schema
        
        coreName=os.environ['CORE_NAME']
        solrAddress=os.environ['SOLR_ADDRESS']
        resp = requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/schema/fields?wt=json")
        

        # #Fetching the fields

        fields = json.loads(resp.text)['fields']
        # print(fields)


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
        
        # print(data)
        if len(toCreate)!=0:
            res=requests.post("http://"+solrAddress+":8983/solr/"+coreName+"/schema",str(data))
            print(res)
        


        # print(req)
        #inserting documents

        headers={"Content-Type":"application/json"}

        


        docs=[{k:v for k,v in req.items()}]
        print(docs)
    
        res=requests.post("http://"+solrAddress+":8983/solr/core1/update?commit=true",str(docs),headers=headers)

        print(res.text)
        
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