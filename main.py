import numpy as np
import matplotlib.pyplot as plt
import femm as fe
import pm_motor
import materials as mat

fe.openfemm()
# fe.opendocument('stator_template.fem')
fe.newdocument(0)
fe.mi_saveas('test.fem')

#%% MATERIALS

air = mat.Material('Air')
R35e = mat.Recoma35E('R35e')
M19 = mat.M19_29Ga('M19')

materials = [air, R35e, M19]
for material in materials:
    material.add()


#%% ROTOR

rotor = pm_motor.PM_Rotor(dri = 50, dm = 10, dmp = 3, alpha_m = 60, p = 2, OR = 100)
rotor.draw()
rotor.set_materials(magnet = R35e, iron = M19)


#%% SCALE SCREEN

fe.mi_zoomnatural()