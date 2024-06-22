from types import SimpleNamespace
import numpy as np
import scipy




def labor_demand(par, p):
    '''Labor demand
    
    Args:
        p: price of goods
    Returns:
        Labor demand
    '''
    return ((p*par.A*par.gamma)/par.w)**(1/(1-par.gamma))


def production(par, p):
    '''Production
    
    Args:
        p: price of goods
    Returns:
        Production
    '''
    return par.A*labor_demand(par, p)**par.gamma

def profit(par, p):
    '''Profit
    
    Args:
        p: price of goods
    Returns:
        Profit
    '''
    return (1-par.gamma)/par.gamma*par.w*((p*par.A*par.gamma)/par.w)**(1/(1-par.gamma))




def demand(par, l, p1, p2):
    '''Demand
    
    Args:
        l: Labor
    Returns:
        Demand
    '''
    c1 = par.alpha*(par.w*l+par.T+profit(par, p1)+profit(par, p2))/p1
    c2 = (1-par.alpha)*(par.w*l+par.T+profit(par, p1)+profit(par, p2))/(p2+par.tau)

    return c1, c2

def labor_supply(par, p1, p2):
    '''Labor supply
    
    Args:
        p1: price of good 1
        p2: price of good 2
    Returns:
        Labor supply
    '''
    def objective_function(par, l, p1, p2):
        obj = np.log(demand(par, l, p1, p2)[0])**par.alpha*(demand(par, l, p1, p2)[1])**(1-par.alpha)-par.nu*(l**(1+par.epsilon))/(1+par.epsilon)
        return -obj
    
    # Perform optimization
    initial_guess = 0.5
    l = scipy.optimize.minimize_scalar(objective_function, args=(par, p1, p2), bounds=[0, 1], method='bounded').x

    return l








