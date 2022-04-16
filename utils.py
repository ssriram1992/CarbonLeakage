import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def write2xl(dfs, SheetNames, filename="output.xlsx"):
    assert len(dfs) == len(SheetNames), "Unequal number of dataframes ({}) and sheets ({})".format(dfs, SheetNames)
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    for dd, ss in zip(dfs, SheetNames):
        if dd.empty:
            print('Nothing to write in '+ss+'. Empty Dataframe.')
            pd.DataFrame({'Label':['Data'],'Value':['Not available']}).set_index(['Label']).to_excel(writer, sheet_name=ss)
        else:
            dd.to_excel(writer, sheet_name=ss)
    writer.save()

def plotIt(xx, yy, zz, xl = "Mean Tax", yl = "Spread of Tax", title="", folder = "./data1/"):
    plt.contourf(xx, yy, zz, cmap='RdBu')
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.title(title)
    plt.colorbar()
    # plt.show()
    def clean(string):
        return string.replace(" ", "")
    plt.savefig(folder+clean(title)+".png")
    plt.close('all')
    np.savetxt(folder+clean(title)+".csv", zz, delimiter=',')