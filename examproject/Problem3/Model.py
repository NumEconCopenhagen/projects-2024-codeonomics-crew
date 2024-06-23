from types import SimpleNamespace
import numpy as np
import scipy

from Funcs import *


class barycentric:
    def __init__(self):
        '''Initialize the model'''
        self.par = SimpleNamespace()

        self.setup()
    
    def setup(self):
        '''Defined parameters'''

        par = self.par
        
 