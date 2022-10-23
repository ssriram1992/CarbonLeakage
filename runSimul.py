import numpy as np
# import gurobipy as gp
# import matplotlib.pyplot as plt
from utils import *
from Stage1lin import *
import sys

if __name__ == '__main__':
    BTs = np.linspace(0, 250, 26)
    uqList = [i*1000 for i in [15, 17.5,20,22.5, 25]]
    for BT in BTs:
        ### For each value of border tax do the below. 
        for uq in uqList:
            dataGenQuad(folder='./dat/20221019_'+str(uq/100)+'_'+str(BT)+'_', bordertax = BT, upgradeLin=0, upgradeQuad = uq, 
            nMeanCT=26, nDevnCT=26,invURcost=120)
        ans = []
        nCols = 9
        for uq in uqList:
            t1 = np.genfromtxt('./dat/20221019_'+str(uq/100)+'_'+str(BT)+'_alldata.csv')
            t1len = t1.shape[0]
            uqCol = np.ones((t1len, 1))*uq
            t2 = np.hstack((uqCol, t1))
            ans.append(t2)
        final = np.vstack(ans)
        """
        The columns in the below file are the following in order.
        upgradeQuad, meanCTrr, devnCTrr, Qrr, Qur, invUR, emission, profits, CLtype, invType
        As a check, there should be 10 columns. 
            - invType meaning.  0 means Domestic Investment in sustainability. 1 means investment domestically as well as outisde. 
                                2 means no investment anywhere. 3 means investment only outside. 
            - CLtype meaning.   Three digits. First digit for behaviour in "low" scenario, Second digit for behaviour in "medium" scenario
                                Third digit for behavious in "high" CT scenario. In each scenario, 
                                    - 0 means no production outside or inside. 
                                    - 1 means production only domestically.
                                    - 2 means production both domestically and externally. 
                                    - 3 means production only externally. 

        """
        np.savetxt('dat/20221019Complete_'+str(BT)+'.csv', final)
    ### 
    nCols = 10
    anss = []
    for BT in BTs:
        t1 = np.genfromtxt('dat/20221019Complete_'+str(BT)+'.csv')
        t1len = t1.shape[0]
        BTcol = np.ones((t1len, 1))*BT
        t2 = np.hstack((BTcol, t1))
        anss.append(t2)
    final = np.vstack(anss)
    np.savetxt('dat/20221019BTMods.csv', final)




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
