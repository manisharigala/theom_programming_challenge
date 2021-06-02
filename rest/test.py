
import json
from app import app
import unittest
from io import BytesIO, StringIO

#export CORE_NAME=core1
#export SOLR_ADDRESS=localhost
class FlaskTest(unittest.TestCase):

    # Check for Response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Check Upload file and verify filename
    def test_upload(self):
        tester = app.test_client(self)
        # Loading File
        with open('test_files/cali.json', 'rb') as file:
            fileStringIO = BytesIO(file.read())
        input_data = {
            'file': (fileStringIO, 'cali.json')
        }

        # Upload File
        response = tester.post('/upload', content_type='multipart/form-data', data=input_data) 
        self.assertEqual(response.status_code, 200)
        
        #verify if file is inserted into solr
        file_data = {
            "fields": ["filename"], 
            "key": "cali.json"
        }

        # verify file is uploaded
        response2 = tester.post('/search', data=json.dumps(file_data), headers={'Content-Type': 'application/json'}) 
        self.assertEqual(response2.status_code, 200)
        

    # Check Search content from uploaded files
    def test_search(self):
        tester = app.test_client(self)
        search_data = {
            "fields": ["Title"], 
            "key": "Monkey"
        }
        response = tester.post('/search', data=json.dumps(search_data), headers={'Content-Type': 'application/json'}) 
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(data["response"]["numFound"], 1)

    # Check get fields API
    def test_fields(self):
        tester = app.test_client(self)
        response = tester.get("/fields")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


    # Check invalid file input format
    def test_invalid_file_format(self):
        tester = app.test_client(self)
        # Loading File
        
        with open('test_files/usa.xml', 'rb') as file:
            fileStringIO = BytesIO(file.read())
        input_data = {
            'file': (fileStringIO, 'usa.xml')
        }
        # Upload File
        response = tester.post('/upload', content_type='multipart/form-data', data=input_data) 
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    
    unittest.main()