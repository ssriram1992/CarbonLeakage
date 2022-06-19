# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils import readComplete
# %%
pf = './img/varUpGradLin_'
sf = '.csv'

# %%
anss = []

meanCPuse = 200
for upgradLin in np.arange(0,2000,100):
    data = pd.DataFrame(readComplete(str(upgradLin), 9),
        columns=['BT','MeanCT','CovCT','InvType'])
    t1 = np.array(data[(data.MeanCT==meanCPuse) ])
    t2 = np.hstack((t1, upgradLin*np.ones((t1.shape[0],1))))
    anss.append(t2)
final = np.vstack(anss)
finaldf = pd.DataFrame(final, columns=['BT','MeanCT','CovCT','InvType','UpgradLin'])
# %%
def plotInvTypeSubsidy(data, BTuse, ax=None):
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(8,8))
    bt0 = data[data.BT==BTuse]
    t0 = bt0[bt0.InvType==0]
    t1 = bt0[bt0.InvType==1]
    t2 = bt0[bt0.InvType==2]
    t3 = bt0[bt0.InvType==3]
    l1 = ax.plot(abs(t0.UpgradLin-2000), t0.CovCT, 'r.', label='Ideal')
    l2 = ax.plot(abs(t1.UpgradLin-2000), t1.CovCT, 'bx', label='Medium')
    l3 = ax.plot(abs(t2.UpgradLin-2000), t2.CovCT, 'g*', label='BAU')
    l4 = ax.plot(abs(t3.UpgradLin-2000), t3.CovCT, 'ko', label='Leakage')
    ax.set_xlabel('Linear Cost of upgrading')
    ax.set_ylabel('Spread of Carbon Tax')
    # ax.legend(loc=(1.01,0))
    ax.set_title('Border Tax = {}'.format(int(BT)))
    # fig.savefig(pf+"BT_"+str(int(BTuse))+'.png')
    return ax
    # plt.close(fig)


# %%
# for BT in np.linspace(0,100,21):
BT = 65
fig, ax = plt.subplots(3,2,figsize=(15,15))
for i, BT in enumerate([0,20,40,60,80,100]):
    plotInvTypeSubsidy(finaldf, BT, ax[i//2,i%2])
# ax = plotInvTypeSubsidy(finaldf, BT)
fig.savefig(pf+'varUpGradLin.png')


# %%
############

# %%
# %%
anss = []

CovCPuse = 0.5
for upgradLin in np.arange(0,2000,100):
    data = pd.DataFrame(readComplete(str(upgradLin), 9),
        columns=['BT','MeanCT','CovCT','InvType'])
    t1 = np.array(data[(data.CovCT==CovCPuse) ])
    t2 = np.hstack((t1, upgradLin*np.ones((t1.shape[0],1))))
    anss.append(t2)
final = np.vstack(anss)
finaldf = pd.DataFrame(final, columns=['BT','MeanCT','CovCT','InvType','UpgradLin'])
# %%
def plotInvTypeSubsidy2(data, BTuse, ax=None):
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(8,8))
    bt0 = data[data.BT==BTuse]
    t0 = bt0[bt0.InvType==0]
    t1 = bt0[bt0.InvType==1]
    t2 = bt0[bt0.InvType==2]
    t3 = bt0[bt0.InvType==3]
    l1 = ax.plot(abs(t0.UpgradLin-2000), t0.MeanCT, 'r.', label='Ideal')
    l2 = ax.plot(abs(t1.UpgradLin-2000), t1.MeanCT, 'bx', label='Medium')
    l3 = ax.plot(abs(t2.UpgradLin-2000), t2.MeanCT, 'g*', label='BAU')
    l4 = ax.plot(abs(t3.UpgradLin-2000), t3.MeanCT, 'ko', label='Leakage')
    ax.set_xlabel('Linear Cost of upgrading')
    ax.set_ylabel('Mean of Carbon Tax')
    # ax.legend(loc=(1.01,0))
    ax.set_title('Border Tax = {}'.format(int(BT)))
    # fig.savefig(pf+"BT_"+str(int(BTuse))+'.png')
    return ax
# %%
BT = 65
fig, ax = plt.subplots(3,2,figsize=(15,15))
for i, BT in enumerate([0,20,40,60,80,100]):
    plotInvTypeSubsidy2(finaldf, BT, ax[i//2,i%2])
# ax = plotInvTypeSubsidy(finaldf, BT)
fig.savefig(pf+'2.png')

# %%
