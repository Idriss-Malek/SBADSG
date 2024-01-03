import numpy as np

from hcms import HCMS
from utils import density,R,C

class AnoGraph():
    def __init__(self, Nr, Nb):
        """
        Initializer.

        :param Nr: The number of hash functions.
        :param Nb: The size of matrices.
        """
        self.hcms = HCMS(Nr,Nb)
    
    def learn_one(self,graph):
        """
        Updates the H-CMS structure for the new graph.

        :param graph: Graph in the form of list of edges (u,v,w).
        """
        self.hcms.reset()
        for (u,v,w) in graph:
            self.hcms.update(u,v,w)
    
    def score_one(self):
        """
        Computes the anomaly score of the last graph learned
        using the AnoGraph algorithm.

        :return: Anomaly score for the last graph learned.
        """
        Dmax = -np.inf
        for r in range(self.hcms.Nr):
            M = self.hcms.Mat[r]
            Scur = list(range(self.hcms.Nb))
            Tcur = list(range(self.hcms.Nb))
            Dmax_temp = density(M,Scur,Tcur)
            while len(Scur) > 0 or len(Tcur) > 0:
                if Scur:
                    hu_p = Scur[0]
                    R_p = R(M,hu_p,Tcur)
                    for i in range(1,len(Scur)):
                        R_temp = R(M,Scur[i],Tcur)
                        if R_temp < R_p:
                            R_p = R_temp
                            hu_p = Scur[i]
                
                if Tcur:
                    hv_p = Tcur[0]
                    C_p = C(M,Scur,hv_p)
                    for i in range(1,len(Tcur)):
                        C_temp = C(M,Scur,Tcur[i])
                        if C_temp < C_p:
                            C_p = C_temp
                            hv_p = Tcur[i]
                if R_p < C_p:
                    Scur.remove(hu_p)
                else:
                    Tcur.remove(hv_p)
                Dmax_temp = max(Dmax_temp,density(M,Scur,Tcur))
            Dmax = max(Dmax,Dmax_temp)
        return Dmax