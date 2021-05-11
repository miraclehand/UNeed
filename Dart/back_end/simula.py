import sys
sys.path.append('../../')
from strat.abstrat import AbstractStratFactory

if __name__ == '__main__':
    factory = AbstractStratFactory.get_factory('Strat2')
    strat = factory.create_strat()
    strat.do_simula('20210101', '20210531')

