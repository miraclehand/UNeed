from pymongo import ASCENDING, DESCENDING
from pymongo.operations import IndexModel
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from util import getDisassembled

#https://pymodm.readthedocs.io/en/latest/index.html
#https://github.com/mongodb/pymodm/tree/master/example/blog

# Establish a connectin to database.
connect('mongodb://localhost:27017/dart', alias='dart')

def extract(newone, key):
    return newone[key] if key in newone else ''

class User(MongoModel):
    name      = fields.CharField()
    email     = fields.CharField()
    pushToken = fields.CharField()
    level     = fields.IntegerField()

    def __init__(self, name=None,email=None,pushToken=None,level=None,**kwargs):
        super().__init__(**kwargs)

        self.name      = name
        self.email     = email 
        self.pushToken = pushToken
        self.level     = level

    class Meta:
        collection_name = 'user'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'name'      : self.name,
            'email'     : self.email,
            'pushToken' : self.pushToken,
            'level'     : self.level,
        }

class Corp(MongoModel):
    corp_code   = fields.CharField()
    corp_name   = fields.CharField()
    stock_code  = fields.CharField()
    modify_date = fields.CharField()

    #_mongometa.object_name = 'db.models.Corp'
    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return

        if isinstance(newone, dict):
            self.corp_code   = newone['corp_code']
            self.corp_name   = newone['corp_name']
            self.stock_code  = newone['stock_code']
            self.modify_date = newone['modify_date']
        else:
            self.corp_code   = newone.findtext('corp_code')
            self.corp_name   = newone.findtext('corp_name')
            self.stock_code  = newone.findtext('stock_code')
            self.modify_date = newone.findtext('modify_date')

    class Meta:
        collection_name = 'corp'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('corp_code',ASCENDING)], name='corp_corp_code')
        ]

    @property
    def to_dict(self):
        return {
            'corp_code'   : self.corp_code,
            'corp_name'   : self.corp_name,
            'stock_code'  : self.stock_code,
            'modify_date' : self.modify_date,
            'url'         : f'http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A{self.stock_code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=&strResearchYN='
        }

class StdDisc(MongoModel):
    id         = fields.IntegerField()
    report_nm  = fields.CharField()
    report_dnm = fields.CharField()

    def __init__(self, id=None, report_nm=None, **kwargs):
        super().__init__(**kwargs)

        self.id = id
        self.report_nm  = report_nm
        self.report_dnm = getDisassembled(report_nm)

    class Meta:
        collection_name = 'std_disc'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'id'        : self.id,
            'report_nm' : self.report_nm,
            'report_dnm': self.report_dnm,
        }

#Disclosure Information
class Disc(MongoModel):
    std_disc   = fields.ReferenceField(StdDisc)
    rcept_dt   = fields.CharField()
    reg_time   = fields.CharField()
    corp_cls   = fields.CharField()
    corp       = fields.ReferenceField(Corp)
    stock_code = fields.CharField()
    rcept_no   = fields.CharField()
    report_nm  = fields.CharField()
    flr_nm     = fields.CharField()
    rm         = fields.CharField()
    tick       = fields.IntegerField()
    content    = fields.CharField()
    url        = fields.CharField()

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        self.std_disc   = extract(newone, 'std_disc')
        self.rcept_dt   = extract(newone, 'rcept_dt')
        self.reg_time   = extract(newone, 'reg_time')
        self.corp       = extract(newone, 'corp')
        self.corp_cls   = extract(newone, 'corp_cls')
        self.stock_code = self.corp.stock_code
        self.rcept_no   = extract(newone, 'rcept_no')
        self.report_nm  = extract(newone, 'report_nm')
        self.flr_nm     = extract(newone, 'flr_nm')
        self.rm         = extract(newone, 'rm')
        self.tick       = extract(newone, 'tick')
        self.content    = extract(newone, 'content')
        self.url        = extract(newone, 'url')

    class Meta:
        collection_name = 'disc'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('rcept_dt',DESCENDING),('reg_time',DESCENDING),('rcept_no',DESCENDING)], name='disc_lastest'),
        ]

    @property
    def to_dict(self):
        return {
            '_id'       : str(self._id),
            'std_disc'  : self.std_disc,
            'rcept_dt'  : f'{self.rcept_dt[0:4]}/{self.rcept_dt[4:6]}/{self.rcept_dt[6:8]}',
            'reg_time'  : self.reg_time,
            'corp_cls'  : self.corp_cls,
            'corp_code' : self.corp.corp_code,
            'corp_name' : self.corp.corp_name,
            'stock_code': self.corp.stock_code,
            'rcept_no'  : self.rcept_no,
            'report_nm' : self.report_nm,
            'flr_nm'    : self.flr_nm,
            'rm'        : self.rm,
            'tick'      : self.tick,
            'content'   : self.content,
            'url'       : self.url,
        }

