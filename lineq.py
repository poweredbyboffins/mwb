import numpy as np
from scipy.linalg import *

def le_solve():
    ar = np.array ([[0.6,0,0.5661,0.2234,0.1975]
,[0,0.9,0.5486,0.2791,0.1693]
,[0,-0.47,0.1104,0.1614,0.6859]
,[0.14,0,0.5598,0.214,0.2082]
#,[0.33,3,0.5492,0.3006,0.1484]
,[0,-0.2,0.532,0.1617,0.7635]]);

    #print ar

    P,L,U = lu(ar)

    #v= array ([3,3,2,1,2]);
    v= np.array ([3,3,2,1,3]);

    s = solve(ar,np.transpose(v))
    print s

    X=np.linalg.lstsq(ar,v)
    print X[0]

le_solve()


