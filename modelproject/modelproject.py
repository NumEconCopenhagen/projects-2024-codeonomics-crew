from scipy import optimize
from types import SimpleNamespace
import numpy as np



class Solow:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # Parameters for production function
        par.alpha = 0.2    # Capital share
        par.beta = 0.4     # Labor share
        par.kappa = 0.2    # Land share
        par.epsilon = 1 - par.alpha - par.beta - par.kappa  # Oil share

        # Parameters for technology growth
        par.g = 0.02        # Growth rate of technology
        par.tech_init = 1

        # Land
        par.land_init = 1

        # Oil
        par.oil.init = 1   # Initial oil stock
        par.s_E = 0.1      # Extraction rate of oil

        # Parameters for labor growth
        par.labor_init = 1
        par.n = 0.01        # Growth rate of labor

        # Parameters for capital accumulation
        par.s_Y = 0.2         # Savings rate
        par.delta = 0.05    # Depreciation rate


    def tech_growth(self):
        """Technical Growth"""

        par = self.par
        A0 = par.tech.init
        A = (1+par.g)*A0

        return A
    
    def labor_growth(self):
        """Labor Growth"""

        par = self.par
        L0 = par.labor_init
        L_next = (1+par.n)*L0

        return L_next
    
    def oil_stock(self):
        """Growth of stock of oil"""

        par = self.par
        R0 = par.oil.init

        R_next = (1-par.s_E)*R0

        return R_next
    
    def production(self, K, L):
        """Production Function"""

        par = self.par
        X = par.land_init
        E = par.oil.init

        Y = K**par.alpha * (par.A * L)**par.beta*X**par.kappa*E**par.epsilon

        return Y
    
    def capital_accumulation(self):
        """Capital Accumulation"""
        par = self.par

        K_next = par.s*self.Y + (1-par.delta)*self.K

        return K_next






# Not used in this project
# def solve_ss(sesult