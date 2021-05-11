from flask_restful import Resource
from flask import request
from db.models import StdDisc, Disc
from constants import *

class ContAPI(Resource):
    def __init__(self):
        super(ContAPI, self).__init__()

    def get(self, cntry=None, keyword=None):
        pass

    #update-task
    def put(self, cntry=None, begin=None, end=None, keyword=None):
        write_log(request.remote_addr,'cont put',cntry, begin, end, keyword)

        std_disc = StdDisc.objects.raw({'keyword':keyword})
        if std_disc.count() == 0:
            return
        discs = Disc.objects.raw({'rcept_dt':{'$gte':begin, '$lte':end}, 'std_disc':std_disc._id}).order_by([('rcept_dt':1)])

        for disc in discs:
            print(disc.content)
            disc.save()


    
    #add-task
    def post(self, cntry=None, keyword=None):
        write_log(request.remote_addr,'cont post',cntry)

    #delete-task
    def delete(self, cntry=None, keyword=None):
        pass

