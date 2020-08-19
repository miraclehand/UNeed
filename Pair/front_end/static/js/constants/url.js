//export const INDEX = 'http://ec2-13-125-8-70.ap-northeast-2.compute.amazonaws.com:5000/'

// Collector
export const URL_COLLECTOR = 'http://125.183.209.195:8000'

// Pair
export const URL_PAIR = 'http://125.183.209.195:8100'

export const LIST_STOCK  = URL_COLLECTOR + '/api/crawler/stocks'

export const CANDLE    = URL_COLLECTOR + '/api/crawler/candle'
export const CANDLES   = URL_COLLECTOR + '/api/crawler/candles'

export const COMPANY   = URL_COLLECTOR + '/api/crawler/company'
export const TICK      = URL_COLLECTOR + '/api/crawler/tick'

export const NORM_CHART= URL_PAIR + '/api/chart/norm_chart'
export const LOG_CHART = URL_PAIR + '/api/chart/log_chart'
export const HIST_CHART= URL_PAIR + '/api/chart/hist_chart'
export const VOL_CHART = URL_PAIR + '/api/chart/vol_chart'

export const SIGN_IN   = URL_PAIR + '/api/auth/signin'
export const SIGN_ON   = URL_PAIR + '/api/auth/signon'
export const FREE_PASS = URL_PAIR + '/api/auth/freepass'

export const PICKED_PAIR = URL_PAIR + '/api/pair/picked_pair'
export const NODE_PAIR   = URL_PAIR + '/api/pair/node_pakr'

export const ASSET = URL_PAIR + '/api/balance/asset'

export const PROGRESS = URL_PAIR + '/api/strategy/progress'
export const STRAINER = URL_PAIR + '/api/strategy/strainer'
export const SIMULA   = URL_PAIR + '/api/strategy/simula'
export const TRADING  = URL_PAIR + '/api/strategy/trading'