class NewDisc(Disc):
    class Meta:
        collection_name = 'new_disc'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('rcept_dt',DESCENDING),('reg_time',DESCENDING),('rcept_no',DESCENDING)], name='disc_lastest'),
        ]

class UserDisc(MongoModel):
    user = fields.ReferenceField(User)
    user_discs = fields.EmbeddedDocumentListField(Disc, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        if user is None:
            return
        self.user = user
        
    class Meta:
        collection_name = 'user_disc'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'user_discs'   : list(self.user_discs),
        }

class UnitDetail(EmbeddedMongoModel):
    name       = fields.CharField()
    qty        = fields.IntegerField()
    
    def __init__(self, name = None, qty = None, **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.qty  = qty

    @property
    def to_dict(self):
        return {
            'name' : self.name,
            'qty'  : self.qty,
        }

class Unit(MongoModel):
    name        = fields.CharField()
    stocks      = fields.ListField()
    stock_codes = fields.CharField()
    stock_names = fields.CharField()
    std_disc    = fields.ReferenceField(StdDisc)
    detail      = fields.EmbeddedDocumentField(UnitDetail)

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        
        self.name        = extract(newone, 'name')
        self.stocks      = extract(newone, 'stocks')
        self.stock_codes = extract(newone, 'stock_codes')
        self.stock_names = extract(newone, 'stock_names')
        self.std_disc    = extract(newone, 'std_disc')
        #self.detail      = extract(newone, 'detail')
        self.detail      = UnitDetail(self.name, 10)

    @property
    def to_dict(self):
        return {
            '_id'    : str(self._id),
            'name'   : self.name,
            'stocks' : list(self.stocks),
            'stock_codes' : self.stock_codes,
            'stock_names' : self.stock_names,
            'std_disc'    : self.std_disc,
            'detail'      : self.detail
        }

class Watch(Unit):
    def __init__(self, new_unit=None, **kwargs):
        super().__init__(new_unit, **kwargs)

    class Meta:
        collection_name = 'watch'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return super().to_dict

class Stats(EmbeddedMongoModel):
    # 삼성전자
    # 공시일자, 공시원문주소
    # 수익률
    corp = fields.ReferenceField(Corp)
    disc = fields.EmbeddedDocumentField(Disc)
    closeBf30 = fields.FloatField()
    closeBf7  = fields.FloatField()
    close     = fields.FloatField()
    closeAf7  = fields.FloatField()
    closeAf30 = fields.FloatField()

    def __init__(self, corp=None, disc = None, ohlcvs = None, **kwargs):
        super().__init__(**kwargs)

        if ohlcvs is None:
            return
        self.corp = corp
        self.disc = disc

        self.closeBf30 = ohlcvs[0].close.values[0]
        self.closeBf7  = ohlcvs[1].close.values[0]
        self.close     = ohlcvs[2].close.values[0]
        self.closeAf7  = ohlcvs[3].close.values[0]
        self.closeAf30 = ohlcvs[4].close.values[0]

    @property
    def to_dict(self):
        return {
            'corp'   : self.corp,
            'disc'   : self.disc,
            'closeBf30': self.closeBf30,
            'closeBf7' : self.closeBf7,
            'close'    : self.close,
            'closeAf7' : self.closeAf7,
            'closeAf30': self.closeAf30,
        }


class Simula(Unit):
    s_date = fields.CharField()
    e_date = fields.CharField()

    #result
    prrt   = fields.FloatField()
    stats  = fields.EmbeddedDocumentListField(Stats, default=[])

    def __init__(self, unit=None,s_date=None,e_date=None,stats=None,**kwargs):
        super().__init__(unit, **kwargs)

        self.s_date = s_date
        self.e_date = e_date
        self.stats  = stats
        self.prrt = 0

    class Meta:
        collection_name = 'simula'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        simula = super().to_dict
        simula['s_date'] = self.s_date
        simula['e_date'] = self.e_date
        simula['prrt']   = self.prrt
        simula['stats']  = list(self.stats)

        return simula

def add_unit(units, new_unit):
    if not units:
        units.insert(0, new_unit)
        return
            
    for i, unit in enumerate(units):
        if unit.name > new_unit.name:
            units.insert(i, new_unit)
            return
    units.append(new_unit)

def del_watch(units, del_unit):
    if not units:
        return
    for i, unit in enumerate(units):
        if str(unit._id) == str(del_unit['_id']):
            del units[i]
            break

class UserWatch(Unit):
    user     = fields.ReferenceField(User)
    watchs   = fields.EmbeddedDocumentListField(Watch, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_watch(self, new_watch):
        add_unit(self.watchs, new_watch)

    def del_watch(self, del_watch):
        del_unit(self.watchs, del_watch)

    class Meta:
        collection_name = 'user_watch'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'watchs' : self.watchs,
        }
        
class UserSimula(Unit):
    user     = fields.ReferenceField(User)
    simulas  = fields.EmbeddedDocumentListField(Simula, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user
    
    def add_simula(self, new_simula):
        add_unit(self.simulas, new_simula)

    def del_simula(self, del_simula):
        del_unit(self.simulas, del_simula)

    class Meta:
        collection_name = 'user_simula'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'simulas' : self.simulas,
        }
        
"""
class UserWatch(MongoModel):
    user     = fields.ReferenceField(User)
    watchs   = fields.EmbeddedDocumentListField(Watch, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_watch(self, new_watch):
        if not self.watchs:
            self.watchs.insert(0, new_watch)
            return
            
        for i, watch in enumerate(self.watchs):
            if watch.name > new_watch.name:
                self.watchs.insert(i, new_watch)
                return
        self.watchs.append(new_watch)

    def del_watch(self, del_watch):
        if not self.watchs:
            return
        for i, watch in enumerate(self.watchs):
            if str(watch._id) == str(del_watch['_id']):
                del self.watchs[i]
                break

    class Meta:
        collection_name = 'watch_kr'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('user',ASCENDING)], name='watch_user')
        ]

    @property
    def to_dict(self):
        return {
            'watchs' : list(self.watchs),
        }
"""

class Room(EmbeddedMongoModel):
    watch         = fields.ReferenceField(Watch)
    discs         = fields.EmbeddedDocumentListField(Disc, default=[])
    #disc          = fields.ReferenceField(Disc)
    #last_message  = fields.ReferenceField(Message)

    def __init__(self, watch=None, **kwargs):
        super().__init__(**kwargs)

        self.watch = watch

    @property
    def to_dict(self):
        return {
            'watch_id' : str(self.watch._id),
            'watch_name' : self.watch.name,
            'last_disc_id' : str(self.discs[-1]._id),
            'last_disc_label' : self.discs[-1].corp.corp_name,
        }

class Alert(MongoModel):
    user     = fields.ReferenceField(User)
    rooms    = fields.EmbeddedDocumentListField(Room, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_or_replace_room(self, newone):
        for i, room in enumerate(self.rooms):
            if room.watch._id != newone.watch._id:
                continue
            del self.rooms[i]
            break
        self.rooms.insert(0, newone)

    class Meta:
        collection_name = 'alert'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            '_id' : str(self._id),
            'rooms' : list(self.rooms),
        }

"""
class Simula(MongoModel):
    #cond
    unit   = fields.EmbeddedDocumentField(Unit, default=[])

    #result
    prrt   = fields.FloatField()

    stats  = fields.EmbeddedDocumentListField(Stats, default=[])

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return
        
        self.unit        = extract(newone, 'name')
        self.s_date      = ' '
        self.e_date      = ' '
        self.stock_codes = extract(newone, 'stock_codes')
        self.stock_names = extract(newone, 'stock_names')
        self.std_disc    = extract(newone, 'std_disc')
        #self.detail      = extract(newone, 'detail')
        self.detail      = UnitDetail(self.name, 10)

    class Meta:
        collection_name = 'simula'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'unit'    : self.unit,
            'stats'   : list(self.stats),
        }

class UserSimula(MongoModel):
    user    = fields.ReferenceField(User)
    simulas = fields.EmbeddedDocumentListField(Simula, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_simula(self, new_simula):
        if not self.simulas:
            self.simulas.insert(0, new_simula)
            return
            
        for i, simula in enumerate(self.simulas):
            if simula.name > new_simula.name:
                self.simulas.insert(i, new_simula)
                return
        self.simulas.append(new_simula)

    def del_simula(self, del_simula):
        if not self.simulas:
            return
        for i, simula in enumerate(self.simulas):
            if str(simula._id) == str(del_simula['_id']):
                del self.simulas[i]
                break

    class Meta:
        collection_name = 'user_simula'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'simulas' : list(self.simulas),
        }

"""
