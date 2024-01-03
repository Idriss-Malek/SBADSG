import numpy as np
class HCMS:
    def __init__(self, Nr, Nb):
        """
        Initializer.

        :param Nr: Number of hash functions.
        :param Nb: Size of the matrices.
        """
        self.Nr = Nr
        self.Nb = Nb

        self.Mat = np.zeros((self.Nr,self.Nb,self.Nb))
        self.a = np.random.randint(0,self.Nb, size = self.Nr)
        self.b = np.random.randint(0,self.Nb, size = self.Nr)
    
    def h(self, x, r):
        """
        Hash function

        :param x: Element to hash.
        :param r: Row number indicating which hashing function to use.
        :return: The anomaly score of the edge.
        """
        return (self.a[r]*x+self.b[r])%self.Nb

    def reset(self):
        """
        Reset the matrices to 0.
        """
        self.Mat = np.zeros((self.Nr,self.Nb,self.Nb))
    
    def update(self,u,v,w):
        """
        Updates the matrices with a new weight.

        :param u: Source node.
        :param v: Destination node.
        :param w: Weight of the edge.
        """
        for r in range(self.Nr):
            self.Mat[r,self.h(u,r),self.h(v,r)] += w
    
    def decay(self,alpha):
        """
        Decays the matrices.

        :param alpha: Decay factor.
        """
        self.Mat *= alpha
    