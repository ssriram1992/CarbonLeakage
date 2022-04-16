import numpy as np
import gurobipy as gp
import matplotlib.pyplot as plt
from utils import *
import Stage1 

def dataGenLin():
    """
    This function roughly reproduces the result in Huang et al. 
    """
    mean = np.array([100+i*15 for i in range(11)])
    # devn = np.array([5*i for i in range(21)])
    devn = np.array([i*0.1 for i in range(21)]) # Coefficient of variation
    meanGrid, devnGrid = np.meshgrid(mean, devn)
    print(meanGrid.shape)
    Qrr = np.zeros_like(meanGrid)
    Qur = np.zeros_like(meanGrid)
    invUR = np.zeros_like(meanGrid)
    emission = np.zeros_like(meanGrid)
    profits = np.zeros_like(meanGrid)
    CLtype = np.zeros_like(meanGrid)
    invType = np.zeros_like(meanGrid)
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
    np.savetxt("./data1/xx.csv",meanGrid, delimiter=',')
    np.savetxt("./data1/yy.csv",devnGrid, delimiter=',')
    plotIt(meanGrid, devnGrid, Qrr, title = "Exp Qty in RR")
    plotIt(meanGrid, devnGrid, Qur, title = "Exp Qty in UR")
    plotIt(meanGrid, devnGrid, invUR, title = "Capacity Inv in UR")
    plotIt(meanGrid, devnGrid, emission, title = "Tech Emission in RR")
    plotIt(meanGrid, devnGrid, profits, title = "Profits")
    plotIt(meanGrid, devnGrid, CLtype, title = "Types")
    plotIt(meanGrid, devnGrid, invType, title = "Investment Types")

def dataGenQuad():
    """
    This function roughly reproduces the result in Huang et al. 
    """
    mean = np.array([100+i*15 for i in range(11)])
    # devn = np.array([5*i for i in range(21)])
    devn = np.array([i*0.05 for i in range(21)]) # Coefficient of variation
    meanGrid, devnGrid = np.meshgrid(mean, devn)
    print(meanGrid.shape)
    Qrr = np.zeros_like(meanGrid)
    Qur = np.zeros_like(meanGrid)
    invUR = np.zeros_like(meanGrid)
    emission = np.zeros_like(meanGrid)
    profits = np.zeros_like(meanGrid)
    CLtype = np.zeros_like(meanGrid)
    invType = np.zeros_like(meanGrid)
    for i in range(len(devn)):
        for j in range(len(mean)):
            input = {'Low':meanGrid[i,j]-devnGrid[i,j]*meanGrid[i,j], "Mid": meanGrid[i,j], 'High':meanGrid[i,j]+devnGrid[i,j]*meanGrid[i,j]}
            stage1 = Stage1.Stage1(DemInt = 200, DemSl = 1, invURcost = 100,
                costLrrBase = 10, CostLrr_l = 10, CostLrr_q = 0,
                costQrrBase = 0.1, upgradeLin = 0, upgradeQuad = 20000,
                CTrrs = input, borderTax = 10,
                costLur = 10, costQur = 0.1, CTur = 0)
            ans = stage1.solve()
            print(input, " ---------- ", ans)
            Qrr[i,j] = ans['E-Qrr']
            Qur[i,j] = ans['E-Qur']
            invUR[i,j] = ans['invUR']
            profits[i,j] = ans['profit']
            emission[i,j] = ans['emission']
            lookup = {"N":0, "R":1, "B":2, "U":3}
            CLtype[i, j] = lookup[ans['CLtype']["Low"]]*100 + lookup[ans['CLtype']["Mid"]]*10 + lookup[ans['CLtype']["High"]]
            lookup = {'I':0, 'M':1, 'B':2, 'P':3}
            invType[i,j] = lookup[ans['invType']]

    np.savetxt("./data1/xx.csv",meanGrid, delimiter=',')
    np.savetxt("./data1/yy.csv",devnGrid, delimiter=',')
    plotIt(meanGrid, devnGrid, Qrr, title = "Exp Qty in RR")
    plotIt(meanGrid, devnGrid, Qur, title = "Exp Qty in UR")
    plotIt(meanGrid, devnGrid, invUR, title = "Capacity Inv in UR")
    plotIt(meanGrid, devnGrid, emission, title = "Tech Emission in RR")
    plotIt(meanGrid, devnGrid, profits, title = "Profits")
    plotIt(meanGrid, devnGrid, CLtype, title = "Carbon Leakage Types")
    plotIt(meanGrid, devnGrid, invType, title = "Investment Types")


if __name__ == "__main__":
    dataGenQuad  ()
    # print(ans) # expQrrval, expQurval, invURval, M.objVal, emission, type

