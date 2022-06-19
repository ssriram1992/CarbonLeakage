# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils import readComplete

# %%
pf = './dat/run_20220417/Complete_'
sf = '.csv'

name = str(2000)
data = pd.DataFrame(readComplete(name, 9),
        columns=['BT','MeanCT','CovCT','InvType'])
# %%
def plotInvType(data, BT, ax = None):
    """
    Given a dataframe, and a value of border tax, 
    filters the rows of data frame only corresponding to the given border tax. 
    Then, it plots the data, showing what is the investment policy 
    """
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(10,10))
    bt0 = data[data.BT==BT]
    t0 = bt0[bt0.InvType==0]
    t1 = bt0[bt0.InvType==1]
    t2 = bt0[bt0.InvType==2]
    t3 = bt0[bt0.InvType==3]
    l1 = ax.plot(t0.MeanCT, t0.CovCT, 'r.', label='Ideal')
    l2 = ax.plot(t1.MeanCT, t1.CovCT, 'bx', label='Medium')
    l3 = ax.plot(t2.MeanCT, t2.CovCT, 'g*', label='BAU')
    l4 = ax.plot(t3.MeanCT, t3.CovCT, 'ko', label='Leakage')
    ax.set_xlabel('Mean of Carbon Tax')
    ax.set_ylabel('Spread of Carbon Tax')
    ax.set_title('Border Tax = {}'.format(int(BT)))
    # fig.savefig(pf+"BT_"+str(int(BT))+'.png')

# %%
# for BT in np.linspace(0,100,21):
#     plotInvType(data, BT)
# %%
fig, ax = plt.subplots(3,2,figsize=(15,15))
for i, BT in enumerate([0,20,40,60,80,100]):
    plotInvType(data, BT, ax[i//2,i%2])
# fig.suptitle("Investment Policy")
fig.savefig(name+"_InvPol.png")
print(name+"_InvPol.png")
# %%
