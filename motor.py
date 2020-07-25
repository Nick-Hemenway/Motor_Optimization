import numpy as np
import femm as fe
from collections import namedtuple

def rotate(x, y, theta):
    
    theta = np.deg2rad(theta)
    
    xnew = x*np.cos(theta) - y*np.sin(theta)
    ynew = x*np.sin(theta) + y*np.cos(theta)
    
    return xnew, ynew

class Stator():
    
    def __init__(self):
        
        pass

class PM_Rotor():
    
    threshold =  0.1 #mm (threshold to determine if the rotor is hollow or not)
    
    def __init__(self, dri, dm, dmp, alpha_m, OR, p):
        
        self.dri = dri
        self.dm = dm
        self.dmp = dmp
        self.alpha_m = np.deg2rad(alpha_m)
        self.alpha_m_deg = alpha_m
        self.OR = OR
        self.p = p #number of pole pairs
        
        self.is_drawn = False
        
    def draw(self):
        
        R1 = self.OR - (self.dm + self.dri) #inner radius of rotor
        R2 = self.OR - self.dm #radius to inside of PM
        R3 = self.OR - self.dmp #radius to outside of steel rotor
        
        self.hollow = R1 > self.threshold
        
        num_magnets = 2*self.p
        theta = 360/num_magnets #span between magnet centers in deg
        
        c = np.cos(self.alpha_m/2)
        s = np.sin(self.alpha_m/2)
        
        #bottom 3 points
        p1 = [R2*c, -R2*s]
        p2 = [R3*c, -R3*s]
        p3 = [self.OR*c, -self.OR*s]
        #top 3 points
        p4 = [self.OR*c, self.OR*s]
        p5 = [R3*c, R3*s]
        p6 = [R2*c, R2*s]
        
        nominal_coords = [p1, p2, p3, p4, p5, p6]
        
        #draw each of the magnets
        for i in range(num_magnets):
            
            angle = i*theta
            rotated_coords = [rotate(*coord, angle) for coord in nominal_coords]
            
            for coord in rotated_coords:
                fe.mi_addnode(*coord)
            
            c1, c2, c3, c4, c5, c6 = rotated_coords
            
            #add segments in clockwise fashion
            fe.mi_addsegment(*c1, *c2)
            fe.mi_addsegment(*c2, *c3)
            fe.mi_addarc(*c3, *c4, self.alpha_m_deg, 1)
            fe.mi_addsegment(*c4, *c5)
            fe.mi_addsegment(*c5, *c6)
            fe.mi_addarc(*c1, *c6, self.alpha_m_deg, 1)
            
        #connect between magnets
        alpha_between = 360/num_magnets - self.alpha_m_deg
        for i in range(num_magnets):
            start = rotate(*p5, theta*i)
            stop = rotate(*p2, theta*(i+1))
            fe.mi_addarc(*start, *stop, alpha_between, 1)
            
        if self.hollow:

            fe.mi_addnode(0, R1)            
            fe.mi_addnode(0, -R1)            
            fe.mi_addarc(0, R1, 0, -R1, 180, 1)
            fe.mi_addarc(0, -R1, 0, R1, 180, 1)
            
        self.is_drawn = True
        # self._set_magnet_materials()
        
    def set_materials(self, magnet, iron):

        R1 = self.OR - (self.dm + self.dri) #inner radius of rotor        
        R2 = self.OR - self.dm #radius to inside of PM

        #assign magnet material
        mag_center = [(R2 + self.OR)/2, 0]
        mag_orientation = 1 #1 = North facing out, -1 = North facing in

        num_magnets = 2*self.p
        theta = 360/num_magnets

        for i in range(num_magnets):
            xy = rotate(*mag_center, theta*i)
            
            #add 180 degrees if magnet faces in
            mag_dir = theta*i + 180*(mag_orientation < 0) #magnet orientation in deg
            fe.mi_addblocklabel(*xy)
            fe.mi_selectlabel(*xy)
            fe.mi_setblockprop(magnet.name, 1, 0, 0, mag_dir, 0, 0)
            fe.mi_clearselected()
            
            mag_dir *= -1 #alternate between N and S poles
            
        #assign steel material
        xy = [(R1 + R2)/2, 0]
        
        fe.mi_addblocklabel(*xy)
        fe.mi_selectlabel(*xy)
        fe.mi_setblockprop(iron.name, 1, 0, 0, 0, 1, 0)
        fe.mi_clearselected()
        
        #add air to center if rotor is hollow
        if self.hollow:
            fe.mi_addblocklabel(0, 0)
            fe.mi_selectlabel(0, 0)
            fe.mi_setblockprop('Air', 1, 0, 0, 0, 0, 0)
            fe.mi_clearselected()       
        
    def set_group(self, groupID):
        
        #select circle slightly larger than the rotor
        select_oversize = 0.001 #mm
        fe.mi_selectcircle(0, 0, self.OR + select_oversize, 4)
        fe.mi_setgroup(groupID)
        fe.mi_clearselected()

def main():
    
    fe.openfemm()
    fe.newdocument(0)
    
    rotor = PM_Rotor(dri = 50, dm = 10, dmp = 3, alpha_m = 60, p = 2, OR = 100)
    rotor.draw()
    rotor.set_materials('test', 'test')
    
    fe.mi_zoomnatural()

if __name__ == '__main__': main()
