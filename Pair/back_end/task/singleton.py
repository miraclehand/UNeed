from utils.singleton import SingletonInstance

class OHLCV(SingletonInstance):
    _ohlcv = dict()

    def clear(self):
        self._ohlcv = dict()

    def get(self, code):
        if code in self._ohlcv:
            return self._ohlcv[code]
        return None

    def set(self, code, df):
        self._ohlcv[code] = df

class Variant(SingletonInstance):
    _variant = dict()

    def clear(self):
        self._variant = dict()

    def get(self, code):
        if code in self._variant:
            return self._variant[code]
        return None

    def set(self, code, value):
        self._variant[code] = value

pool_ohlcv = OHLCV.instance()
pool_variant = Variant.instance()
pool_variant.set('simula_valid', True)
