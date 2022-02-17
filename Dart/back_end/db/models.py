from datetime import datetime
from pymongo import ASCENDING, DESCENDING
from pymongo.operations import IndexModel
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from pytz import timezone
from util import getDisassembled

#https://pymodm.readthedocs.io/en/latest/index.html
#https://github.com/mongodb/pymodm/tree/master/example/blog

# Establish a connectin to database.
connect('mongodb://localhost:27017/dart', alias='dart', connect=False)

def extract(newone, key):
    return newone[key] if key in newone else ''

class MetaData(MongoModel):
    stockVer   = fields.CharField()
    stdDiscVer = fields.CharField()

    def __init__(self, stockVer=None, stdDiscVer=None, **kwargs):
        super().__init__(**kwargs)

        self.stockVer   = stockVer
        self.stdDiscVer = stdDiscVer

    class Meta:
        collection_name = 'meta_data'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'stock_ver'   : self.stockVer,
            'std_disc_ver': self.stdDiscVer,
        }

class Version(MongoModel):
    stockVer   = fields.DateTimeField()
    stdDiscVer = fields.DateTimeField()

    def __init__(self, stockVer=None, stdDiscVer=None, **kwargs):
        super().__init__(**kwargs)

        self.stockVer   = stockVer
        self.stdDiscVer = stdDiscVer

    class Meta:
        collection_name = 'version'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'stock_ver'   : self.stockVer.date(),
            'std_disc_ver': self.stdDiscVer.date(),
        }

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

