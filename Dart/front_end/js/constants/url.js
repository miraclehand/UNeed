export const INDEX = 'http://125.183.209.195:8200'

export const VERSION  = INDEX + '/api/version'
export const CORP     = INDEX + '/api/corp'
export const CORPS    = INDEX + '/api/corps'
export const DISC     = INDEX + '/api/disc'
export const DISCS    = INDEX + '/api/discs'
export const KEYWORD  = INDEX + '/api/keyword'
export const KEYWORDS = INDEX + '/api/keywords'

export const WATCHS   = INDEX + '/api/watchs'
export const CHAT     = INDEX + '/api/chat'
export const CHAT_ROOM= INDEX + '/api/chat_room'
export const CHAT_CHECK = INDEX + '/api/chatcheck'
export const CHAT_CATCHUP = INDEX + '/api/chat_catchup'

export const SIMULA   = INDEX + '/api/simula'
export const SIMULAS  = INDEX + '/api/simulas'
export const USER_DISCS  = INDEX + '/api/user_discs'

export const STD_DISCS   = INDEX + '/api/std_discs'

export const SIGN_IN   = INDEX + '/api/auth/signin'
export const SIGN_ON   = INDEX + '/api/auth/signon'
export const FREE_PASS = INDEX + '/api/auth/freepass'
export const USER  = INDEX + '/api/user'


export const DC_INDEX = 'http://125.183.209.195:8000'
export const OHLCV  = DC_INDEX + '/api/crawler/ohlcv'
export const STOCKS = DC_INDEX + '/api/crawler/stocks'


/*
export const CANDLE = 'https://fchart.stock.naver.com/sise.nhn?symbol=%d&timeframe=day&count=%d&requestType=0'
*/
export const CANDLE = 'https://fchart.stock.naver.com/sise.nhn?symbol=005930&timeframe=day&count=10&requestType=0'


