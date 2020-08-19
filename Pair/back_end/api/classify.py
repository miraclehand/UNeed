from flask_restful import Resource
from db.models import Classify
from utils.datetime import to_yyyymmdd

class ClassifyAPI(Resource):
    def __init__(self):
        super(ClassifyAPI, self).__init__()

    def get(self, id=None):
        #print('NodePairAPI', request.remote_addr)
        return {'items':[]}

    #add-task
    def post(self):
        print('ClassifyAPI post', request.remote_addr)

        date = to_yyyymmdd(datetime.now().today())
        #make_classify_model(date)
        return None

    #delete-task
    def delete(self):
        Classify.objects().delete()

