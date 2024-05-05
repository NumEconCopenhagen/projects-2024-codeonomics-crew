from scipy import optimize
from types import SimpleNamespace
import numpy as np
import sympy as sm
from IPython.display import display 
import matplotlib.pyplot as plt


def analytical(ext = 0, do_print = False):
    """
    Use sympy to solve the model.

    Args:
        ext: The extension of the model. 0 is the basic model, 1 is the model with land, and 2 is the model with land and oil.
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
    if ext == 1:
        kappa = sm.symbols('kappa')
        epsilon = 0
    elif ext == 2:
        kappa = sm.symbols('kappa')
        epsilon = sm.symbols('epsilon')

    # Define equation
    denominator = (((1+g) * (1+n))**(1 - alpha - kappa - epsilon) * (1-s_E)**epsilon)**(1/(1-alpha))
    transition = sm.Eq(z, (1/denominator) *(s_Y + (1-delta)*z))

    # Solve equation
    z_sol = sm.solve(transition, z)[0]

    # Print solution
    if do_print == True:
        if ext == 1:
            print(f'The solution to the model with extension 1 is: z = {z_sol}')
        elif ext == 2:
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

        self.par = SimpleNamespace()    # Parameters
        self.sim = SimpleNamespace()    # Simulation results

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
        par.alpha = 1/3    # Capital share
        par.kappa = 0.15    # Land share
        par.epsilon = 0.15 # Oil share

        par.g = 0.02        # Growth rate of technology
        par.s_E = 0.01       # Extraction rate of oil
        par.n = 0.01        # Growth rate of labor
        par.s_Y = 0.1       # Savings rate
        par.delta = 0.05    # Depreciation rate of capital

        # Initial values
        par.K0 = 1          # Initial capital
        par.L0 = 1          # Initial labor
        par.A0 = 1          # Initial technology
        par.R0 = 100        # Initial oil stock

        # Land
        par.X = 100         # Fixed land


    def evaluate_ss(self, ss, ext = 0, do_print = False):
        """
        Evaluate the analycally derivated steady state

        Args:
            ss: Analytical steady state
            ext: The extension of the model. 0 is the basic model, 1 is the model with land, and 2 is the model with land and oil.
            do_print: If True, the steady state is printed
        
        Returns:
            sol: Solution to the steady state
            if do_print is True, the solution is printed
        """

        par = self.par  # Parameters



        # Define extensions
        if ext == 1:
            kappa = sm.symbols('kappa')
            epsilon = 0
        elif ext == 2:
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




    def solve_ss(self, method='brentq', ext = 0, do_print = False):
        """
        Solve the model numerically

        Args:
            method: Method for solving the model - either bisect or brentq
            ext: The extension of the model. 0 is the basic model, 1 is the model with land, and 2 is the model with land and oil.
            do_print: If True, the solution is printed
        
        Returns:
            sol: Solution to the model
            if do_print is True, the solution is printed
        """
        par = self.par  # Parameters

        # Define extensions
        if ext == 1:
            kappa = par.kappa
            epsilon = 0
        elif ext == 2:
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


    def graph(self, periods = 100, ext = 0, do_print = False, shock_period = 0, shock_size = 0):
        """
        Graph the model

        Args:
            periods: Number of periods to simulate
            ext: The extension of the model. 0 is the basic model, 1 is the model with land, and 2 is the model with land and oil.
            do_print: If True, the solution is printed
            shock_period: Period of shock (set to 0 as default)
            shock_size: Amount of capital destroyed (set to 0 as default)
        
        Returns:
            if do_print is True, the solution is printed
        """
        par = self.par  # Parameters
        sim = self.sim  # Simulation results
        T = periods

        # Define extensions
        if ext == 1:
            kappa = par.kappa
            epsilon = 0
        elif ext == 2:
            kappa = par.kappa
            epsilon = par.epsilon
        else:
            kappa = 0
            epsilon = 0
        
        # Check shock is within maximum amount of periods and not negative
        if shock_period < 0:
            raise ValueError('Shock period must be positive')
        if shock_period > T:
            shock_period = 0
            shock_size = 0

        # Find steady state
        ss = self.solve_ss(method='brentq', ext=ext).root

        
        if ss < 0:
            message = 'The steady state is negative'
        else:
            message = ''

        # Create empty arrays to store results
        sim.K = np.empty(T+1)   # Capital
        sim.L = np.empty(T+1)   # Labor
        sim.A = np.empty(T+1)   # Technology
        sim.R = np.empty(T+1)   # Oil
        sim.Y = np.empty(T+1)   # Output
        sim.E = np.empty(T+1)   # Consumption of oil
        sim.z = np.empty(T+1)   # Capital-output ratio
        sim.t = np.linspace(0, T+1, T+1)    # Time

        # Initial values
        sim.K[0] = par.K0 
        sim.L[0] = par.L0   
        sim.A[0] = par.A0
        sim.R[0] = par.R0
        sim.Y[0] = sim.K[0]**par.alpha * (sim.A[0]*sim.L[0])**(1-par.alpha) * par.X**kappa * sim.E[0]**epsilon
        sim.E[0] = par.s_E * sim.R[0]
        sim.z[0] = sim.K[0]/sim.Y[0]

        # Simulate up till shock
        for t in range(shock_period):
            sim.K[t+1] = par.s_Y * sim.Y[t] + (1-par.delta)*sim.K[t]
            sim.R[t+1] = (1-par.s_E)*sim.R[t]
            sim.L[t+1] = (1+par.n)*sim.L[t]
            sim.A[t+1] = (1+par.g)*sim.A[t]
            sim.E[t+1] = par.s_E * sim.R[t+1]
            sim.Y[t+1] = sim.K[t+1]**par.alpha * (sim.A[t+1]*sim.L[t+1])**(1-par.alpha-kappa-epsilon) * par.X**kappa * sim.E[t+1]**epsilon 
            sim.z[t+1] = sim.K[t+1]/sim.Y[t+1]
        
        # Store shock
        sim.K[shock_period] = sim.K[shock_period]*(1-shock_size)    # Shock is relative amout of capital destroyed, and thus we subtract it from 1
        

        # Simulate remaining periods
        for t in range(shock_period, T):
            sim.K[t+1] = par.s_Y * sim.Y[t] + (1-par.delta)*sim.K[t]
            sim.L[t+1] = (1+par.n)*sim.L[t]
            sim.A[t+1] = (1+par.g)*sim.A[t]
            sim.R[t+1] = (1-par.s_E)*sim.R[t]
            sim.E[t+1] = par.s_E * sim.R[t+1]
            sim.Y[t+1] = sim.K[t+1]**par.alpha * (sim.A[t+1]*sim.L[t+1])**(1-par.alpha-kappa-epsilon) * par.X**kappa * sim.E[t+1]**epsilon 
            sim.z[t+1] = sim.K[t+1]/sim.Y[t+1]

        # Plot
        if do_print == True:    # Start plotting
            if ext == 1:    # For model with land
                fig, ax = plt.subplots(2, 3)    # Create figure with 2 rows and 3 columns
                fig.suptitle(f'Simulated model with land{message}', size = 20)   # Title of figure
                ax[0,2].plot(sim.t,par.X*np.ones(T+1))   # Plot fixed resources on row 0, column 2
                ax[0,2].set_title('Land, $X$')  # Title of subplot
            elif ext == 2:   # For model with land and oil
                fig, ax = plt.subplots(2, 3)   # Create figure with 2 rows and 3 columns
                fig.suptitle(f'Simulated model with land and oil{message}', size = 20)  # Title of figure
                ax[0,2].plot(sim.t,sim.R)  # Plot exhaustible resource on row 0, column 2
                ax[0,2].set_title('Stock of oil, $R_t$') # Title of subplot
                ax[1,2].plot(sim.t,sim.E) # Plot consumption of exhaustible resource on row 1, column 2
                ax[1,2].set_title('Consumption of limited resource, $E_t$') # Title of subplot
            else:  # For model without land or oil
                fig, ax = plt.subplots(2, 2) # Create figure with 2 rows and 2 columns
                fig.suptitle(f'Simulated model without land or oil{message}', size = 20)  # Title of figure
                fig.suptitle(f'Simulated model{message}', size = 20) # Title of figure
            ax[0,0].plot(sim.t,sim.K) # Plot capital on row 0, column 0
            ax[0,0].set_title('Capital stock, $K_t$') # Title of subplot
            ax[1,0].plot(sim.t,sim.Y) # Plot output on row 1, column 0
            ax[1,0].set_title('Output, $Y_t$') # Title of subplot
            ax[0,1].plot(sim.t,sim.z, label=r'$z_t$') # Plot capital-output ratio on row 0, column 1
            ax[0,1].axhline(y=ss, color='black', linestyle='--', label=f'Steady state: {ss:.2f}') # Add horizontal line for steady state
            ax[0,1].legend() # Add legend to subplot 
            ax[0,1].set_title('Capital-output ratio, $z_t$')    # Title of subplot
            ax[1,1].plot(sim.t,sim.A, label=r'$A_t$') # Plot technology on row 1, column 1
            ax[1,1].plot(sim.t,sim.L, label=r'$L_t$') # Plot labor on row 1, column 1
            ax[1,1].legend() # Add legend to subplot
            ax[1,1].set_title('Technology and Labour, $A_t$ and $L_t$') # Title of subplot
            plt.subplots_adjust(wspace=0.2, hspace=0.4) # Adjust space between subplots
            plt.show() # Show plot



