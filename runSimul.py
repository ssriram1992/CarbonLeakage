import numpy as np
# import gurobipy as gp
# import matplotlib.pyplot as plt
from utils import *
from Stage1lin import *
import sys

if __name__ == '__main__':
    args = sys.argv
    upgradeLin = 1000
    BT = 50
    uqList = [5000] + [10e3*(i+1) for i in range(5)]
    for uq in uqList:
        dataGenQuad(folder='./dat/test_'+str(uq)+'_', bordertax = BT, upgradeLin=0, upgradeQuad = uq, 
        nMeanCT=4, nDevnCT=4)
    ans = []
    nCols = 9
    for uq in uqList:
        t1 = np.genfromtxt('./dat/test_'+str(uq)+'_alldata.csv')
        t1len = t1.shape[0]
        uqCol = np.ones((t1len, 1))*uq
        t2 = np.hstack((uqCol, t1))
        ans.append(t2)
    final = np.vstack(ans)
    np.savetxt('dat/Complete_'+str(upgradeLin)+'.csv', final)




if __name__ == "__main__Old":
    args = sys.argv
    if len(args)>1:
        if len(args) <=4:
            print("Syntax: python3 runSimul.py <ugStart> <ugEnd> <ugNos>")
            exit()
        ugStart = int(args[1]) # Value of upgradeLin
        ugEnd = int(args[2])
        ugNos = int(args[3])
    else:
        ugStart = 0
        ugEnd = 2000
        ugNos = 21
    ugVals = np.linspace(0,2000,21)
    BTvals = np.linspace(0,100,21)

    for upgradeLin in ugVals:
        for BT in BTvals:
            print("***************************************")
            print("******************{}********************".format(BT))
            print("***************************************")
            dataGenQuad (folder='./dat/BT_'+str(BT)+ '_' + str(upgradeLin) +'_', bordertax = BT, upgradeLin=upgradeLin)
        nCols = 9
        anss = []
        for BT in BTvals:
            t1 = np.genfromtxt('./dat/BT_'+str(BT)+ '_' + str(upgradeLin) +'_alldata.csv')
            t1len = t1.shape[0]
            btCol = np.ones((t1len, 1))*BT
            t2 = np.hstack((btCol, t1))
            anss.append(t2)
        final = np.vstack(anss)
        np.savetxt('dat/Complete_'+str(upgradeLin)+'.csv', final)
    nCols = 10
    anss = []
    for upgradeLin in ugVals:
        t1 = np.genfromtxt('dat/Complete_'+str(upgradeLin)+'.csv')
        t1len = t1.shape[0]
        uLcol = np.ones((t1len, 1))*upgradeLin
        t2 = np.hstack((uLcol, t1))
        anss.append(t2)
    final = np.vstack(anss)
    np.savetxt('dat/upgradeLinMods_a.csv', final)
