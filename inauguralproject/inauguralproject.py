
from types import SimpleNamespace
import numpy as np

class ExchangeEconomyClass:

    def __init__(self):
        """Initialize the model with parameters"""

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

        par.w1B = 1 - par.w1A   #Consumer B endownment normalisation 
        par.w2B = 1 - par.w2A   #Consumer B endownment normalisation

        # Price normalisation
        par.p2 = 1

        # Equilibrium parameters
        par.kappa = 0.1
        par.eps = 1e-8
        par.maxiter = 10000

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
    
    def excess_demand_good_1_func(self,p1):
        """Calculates the excess demand for good 1

        Args:
            p1: Price of good 1

        Returns:
            excess_demand: Excess demand of good 1
        """
        par = self.par

        # 1. demand
        x1A, _ = self.demand_A(p1)
        x1B, _ = self.demand_B(p1)
        demand = x1A + x1B

        # 2. supply
        supply = par.w1A + par.w1B

        # 3. excess demand
        excess_demand = demand - supply

        return excess_demand
    
    def excess_demand_good_2_func(self, p1):
        """Calculates the excess demand for good 2

        Args:
            p1: Price of good 1

        Returns:
            excess_demand: Excess demand of good 2 
        """
        par = self.par

        # 1. demand
        _ , x2A = self.demand_A(p1)
        _ , x2B = self.demand_B(p1)
        demand = x2A + x2B

        # 2. supply 
        supply = par.w2A + par.w2B

        # 3. excess demand
        excess_demand = demand-supply
        
        return excess_demand



    def find_equilibrium(self, p2, p1_guess):
        """Calculates the market equilibrium

        Args:
            p1_guess: Arbitrary starting value of price for good 1

        Returns:
             Iteration over excess demand based on the price of good 1
        """
        par = self.par

        # Counter:
        t = 0
        # Guess on price
        p1 = p1_guess

        
        # using a while loop as we don't know number of iterations a priori
        while True:

            # 1. excess demand for good 1
            Z1 = self.excess_demand_good_1_func(p1)
            
            # 2. check stop?
            if  np.abs(Z1) < par.eps or t >= par.maxiter:   # The first condition compares to the tolerance level and the second condition ensures that the loop does not go to infinity
                print(f'{t:3d}: p1 = {p1:12.8f} -> excess demand -> {Z1:14.8f}')
                break    
            
            # 3. Print the first 5 and every 25th iteration using the modulus operator 
            if t < 5 or t%25 == 0:
                print(f'{t:3d}: p1 = {p1:12.8f} -> excess demand -> {Z1:14.8f}')
            elif t == 5:
                print('   ...')
            
            # 4. update p1
            p1 = p1 + par.kappa*Z1/2    # The price is updated by a small number (kappe) scaled to excess demand divded among the number of consumers, i.e. 2
            
            # 5. update counter and return to step 1
            t += 1    


        # Check if solution is found 
        if np.abs(Z1) < par.eps:
            # Store equilibrium prices
            self.p1_star = p1 

            # Store equilibrium excess demand 
            self.Z1 = Z1
            self.Z2 = self.excess_demand_good_2_func(self.p1_star)

            # Make sure that Walras' law is satisfied
            if not np.abs(self.Z2) < par.eps:
                print('The market for good 2 was not cleared')
                print(f'Z2 = {self.Z2}')

        else:
            print('Solution was not found')


    def print_solution(self):
        """Prints the solution to exchange economy
        
        Args:
            No arguments
        
        Returns:
            Returns solutions to the exchange economy
        """

        text = 'Solution to market equilibrium:\n'
        text += f'p1 = {self.p1_star}\n\n'

        text += 'Excess demands are:\n'
        text += f'Z1 = {self.Z1}\n'
        text += f'Z2 = {self.Z2}'
        print(text)
