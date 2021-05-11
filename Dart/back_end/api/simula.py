from flask_restful import Resource
from flask import request
from db.models import User, Simula, UserSimula, Disc, StdDisc, Stats
from app import app
from util import write_log, str_to_date
from api.util import to_json
from constants import *
from bson import ObjectId
from task.singleton import pool_ohlcv
from task.mfg.reproduce import get_ohlcvs
from datetime import datetime

class SimulaAPI(Resource):
    def __init__(self):
        super(SimulaAPI, self).__init__()

    def get(self, cntry=None, usid=None, id=None):
        write_log(request.remote_addr,'simula get',cntry)

        user = User.objects.get({'email':usid})

        try:
            simulas = UserSimula.objects.get({'user':user._id}).simulas
        except:
            return {'simulas':[]}

        return {'simulas':to_json(list(simulas))}
    
    #update-task
    def put(self, cntry=None, usid=None, id=None):
        write_log(request.remote_addr,'simula put',cntry)

        data = request.get_json()
        new_data = data['simula']

        user = User.objects.get({'email':usid})
        try:
            simulas = UserSimula.objects.get({'user':user._id})
        except:
            return {'simulas':None}

        return {'simulas':to_json(list(simulas))}
        
    #add-task
    def post(self, cntry=None, usid=None, id=None):
        write_log(request.remote_addr,'user watch post',cntry)

        data = request.get_json()

        unit = data['unit']
        print(unit)

        user = User.objects.get({'email':usid})

        std_disc = StdDisc.objects.get({'id':unit['std_disc']['id']})
        unit['std_disc'] = std_disc
        s_date, e_date = unit['s_date'][:10], unit['e_date'][:10]

        user_simula = None
        try:
            user_simula = UserSimula.objects.get({'user':user._id})
        except:
            user_simula = UserSimula(user)

        std_disc = unit['std_disc']
        stock_codes = unit['stock_codes'].strip()

        if stock_codes == '000000':
            discs = Disc.objects.raw({
                'std_disc':std_disc._id,
            })
        else:
            stock_codes = stock_codes.split(' ')
            discs = Disc.objects.raw({
                'std_disc':std_disc._id,
                'stock_code':{'$in':stock_codes},
            })

        stats = [Stats(disc.corp, disc, get_ohlcvs(disc)) for disc in discs]

        new_simula = Simula(unit, s_date, e_date, stats)
        new_simula.save()

        user_simula.add_simula(new_simula)
        user_simula.save()

        return {'simula':to_json(new_simula)}

    #delete-task
    def delete(self, cntry=None, usid=None):
        write_log(request.remote_addr,'user simula delete',cntry)
        print('delete', cntry, usid)

        data = request.get_json()

        #print('data', data)
        unit = data['unit']
        #print('unit', unit)
        user = User.objects.get({'email':usid})
        user_simula = UserSimula.objects.get({'user':user._id})
        user_simula.del_simula(unit)
        user_simula.save()

