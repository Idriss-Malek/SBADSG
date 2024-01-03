from itertools import product
import numpy as np

from hcms import HCMS
from utils import EdgeSubmatrixDensity


class AnoGraphK():
    def __init__(self, Nr, Nb, K):

        """
        Initializer.

        :param Nr: The number of hash functions.
        :param Nb: The size of matrices.
        :param K: Number of iterations.
        """
        self.hcms = HCMS(Nr,Nb)
        self.K = K
    
    def learn_one(self,graph):

        """
        Updates the H-CMS structure for the new graph.

        :param graph: Graph in the form of list of edges (u,v,w,t).
        """
        self.hcms.reset()
        for (u,v,w) in graph:
            self.hcms.update(u,v,w)
    
    def score_one(self):

        """
        Computes the anomaly score of the last graph learned
        using the AnoGraph-K algorithm.

        :return: Anomaly score for the last graph learned.
        """
        Dmax = -np.inf
        for r in range(self.hcms.Nr):
            B = list(product(range(self.hcms.Nb), range(self.hcms.Nb)))
            M = self.hcms.Mat[r]
            Dmax_temp = -np.inf
            for i in range(1,self.K+1):
                hu_p,hv_p = B[0]
                Mmax = M[hu_p,hv_p]
                for j in range(1,len(B)):
                    if M[B[j]] > Mmax:
                        Mmax = M[B[j]]
                        hu_p,hv_p = B[j]
                Dmax_temp = max(Dmax_temp,EdgeSubmatrixDensity(M,hu_p,hv_p))
                B.remove((hu_p,hv_p))
            Dmax = max(Dmax,Dmax_temp)
        return Dmax