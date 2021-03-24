from flask import Flask,Response,request,json
from flask_pymongo import MongoClient
import logging as log
from bson.json_util import dumps

app = Flask(__name__)

class MongoAPI:
    def __init__(self,data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        #self.client = MongoClient("mongodb://localhost:27017/")
        self.client = MongoClient("mongodb://mymongo:27017/")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        log.info("Showing all Data")
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self,data):
        log.info("Writing Data")
        new_doc = data['Document']
        response = self.collection.insert_one(new_doc)
        output = {'Status':'Inserted Successfully','ID':str(response.inserted_id)}
        return output
@app.route('/')
def base():
    return Response(response=json.dumps({'Status':'UP'}),
                    status=200,
                    mimetype='application/json')

@app.route('/get_records',methods=['GET'])
def retrieve_all():
    data =request.json
    if data is None or data =={}:
        return Response(response=json.dumps({"Error":"Please provide connection info"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/get_records',methods=['POST'])
def add_employee():
    data = request.json
    if data is None or data =={} or 'Document' not in data:
        return Response(response=json.dumps({"Error":"Please provide connection info"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

'''
def hello():
    return 'Connected Successfully! '
'''
if __name__ == '__main__':
    app.run(debug=True,port=5002,host='0.0.0.0')