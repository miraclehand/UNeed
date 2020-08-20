import config from '../../../../../uneed.config.json'

const HOSTNAME = config['HOSTNAME']
const AWS_IP = config['AWS_IP']
const HIKEY_INTER_IP = config['HIKEY_INTER_IP']
const HIKEY_OUTER_IP = config['HIKEY_OUTER_IP']
const COLLECTOR_PORT = config['COLLECTOR_PORT']
const PAIR_PORT = config['PAIR_PORT']

export const URL_OUTER = 'http://' + HIKEY_OUTER_IP
// Collector
export const URL_COLLECTOR = URL_OUTER + ':' + COLLECTOR_PORT

// Pair
export const URL_PAIR = URL_OUTER + ':' + PAIR_PORT

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
