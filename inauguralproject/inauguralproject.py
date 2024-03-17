
from types import SimpleNamespace
import numpy as np

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

        par.w1B = 1 - par.w1A   #Consumer B endownment normalisation 
        par.w2B = 1 - par.w2A   #Consumer B endownment normalisation

        par.p2 = 1

    def utility_A(self,x1A,x2A):
        """Defines the utility for consumer A
        
        Args:
            x1A: Number of good 1
            x2A: Number of good 2

        Returns:
            u_A: Utility of consumer A        

        """

        par = self.par 
        
        u_A = x1A**(par.alpha) * x2A**(1-par.alpha)
        return u_A


    def utility_B(self,x1B,x2B):
        """Defines the utility for consumer B
        
        Args:
            x1B: Number of good 1
            x2B: Number of good 2

        Returns:
            u_B: Utility of consumer B        

        """

        par = self.par 

        u_B = x1B**par.beta * x2B**(1-par.beta)
        return u_B

    def demand_A(self,p1):
        """Defines demand for consumer A

        Args:
            p1: Price of good 1
        
        Returns:
            x1A: Consumer A's demand for good 1
            x2A: Consumer A's demand for good 2
        
        """
        par = self.par

        x1A = par.alpha*(p1*par.w1A+par.p2*par.w2A)/p1      #Demand for good 1
        x2A = (1-par.alpha)*(p1*par.w1A+par.p2*par.w2A)/1   #Demand for good 2

    
        return x1A, x2A

    def demand_B(self,p1):
        """Defines demand for consumer B

        Args:
            p1: Price of good 1
        
        Returns:
            x1B: Consumer B's demand for good 1
            x2B: Consumer B's demand for good 2
        
        """

        par = self.par

        x1B = par.beta*(p1*par.w1B+par.p2*par.w2B)/p1           #Demand for good 1
        x2B = (1-par.beta)*(p1*par.w1B+par.p2*par.w2B)/par.p2   #Demand for good 2

        # xB = []

        # xB.append(np.array([x1B,x2B]))

        return x1B, x2B

    def check_market_clearing(self,p1):
        """Checks if the market clears

        Args:
            p1: Price of good 1
        
        """


        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2