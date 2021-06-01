import json
ALLOWED_EXTENSIONS = ['json', 'txt']

def file_sanity_check(file):
    is_valid_format = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return is_valid_format

def getFileFormat(file):
    return file.filename.rsplit('.', 1)[1].lower()

def readFile(file):
    format = getFileFormat(file)
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
    return parsed