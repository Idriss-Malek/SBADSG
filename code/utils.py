import numpy as np

def density(M, Sx, Tx):
    """
    Density of a submatrix.

    :param M: Matrix.
    :param Sx: List of rows.
    :param Tx: List of columns.
    :return: Density.
    """
    return sum([sum([M[s][t] for t in Tx]) for s in Sx])/(np.sqrt(len(Sx)*len(Tx))+10e-6)

def R(M,hu,Tx):
    """
    Row-sum.

    :param M: Matrix.
    :param hu: Row index.
    :param Tx: List of columns.
    :return: Row-sum.
    """
    return sum([M[hu][hv] for hv in Tx])

def C(M,Sx,hv):
    """
    Column-sum.

    :param M: Matrix.
    :param Sx: List of rows.
    :param hv: Column index.
    :return: Column-sum.
    """
    return sum([M[hu][hv] for hu in Sx])

def EdgeSubmatrixDensity(M,hu,hv):
    """
    Computes the Edge Submatrix density of an edge.

    :param M: Matrix.
    :param hu: row of the matrix.
    :param hv: column of the matrix.
    :return: Edge Submatrix density of the edge.
    """
    Scur = [hu]
    Tcur = [hv]
    Srem = list(range(len(M))).remove(hu)
    Trem = list(range(len(M))).remove(hv)
    Dmax_temp = density(M,Scur,Tcur)
    while Srem or Trem:
        if Srem:
            hu_p = Srem[0]
            R_p = R(M,hu_p,Tcur)
            for i in range(1,len(Srem)):
                R_temp = R(M,Srem[i],Tcur)
                if R_temp > R_p:
                    R_p = R_temp
                    hu_p = Srem[i]
        
        if Trem:
            hv_p = Trem[0]
            C_p = C(M,Scur,hv_p)
            for i in range(1,len(Trem)):
                C_temp = C(M,Scur,Trem[i])
                if C_temp > C_p:
                    C_p = C_temp
                    hv_p = Trem[i]
        
        if R_p > C_p:
            Scur.append(hu_p)
            Srem.remove(hu_p)
        else:
            Tcur.append(hv_p)
            Trem.remove(hv_p)
        
        Dmax_temp = max(Dmax_temp,density(M,Scur,Tcur))
    return Dmax_temp