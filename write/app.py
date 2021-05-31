import pika, sys, os,json,requests

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
    channel = connection.channel()

    channel.queue_declare(queue="upload")

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
        coreName="core1"
        resp = requests.get("http://solr:8983/solr/core1/schema/fields?wt=json")
        

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
                curField["type"]="string"
                curField["indexed"]=True
                curField["stored"]=True
                toCreate.append(curField)
        print("******")
        # print(toCreate)
        # #creating the fields
        data = {
        "add-field": toCreate
            }
        
        # print(data)
        if len(toCreate)!=0:
            res=requests.post("http://solr:8983/solr/core1/schema",str(data))
            print(res)
        


        # print(req)
        #inserting documents

        headers={"Content-Type":"application/json"}

        


        docs=[{k:v for k,v in req.items()}]
        print(docs)
    
        res=requests.post("http://solr:8983/solr/core1/update?commit=true",str(docs),headers=headers)

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