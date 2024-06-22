from types import SimpleNamespace
import numpy as np
import scipy

from Funcs import *

class production_economy:
    def __init__(self):
        '''Initialize the model'''
        self.par = SimpleNamespace()
    
    def setup(self):
        '''Defined parameters'''

        par = self.par

       # firms
        par.A = 1.0
        par.gamma = 0.5
        par.w = 1.0

        # households
        par.alpha = 0.3
        par.nu = 1.0
        par.epsilon = 2.0 

        # government
        par.tau = 0.0
        par.T = 0.0

        # Question 3
        par.kappa = 0.1

    def market_clearing(self, p1, p2):
        '''Market clearing
        
        Args:
            p1: price of good 1
            p2: price of good 2
        Returns:
            Market clearing
        '''

        # Labor demanded by the firms
        l1 = labor_demand(self.par, p1)
        l2 = labor_demand(self.par, p2)

        # Optimal production by the firms
        y1 = production(self.par, p1)
        y2 = production(self.par, p2)

        # Profit for the firms
        pi1 = profit(self.par, p1)
        pi2 = profit(self.par, p2)

        # Total demand for labor supply
        ell = l1+l2

        # Household consumption
        c1 = demand(self.par, ell, p1, p2)[0]
        c2 = demand(self.par, ell, p1, p2)[1]

        if c1 != y1 or c2 != y2:
            print('Market for good 1 is not cleared')
        else:

            # Market clearing conditions:
            labor_market_clearing = ell
            good1_market_clearing = c1
            good2_market_clearing = c2

        return labor_market_clearing, good1_market_clearing, good2_market_clearing