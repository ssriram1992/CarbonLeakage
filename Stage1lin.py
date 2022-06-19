import numpy as np
# import gurobipy as gp
# import matplotlib.pyplot as plt
import pandas as pd
from utils import *
import Stage1

def makeOutputProtoTypes(xGridder, yGridder):
    xGrid, yGrid = np.meshgrid(xGridder, yGridder)
    Qrr = np.zeros_like(xGrid)
    Qur = np.zeros_like(xGrid)
    invUR = np.zeros_like(xGrid)
    emission = np.zeros_like(xGrid)
    profits = np.zeros_like(xGrid)
    CLtype = np.zeros_like(xGrid)
    invType = np.zeros_like(xGrid)
    return xGrid, yGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType

def writedata(xGrid, yGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType, folder = './data1/'):
    np.savetxt(folder+"xx.csv",xGrid, delimiter=',')
    np.savetxt(folder+"yy.csv",yGrid, delimiter=',')
    # plotIt(xGrid, yGrid, Qrr, title = "Exp Qty in RR", folder=folder)
    # plotIt(xGrid, yGrid, Qur, title = "Exp Qty in UR", folder=folder)
    # plotIt(xGrid, yGrid, invUR, title = "Capacity Inv in UR", folder=folder)
    # plotIt(xGrid, yGrid, emission, title = "Tech Emission in RR", folder=folder)
    # plotIt(xGrid, yGrid, profits, title = "Profits", folder=folder)
    # plotIt(xGrid, yGrid, CLtype, title = "Types", folder=folder)
    # plotIt(xGrid, yGrid, invType, title = "Investment Types", folder=folder)
    bigArray = np.array([xGrid, yGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType]).reshape(9,-1).T
    # df = pd.DataFrame(bigArray, columns=['x', 'y', 'Qrr', 'Qur', 'invUR', 'emission', 'profits', 'CLtype', 'invType'])
    np.savetxt(folder+"alldata.csv",bigArray,delimiter=' ')
    return bigArray
    # write2xl([df],['allData'])


def dataGenLin():
    """
    This function roughly reproduces the result in Huang et al.
    """
    mean = np.array([100+i*15 for i in range(11)])
    # devn = np.array([5*i for i in range(21)])
    devn = np.array([i*0.1 for i in range(21)]) # Coefficient of variation
    meanGrid, devnGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType = makeOutputProtoTypes(mean, devn)
    for i in range(len(devn)):
        for j in range(len(mean)):
            input = {'Low':meanGrid[i,j]-devnGrid[i,j]*meanGrid[i,j], 'High':meanGrid[i,j]+devnGrid[i,j]*meanGrid[i,j]}
            stage1 = Stage1.Stage1(CTrrs = input)
            ans = stage1.solve()
            print(input, " ---------- ", ans)
            Qrr[i,j] = ans['E-Qrr']
            Qur[i,j] = ans['E-Qur']
            invUR[i,j] = ans['invUR']
            profits[i,j] = ans['profit']
            emission[i,j] = ans['emission']
            lookup = {"N":0, "R":1, "B":2, "U":3}
            CLtype[i, j] = lookup[ans['CLtype']["Low"]]*10 + lookup[ans['CLtype']["High"]]
            lookup = {'I':0, 'M':1, 'B':2, 'P':3}
            invType[i,j] = lookup[ans['invType']]
    writedata(meanGrid, devnGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType, folder = './data1/')

def dataGenQuad(folder='./data1/', bordertax=10, upgradeLin = 0, upgradeQuad=20000):
    """
    This function roughly reproduces the result in Huang et al.
    """
    mean = np.linspace(0,250,26)
    devn = np.linspace(0,1,21)
    meanGrid, devnGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType = makeOutputProtoTypes(mean, devn)
    for i in range(len(devn)):
        for j in range(len(mean)):
            input = {'Low':meanGrid[i,j]-devnGrid[i,j]*meanGrid[i,j],
                    "Mid": meanGrid[i,j],
                    'High':meanGrid[i,j]+devnGrid[i,j]*meanGrid[i,j]}
            stage1 = Stage1.Stage1(DemInt = 200, DemSl = 1, invURcost = 100,
                costLrrBase = 15, CostLrr_l = 10, CostLrr_q = 0,
                costQrrBase = 0.1, upgradeLin = upgradeLin, upgradeQuad = upgradeQuad,
                CTrrs = input, borderTax = bordertax,
                costLur = 10, costQur = 0.1, CTur = 0)
            ans = stage1.solve()
            Qrr[i,j] = ans['E-Qrr']
            Qur[i,j] = ans['E-Qur']
            invUR[i,j] = ans['invUR']
            profits[i,j] = ans['profit']
            emission[i,j] = ans['emission']
            lookup = {"N":0, "R":1, "B":2, "U":3}
            CLtype[i, j] = lookup[ans['CLtype']["Low"]]*100 + lookup[ans['CLtype']["Mid"]]*10 + lookup[ans['CLtype']["High"]]
            lookup = {'I':0, 'M':1, 'B':2, 'P':3}
            invType[i,j] = lookup[ans['invType']]
            input['BT'] = bordertax
            dictPrint(input, end="-----\t{:.1f}\t------\n\t".format(upgradeLin))
            dictPrint(ans)
    return writedata(meanGrid, devnGrid, Qrr, Qur, invUR, emission, profits, CLtype, invType, folder = folder)


if __name__ == "__main__":

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