import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils import readComplete

def typeTrans(row):
    """
    Ensure that the type is a string with three characters.
    Then transforms that in a row. 
    This function is a temporary function, written to be used like 
    a lambda function for pd.DataFrame.apply()
    """
    t1 = str(int(row.Type))
    while len(t1) < 3:
        t1 = '0'+t1
    t2 = pd.Series(list(t1), index=['lowType','medType','hiType'])
    return t2

    
def plotIt(data, BT):
    """
    Given a dataframe, and a value of border tax, 
    filters the rows of data frame only corresponding to the given border tax. 
    Then, it plots the data, showing what is the production policy in each of 
    high, medium and low scenarios. 
    """
    bt0 = data[data.BT==BT]
    fig, (ax0,ax1,ax2) = plt.subplots(3,1,figsize=(10,10), sharex=True)
    def subPlotPrdType(ax,reducedDf, c, name=''):
        (c0,c1,c2,c3) = c
        t0 = bt0[reducedDf=='0']
        t1 = bt0[reducedDf=='1']
        t2 = bt0[reducedDf=='2']
        t3 = bt0[reducedDf=='3']
        # l1 = ax.plot(t0.MeanCT, t0.CovCT, c0, label='No production')
        # l2 = ax.plot(t1.MeanCT, t1.CovCT, c1, label='Only in Policy Region')
        # l3 = ax.plot(t2.MeanCT, t2.CovCT, c2, label='Both Policy Region and Offshore Region')
        # l4 = ax.plot(t3.MeanCT, t3.CovCT, c3, label='Only in Offshore Region')
        l1 = ax.plot(t0.MeanCT, t0.CovCT, c0, label='(0, 0)')
        l2 = ax.plot(t1.MeanCT, t1.CovCT, c1, label='(>0, 0)')
        l3 = ax.plot(t2.MeanCT, t2.CovCT, c2, label='(>0, >0)')
        l4 = ax.plot(t3.MeanCT, t3.CovCT, c3, label='(>0, >0)')
        ax.set_title(name)
        return (l1,l2,l3,l4)
    subPlotPrdType(ax0, bt0.lowType, ('r.','bx','g*','ko'), name='Low Carbon Price')
    subPlotPrdType(ax1, bt0.medType, ('r.','bx','g*','ko'), name='Medium Carbon Price')
    subPlotPrdType(ax2, bt0.hiType, ('r.','bx','g*','ko'), name='High Carbon Price')
    # fig.suptitle('Border Tax = {}'.format(int(BT)))
    # fig.suptitle("Operational policy under different realisations of Carbon Price")
    ax2.legend(loc=(0.98,0))
    fig.savefig(pf+"BT_"+str(int(BT))+'.png')

if __name__ == "__main__":
    pf = './dat/run_20220417/Complete_'
    sf = '.csv'
    name = str(1000)
    data = pd.DataFrame(readComplete(name, 8),
            columns=['BT','MeanCT','CovCT','Type'])
    data = data.join(data.apply(typeTrans, axis=1))
    # for BT in np.linspace(0,100,21):
        # plotIt(data, BT)
    plotIt(data, 70)