class Fnltt(MongoModel):
    account_nm        = fields.CharField()
    bsns_year         = fields.CharField()
    corp_code         = fields.CharField()
    frmtrm_add_amount = fields.CharField()
    frmtrm_amount     = fields.CharField()
    frmtrm_dt         = fields.CharField()
    frmtrm_nm         = fields.CharField()
    fs_div            = fields.CharField()
    fs_nm             = fields.CharField()
    ord               = fields.CharField()
    rcept_no          = fields.CharField()
    reprt_code        = fields.CharField()
    sj_div            = fields.CharField()
    sj_nm             = fields.CharField()
    stock_code        = fields.CharField()
    thstrm_add_amount = fields.CharField()
    thstrm_amount     = fields.CharField()
    thstrm_dt         = fields.CharField()
    thstrm_nm         = fields.CharField()

    def __init__(self, newone=None, **kwargs):
        super().__init__(**kwargs)

        if newone is None:
            return

        if 'account_nm'        in newone: self.account_nm        = newone['account_nm']
        if 'bsns_year'         in newone: self.bsns_year         = newone['bsns_year']
        if 'corp_code'         in newone: self.corp_code         = newone['corp_code']
        if 'frmtrm_add_amount' in newone: self.frmtrm_add_amount = newone['frmtrm_add_amount']
        if 'frmtrm_amount'     in newone: self.frmtrm_amount     = newone['frmtrm_amount']
        if 'frmtrm_dt'         in newone: self.frmtrm_dt         = newone['frmtrm_dt']
        if 'frmtrm_nm'         in newone: self.frmtrm_nm         = newone['frmtrm_nm']
        if 'fs_div'            in newone: self.fs_div            = newone['fs_div']
        if 'fs_nm'             in newone: self.fs_nm             = newone['fs_nm']
        if 'ord'               in newone: self.ord               = newone['ord']
        if 'rcept_no'          in newone: self.rcept_no          = newone['rcept_no']
        if 'reprt_code'        in newone: self.reprt_code        = newone['reprt_code']
        if 'sj_div'            in newone: self.sj_div            = newone['sj_div']
        if 'sj_nm'             in newone: self.sj_nm             = newone['sj_nm']
        if 'stock_code'        in newone: self.stock_code        = newone['stock_code']
        if 'thstrm_add_amount' in newone: self.thstrm_add_amount = newone['thstrm_add_amount']
        if 'thstrm_amount'     in newone: self.thstrm_amount     = newone['thstrm_amount']
        if 'thstrm_dt'         in newone: self.thstrm_dt         = newone['thstrm_dt']
        if 'thstrm_nm'         in newone: self.thstrm_nm         = newone['thstrm_nm']

    class Meta:
        collection_name = 'fnlti'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('corp_code',ASCENDING)], name='fnltt_corp_code' )
        ]

    @property
    def to_dict(self):
        return {
            'account_nm'        : self.account_nm,
            'bsns_year'         : self.bsns_year,
            'corp_code'         : self.corp_code,
            'frmtrm_add_amount' : self.frmtrm_add_amount,
            'frmtrm_amount'     : self.frmtrm_amount,
            'frmtrm_dt'         : self.frmtrm_dt,
            'frmtrm_nm'         : self.frmtrm_nm,
            'fs_div'            : self.fs_div,
            'fs_nm'             : self.fs_nm,
            'ord'               : self.ord,
            'rcept_no'          : self.rcept_no,
            'reprt_code'        : self.reprt_code,
            'sj_div'            : self.sj_div,
            'sj_nm'             : self.sj_nm,
            'stock_code'        : self.stock_code,
            'thstrm_add_amount' : self.thstrm_add_amount,
            'thstrm_amount'     : self.thstrm_amount,
            'thstrm_dt'         : self.thstrm_dt,
            'thstrm_nm'         : self.thstrm_nm,
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
            IndexModel([('corp_code',ASCENDING)], name='corp_corp_code' )
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
    id          = fields.IntegerField()
    category    = fields.IntegerField()   #1:일반, 2:요약가능, 3:조건 디테일
    seq         = fields.IntegerField()
    keyword     = fields.CharField()
    report_nm   = fields.CharField()
    report_dnm  = fields.CharField()
    crud        = fields.CharField()
    lastUpdated = fields.DateTimeField()

    def __init__(self, id=None, category=None, keyword=None, report_nm=None, **kwargs):
        super().__init__(**kwargs)

        self.id = id
        self.keyword    = keyword
        self.report_nm  = report_nm if report_nm else keyword
        self.report_dnm = getDisassembled(self.report_nm)

        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        self.crud = 'C'
        self.lastUpdated = today
        self.seq = id
        self.category = category

    class Meta:
        collection_name = 'std_disc'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            'std_disc_id': self.id,
            'keyword'    : self.keyword,
            'category'   : str(self.category),
            'seq'        : str(self.seq),
            'report_nm'  : self.report_nm,
            'report_dnm' : self.report_dnm,
            'lastUpdated': self.lastUpdated.date(),
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
    change     = fields.FloatField()
    content    = fields.CharField()
    url        = fields.CharField()
    high_time  = fields.CharField()
    high_tick  = fields.IntegerField()
    low_time   = fields.CharField()
    low_tick   = fields.IntegerField()

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
        self.change     = extract(newone, 'change')
        self.content    = extract(newone, 'content')
        self.url        = extract(newone, 'url')
        self.high_time  = extract(newone, 'high_time')
        self.high_tick  = extract(newone, 'high_tick')
        self.low_time   = extract(newone, 'low_time')
        self.low_tick   = extract(newone, 'low_tick')

    class Meta:
        collection_name = 'disc'
        connection_alias = 'dart'
        indexes = [
            IndexModel([('rcept_dt',DESCENDING),('reg_time',DESCENDING),('rcept_no',DESCENDING)], name='disc_lastest'),
        ]

    @property
    def to_dict(self):
        return {
            'disc_id'   : str(self._id),
            'std_disc'  : self.std_disc.id,
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
            'change'    : self.change,
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

#REMOVEME
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
    val1       = fields.CharField()
    val2       = fields.CharField()
    val3       = fields.CharField()
    val4       = fields.CharField()
    val5       = fields.CharField()
    num1       = fields.IntegerField()
    num2       = fields.IntegerField()
    num3       = fields.IntegerField()
    num4       = fields.IntegerField()
    num5       = fields.IntegerField()
    
    def __init__(self, details = None, **kwargs):
        super().__init__(**kwargs)

        if details is None:
            return
        vals = details['vals']
        nums = details['nums']
        if type(vals) is list:
            for idx, val in enumerate(vals):
                #vars()['val'+str(idx+1)] = val
                #vars(self).update(locals())
                if   not self.val1: self.val1 = val
                elif not self.val2: self.val2 = val
                elif not self.val3: self.val3 = val
                elif not self.val4: self.val4 = val
                elif not self.val5: self.val5 = val
        if type(nums) is list:
            for idx, num in enumerate(nums):
                if   not self.num1: self.num1 = num
                elif not self.num2: self.num2 = num
                elif not self.num3: self.num3 = num
                elif not self.num4: self.num4 = num
                elif not self.num5: self.num5 = num

    @property
    def to_dict(self):
        return {
            'val1' : self.val1,
            'val2' : self.val2,
            'val3' : self.val3,
            'val4' : self.val4,
            'val5' : self.val5,
            'num1' : self.num1,
            'num2' : self.num2,
            'num3' : self.num3,
            'num4' : self.num4,
            'num5' : self.num5,
        }

class Unit(MongoModel):
    #id          = fields.CharField()
    id          = fields.IntegerField()
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
        
        self.id          = extract(newone, 'id')
        self.name        = extract(newone, 'name')
        self.stocks      = extract(newone, 'stocks')
        self.stock_codes = extract(newone, 'stock_codes')
        self.stock_names = extract(newone, 'stock_names')
        self.std_disc    = extract(newone, 'std_disc')
        self.detail      = UnitDetail(extract(newone, 'detail'))

    @property
    def to_dict(self):
        return {
            'id'     : self.id,
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

    def __init__(self, disc = None, ohlcvs = None, **kwargs):
        super().__init__(**kwargs)

        if ohlcvs is None:
            return
        if ohlcvs.__len__() == 0:
            return

        self.corp = disc.corp
        self.disc = disc

        self.closeBf30 = ohlcvs[0].close.values[0] if not ohlcvs[0].empty else 0
        self.closeBf7  = ohlcvs[1].close.values[0] if not ohlcvs[1].empty else 0
        self.close     = ohlcvs[2].close.values[0] if not ohlcvs[2].empty else 0
        self.closeAf7  = ohlcvs[3].close.values[0] if not ohlcvs[3].empty else 0
        self.closeAf30 = ohlcvs[4].close.values[0] if not ohlcvs[4].empty else 0

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

def del_unit(units, del_unit):
    if not units:
        return
    for i, unit in enumerate(units):
        if str(unit.id) == str(del_unit['id']):
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
        
class Chat(MongoModel):
    user      = fields.ReferenceField(User)
    watch     = fields.ReferenceField(Watch)
    createdAt = fields.DateTimeField()

    chat_type = fields.IntegerField()
    disc      = fields.ReferenceField(Disc)
    content   = fields.CharField()
    recv_date = fields.DateTimeField()
    label     = fields.CharField()

    def __init__(self, user=None, watch=None, chat_type=None, disc=None, content=None, **kwargs):
        super().__init__(**kwargs)
        self.user      = user
        self.watch     = watch
        self.chat_type = chat_type
        self.disc      = disc
        self.content   = content
        self.createdAt = datetime.now(timezone('UTC'))  #expiring timezone
        if disc:
            self.label = disc.report_nm + ' [' + disc.corp.corp_name + ']'
        else:
            self.label = None

    class Meta:
        collection_name = 'chat'
        connection_alias = 'dart'

        #expire after 7days 604800
        indexes = [
            IndexModel([('user', ASCENDING), ('createdAt',ASCENDING)], name='chat_created_at', expireAfterSeconds= 604800)
        ]

    @property
    def to_dict(self):
        return dict({'_id'       : str(self._id),
                     'chat_type' : self.chat_type,
                     'watch_id'  : self.watch.id,
                     'label'     : self.label
                    }, **self.disc.to_dict)

class ChatRoom(MongoModel):
    watch = fields.ReferenceField(Watch)
    chats = fields.EmbeddedDocumentListField(Chat, default=[])

    def __init__(self, watch=None, **kwargs):
        super().__init__(**kwargs)

        self.watch = watch

    def add_chat(self, new_chat):
        self.chats.append(new_chat)

    class Meta:
        collection_name = 'chat_room'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return list(self.chats)

class UserChatRoom(MongoModel):
    user  = fields.ReferenceField(User)
    rooms = fields.EmbeddedDocumentListField(ChatRoom, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_or_replace_room(self, newone):
        for i, room in enumerate(self.rooms):
            if room.watch != newone.watch:
                continue
            del self.rooms[i]
            break
        self.rooms.insert(0, newone)

    class Meta:
        collection_name = 'user_chat_room'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            '_id' : str(self._id),
            'rooms': [{'watch_id':room.watch.id, 'watch_name':room.watch.name, 'last_label':room.chats[-1].label} for room in self.rooms]
        }

"""
class Message(EmbeddedMongoModel):
    msg_type = fields.IntegerField()
    content  = fields.CharField()
    disc     = fields.ReferenceField(Disc)
    label    = fields.CharField()

    def __init__(self, msg=None, **kwargs):
        super().__init__(**kwargs)

        if isinstance(msg, Disc):
            self.msg_type = 1
            self.disc     = msg
            self.label    = self.disc.content
        else:
            self.msg_type = 2
            self.content  = msg
            self.label    = self.content
        
    @property
    def to_dict(self):
        return {
            'type'    : self.msg_type,
            'content' : self.content,
            'disc'    : self.disc,
            'label'   : self.label,
        }
class Chat(EmbeddedMongoModel):
    watch        = fields.ReferenceField(Watch)
    messages     = fields.EmbeddedDocumentListField(Message, default=[])
    #last_message = fields.ReferenceField(Message)

    def __init__(self, watch=None, **kwargs):
        super().__init__(**kwargs)

        self.watch = watch

    @property
    def to_dict(self):
        return {
            'watch_id'   : str(self.watch.id),
            'watch_name' : self.watch.name,
            'messages'   : list(self.messages),
        }

class UserChatRoom(MongoModel):
    user  = fields.ReferenceField(User)
    chats = fields.EmbeddedDocumentListField(Chat, default=[])

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

    def add_or_replace_chat(self, newone):
        for i, chat in enumerate(self.chats):
            if chat.watch.id != newone.watch.id:
                continue
            del self.chats[i]
            break
        self.chats.insert(0, newone)

    class Meta:
        collection_name = 'user_chat_room'
        connection_alias = 'dart'

    @property
    def to_dict(self):
        return {
            '_id' : str(self._id),
            'rooms': [{'watch_id':chat.watch.id, 'watch_name':chat.watch.name, 'last_message':chat.messages[-1].label} for chat in self.chats]
        }

"""
