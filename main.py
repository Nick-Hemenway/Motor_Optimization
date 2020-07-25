import numpy as np
import pathlib as pl
import femm as fe
import motor
import materials as mat

class MotorSimulation():
    
    def __init__(self, fname = None, overwrite = False):
        
        if fname is not None:
            p = pl.Path(fname)
            
            if p.exists() and (not overwrite):
                self.open_previous(str(p))
            else:
                self.new(str(p))
            
    def open_previous(self, fname):
        
        fe.openfemm()
        fe.opendocument(fname)
        self.fname = fname
        
    def new(self, fname):
        
        fe.openfemm()
        fe.newdocument(0)
        fe.mi_saveas(fname)
        self.fname = fname
        
        #add air to problem by default
        air = mat.Material('Air')
        air.add()
        
    @staticmethod
    def zoom(method = 'natural'):
        
        if method.lower() == 'natural':
            fe.mi_zoomnatural()
    
    def save(self):
        
        fe.mi_saveas(self.fname)
        
    def saveas(self, fname):
        
        fe.mi_saveas(fname)
        self.fname = fname
        
#%% Create Simulation
        
sim = MotorSimulation('test.fem', overwrite = True)
        
#%% MATERIALS

R35e = mat.Recoma35E('R35e')
M19 = mat.M19_29Ga('M19')

#%% ROTOR

rotor = motor.PM_Rotor(dri=50, dm=10, dmp=3, alpha_m=60, p=2, OR=100)
rotor.draw()
rotor.set_materials(magnet=R35e, iron=M19)

#%% SCALE SCREEN AND SAVE

sim.zoom()
sim.save()


