from hcms import HCMS
from utils import EdgeSubmatrixDensity

class AnoEdgeG():
    def __init__(self, Nr, Nb, alpha):
        """
        Initializer.

        :param Nr: Number of hash functions.
        :param Nb: Size of the matrices.
        :param alpha: Decay factor.
        """
        self.hcms = HCMS(Nr,Nb)
        self.t = 0
        self.alpha = alpha
    
    def learn_one(self,edge):
        """
        Updates the H-CMS structure with the new edge.

        :param edge: Edge in the form of (u,v,w,t).
        """
        u,v,w,t = edge
        if t > self.t:
            self.t = t
            self.hcms.decay(self.alpha)
        self.hcms.update(u,v,w)
    
    def score_one(self,u,v):
        """
        Anomaly score of the edge with the AnoEdgeG algorithm.

        :param u: Source.
        :param v: Destination.
        :return: The anomaly score of the edge.
        """
        densities = []
        for r in range(self.hcms.Nr):
            densities.append(EdgeSubmatrixDensity(self.hcms.Mat[r],self.hcms.h(u,r),self.hcms.h(v,r)))
        return min(densities)

            
            