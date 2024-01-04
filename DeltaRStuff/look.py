from ROOT import TFile, TLorentzVector
from more_itertools import distinct_permutations
from itertools import combinations
from itertools import permutations as perm
from itertools import chain
from more_itertools import unique_everseen
import time
f = TFile.Open("X300A15/F8CDC574-C9F3-3F40-882B-2406F533A586.root")
events = f.Events

def Reverse(v):
    new_tup = v[::-1]
    return new_tup

def RmRev(v):
    temp = []
    for i in v:
        if i in temp or Reverse(i) in temp:
            continue
        if i not in temp:
            temp.append(i)
    return temp
start = time.time()
'''
for e in range(0,2):
    events.GetEntry(e)
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    vec = [[pt[i],eta[i],phi[i],m[i]] for i in range(len(pt))]
    comb = unique_everseen(combinations(vec,2))
    for c in comb:
        print("Entry")



        #print(c[0][0],c[0][1],c[0][2],c[0][3])
        #print(c[1][0],c[1][1],c[1][2],c[1][3])
        #photon0 = TLorentzVector()
        #photon1 = TLorentzVector()
        #photon0.SetPtEtaPhiM(c[0][0],c[0][1],c[0][2],c[0][3])
        #photon1.SetPtEtaPhiM(c[1][0],c[1][1],c[1][2],c[1][3])
        #dR = photon1.DeltaR(photon0)
        
'''
for e in range(0,2):
    events.GetEntry(e) 
    pt = events.Photon_pt
    eta = events.Photon_eta
    phi = events.Photon_phi 
    m = events.Photon_mass
    for i in range(0,len(pt)):
        #photon0 = TLorentzVector()
        #photon0.SetPtEtaPhiM(pt[i],eta[i],phi[i],m[i])
        #print("Count")
        for j in range(0,len(pt)):
            if i >= j:
                continue
            print(" Count Count")
          #photon1 = TLorentzVector()
            #photon1.SetPtEtaPhiM(pt[j],eta[j],phi[j],m[j])
            #dR = photon1.DeltaR(photon0)
         
    
print("Time Elapsed: ", time.time()-start) 



            
