import sys
sys.path.append('../../')
from strat.abstrat import AbstractStratFactory

if __name__ == '__main__':
    factory = AbstractStratFactory.get_factory('Strat2')
    strat = factory.create_strat()
    #strat.do_simula('20160101', '20211231')
    strat.do_simula('20100101', '20501231')

