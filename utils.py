import pandas as pd

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