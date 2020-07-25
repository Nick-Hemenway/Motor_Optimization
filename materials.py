import numpy as np
import femm as fe
import pathlib as pl
from scipy.constants import mu_0

class Material():
    
    def __init__(self, name):
        
        self.name = name
        self.add_count = 0
        
    def add(self):
        
        #ensure materials don't get added to the analysis more than once
        if self.add_count < 1:
            fe.mi_getmaterial(self.name)
            self.add_count += 1
        else:
            pass
        
class Recoma35E(Material):
    
    def __init__(self, name):
        
        super().__init__(name)
        self.Br = 1.19 #remanent field of magnet in T
        self.Hc = 880_000 #coercivity of magnet in A/m
        
        self.mu_r = self.Br/(self.Hc*mu_0) #relative permeability
        
        self.conductivity = 0 #MS/m
        self.lam_fill = 1 #magnets are not laminated
        self.num_strands = 1 #FEMM manual says this should be 1 for magnets (ref. pg. 10)
        self.add_count = 0
        
    def add(self):
        
        #ensure materials don't get added to the analysis more than once
        if self.add_count < 1:
            fe.mi_addmaterial(self.name, self.mu_r, self.mu_r, self.Hc, 0,
                              self.conductivity, 0, 0, self.lam_fill, 0, 0, 0, self.num_strands)
            self.add_count += 1
        else:
            pass

class M19_29Ga(Material):
    
    def __init__(self, name, fname = 'recoma35e.txt'):
        
        super().__init__(name)
        self.file = pl.Path(fname)
        
        self.lam_thickness = 0.36 #lam thickness in mm
        self.fill_factor = 0.91 #lam fill factor/stacking factor --> 1 == solid
        self.add_count = 0
        
    def add(self):
        
        #ensure materials don't get added to the analysis more than once
        if self.add_count < 1:
            H, B = np.loadtxt(self.file, unpack = True)
            
            fe.mi_addmaterial(self.name, 0, 0, 0, 0, 0, self.lam_thickness, 0,
                           self.fill_factor, 0, 0, 0, 0, 0)
            
            for b,h in zip(B,H):
                fe.mi_addbhpoint(self.name, b, h)
                
            self.add_count += 1
        else:
            pass
        
        