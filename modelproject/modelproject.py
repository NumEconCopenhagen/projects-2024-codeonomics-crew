from scipy import optimize
from types import SimpleNamespace
import numpy as np
import sympy as sm
from IPython.display import display 
import matplotlib.pyplot as plt


def analytical(ext1 = False, ext2 = False, do_print = False):
    """
    Use sympy to solve the model.

    Args:
        ext1 (bool): If True, the model is solved with land.
        ext2 (bool): If True, the model is solved with land AND oil
        do_print (bool): If True, the solution is printed.
    
    Returns:
        z_sol: The solution to the model.
    """
    # Define symbols
    z = sm.symbols('z')
    s_Y = sm.symbols('s_Y')
    s_E = sm.symbols('s_E')
    delta = sm.symbols('delta')
    alpha = sm.symbols('alpha')
    g = sm.symbols('g')
    n = sm.symbols('n')

    # Define extensions
    kappa = 0
    epsilon = 0


    if ext1:
        kappa = sm.symbols('kappa')
        epsilon = 0
    elif ext2:
        kappa = sm.symbols('kappa')
        epsilon = sm.symbols('epsilon')

    # Define equation
    denominator = (((1+g) * (1+n))**(1 - alpha - kappa - epsilon) * (1-s_E)**epsilon)**(1/(1-alpha))
    transition = sm.Eq(z, (1/denominator) *(s_Y + (1-delta)*z))

    # Solve equation
    z_sol = sm.solve(transition, z)[0]

    # Print solution
    if do_print == True:
        if ext1 == True:
            print(f'The solution to the model with extension 1 is: z = {z_sol}')
        elif ext2 == True:
            print(f'The solution to the model with extension 2 is: z = {z_sol}')
        else:
            print(f'The solution to the model without any extensions is: z = {z_sol}')
        display(sm.Eq(z, z_sol))
        
    return z_sol



class Solow:

    def __init__(self):
        """
        Initialize the model with parameters and initial values
        
        Args:
            None
        
        Returns:
            None
        """

        par = self.par = SimpleNamespace()

    def setup(self):
        """
        Define parameters

        Args:
            None
        
        Returns:
            None
        """

        par = self.par

        # Parameters for production function
        par.alpha = 0.2    # Capital share
        par.kappa = 0.15    # Land share
        par.epsilon = 0.15 # Oil share

        par.g = 0.02        # Growth rate of technology
        par.s_E = 0.1       # Extraction rate of oil
        par.n = 0.01        # Growth rate of labor
        par.s_Y = 0.2       # Savings rate
        par.delta = 0.05    # Depreciation rate of capital

        # Initial values
        par.K0 = 1          # Initial capital
        par.L0 = 1          # Initial labor
        par.A0 = 1          # Initial technology
        par.R0 = 100        # Initial oil stock

        # Land
        par.X = 100         # Fixed land


    def evaluate_ss(self, ss, ext1 = False, ext2 = False, do_print = False):
        """
        Evaluate the analycally derivated steady state

        Args:
            ss: Analytical steady state
            do_print: If True, the steady state is printed
        
        Returns:
            sol: Solution to the steady state
            if do_print is True, the solution is printed
        """

        par = self.par  # Parameters



        # Define extensions
        if ext1 == True:
            kappa = sm.symbols('kappa')
            epsilon = 0
        elif ext2 == True:
            kappa = sm.symbols('kappa')
            epsilon = sm.symbols('epsilon')
        
        # Sympy
        alpha = sm.symbols('alpha')
        kappa = sm.symbols('kappa')
        epsilon = sm.symbols('epsilon')
        g = sm.symbols('g')
        n = sm.symbols('n')
        s_Y = sm.symbols('s_Y')
        s_E = sm.symbols('s_E')
        delta = sm.symbols('delta')

        # Lamdify equation
        eq = sm.lambdify((alpha, kappa, epsilon, s_Y, s_E, delta, g, n), ss)

        # Evaluate
        sol = eq(par.alpha, par.kappa, par.epsilon, par.s_Y, par.s_E, par.delta, par.g, par.n)

        # Print
        if do_print:
            print(f'The analytical steady state is: z = {sol}')

        return sol




    def solve_ss(self, method='brentq', ext1 = False, ext2= False, do_print = False):
        """
        Solve the model numerically

        Args:
            method: Method for solving the model - either bisect or brentq
            ext1: If True, the model is solved with land
            ext2: If True, the model is solved with land AND oil
            do_print: If True, the solution is printed
        
        Returns:
            sol: Solution to the model
            if do_print is True, the solution is printed
        """
        par = self.par  # Parameters

        # Define extensions
        if ext1 == True:
            kappa = par.kappa
            epsilon = 0
        elif ext2 == True:
            kappa = par.kappa
            epsilon = par.epsilon
        else:
            kappa = 0
            epsilon = 0

        # Objective function
        denominator = (((1+par.g) * (1+par.n))**(1 - par.alpha - kappa - epsilon) * (1-par.s_E)**epsilon)
        obj = lambda z: (1/denominator)*(par.s_Y + (1-par.delta)*z)**(1-par.alpha)*z**par.alpha - z

        # Solve the model numerically
        if method == 'bisect':
            result = optimize.root_scalar(obj, bracket=[0.1, 100], method='bisect')
        elif method == 'brentq':
            result = optimize.root_scalar(obj, bracket=[0.1, 100], method='brentq')
        else:
            raise ValueError('method must be either bisect or brentq')

        # Print results
        if do_print:
            print(f'The numerical steady state using {method}')
            print(result)

        return result












