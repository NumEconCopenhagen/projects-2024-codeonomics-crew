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

def utility(par):
    '''Utility
    
    Args:
        p1: price of good 1
        p2: price of good 2
        tau: tax
        T: transfer
    Returns:
        Utility
    '''

    c1, c2 = demand(par, labor_demand(par, p1, p2), p1, p2)
    p1 = par.p1
    p2 = par.p2

    return np.log(c1**par.alpha*c2**(1-par.alpha))-par.nu*(labor_demand(par, p1, p2)**(1+par.epsilon))/(1+par.epsilon)

def demand(par, l, p1, p2, tau):
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

def SWF(par):
    '''Social welfare function
    
    Args:
        p1: price of good 1
        p2: price of good 2
    Returns:
        Social welfare function
    '''
    p1 = par.p1
    p2 = par.p2

    return -(utility(par, p1, p2) - par.kappa*production(par, p2))

from Model import production_economy
model = production_economy()
model.setup()
par = model.par

def Walras_law(prices):
    '''Use Walras law to get market clearing
    
    Args:
        p1: price of good 1
    Returns:
        Market clearing
    '''

    p1, p2 = prices

    # Labor demanded by the firms
    l1 = labor_demand(par, p1)
    l2 = labor_demand(par, p2)

    # Optimal production by the firms
    y1 = production(par, p1)
    y2 = production(par, p2)

    # Total demand for labor supply
    ell = l1+l2

    # Household consumption
    c1, c2 = demand(par, ell, p1, p2)

    # Market clearings
    labor_market_clear = ell - l1 - l2
    good1_market_clear = y1 - c1
    good2_market_clear = y2 - c2

    return labor_market_clear, good1_market_clear








