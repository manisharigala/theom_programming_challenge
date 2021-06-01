import json,requests,os

coreName=os.environ["CORE_NAME"]
solrAddress=os.environ["SOLR_ADDRESS"]


def getDocuments(query, limit):
    res=requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/select?q="+query+"&wt=json"+"&rows="+limit)
    return json.loads(res.text)

def getSchemaFields():
    resp = requests.get("http://"+solrAddress+":8983/solr/"+coreName+"/schema/fields?wt=json")
    return json.loads(resp.text)['fields']