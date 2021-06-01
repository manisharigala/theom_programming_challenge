import os,json,requests,time

coreName=os.environ['CORE_NAME']
solrAddress=os.environ['SOLR_ADDRESS']


def getSolrFields():
    resp = requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/schema/fields?wt=json")
    fields = json.loads(resp.text)['fields']
    return fields

def createNewFieldsFromFileContent(fields, doc):
    #checking out what fields to create
    toCreate=[]
    existingFields=set()
    for i in fields:
        if i['name'] in doc:
            existingFields.add(i['name'])
    for i in doc:
        if i not in existingFields:
            curField={}
            curField["name"]=str(i)
            curField["type"]="text_general"
            curField["indexed"]=str(i) != 'raw'
            curField["stored"]=True
            toCreate.append(curField)
    
    data = {
        "add-field": toCreate
    }
    if len(toCreate) != 0:
        res=requests.post("http://"+solrAddress+":8983/solr/"+coreName+"/schema",str(data))



def createDocInSOLR(doc):
    headers={"Content-Type":"application/json"}
    docs=[{k:v for k,v in doc.items()}]
    res=requests.post("http://"+solrAddress+":8983/solr/core1/update?commit=true",str(docs),headers=headers)
    print(res.text)



def waitForSolrStartup():
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