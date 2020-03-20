import requests 
import pandas as pd
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure



def getData():
    data = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"		        )
    data["data"] = pd.to_datetime(data["data"]).apply(lambda x: x.date())
    return data     
    

def FattoreAumento(regione: str, df: pd.DataFrame, azione:str ):
    index=0
    val=0
    y = []  
    data = []  
    for i,valore in df.iterrows():
        if(valore.denominazione_regione == regione):
            if(index==0):
                val = valore[azione]
            elif(index!=0):
                if val!=0:
                    y.append(round(valore[azione]/(val),4))
                else:
                    y.append(round(valore[azione],4))
                val=valore[azione]
                data.append(valore.data)
            index+=1
            print(valore)    
    print(y)
    PlottingData(data,y,regione,azione)


def TotaleAumento(regione: str, df: pd.DataFrame, azione:str ):
    index=0
    val=0
    y = []  
    data = []  
    for i,valore in df.iterrows():
        if(valore.denominazione_regione == regione):
            if(index==0):
                val = valore[azione]
            elif(index!=0):
                y.append(valore[azione]-val)
                val=valore[azione]
                data.append(valore.data)
            index+=1
               
    print(regione, y)
    PlottingData(data,y,regione,azione)
    
    
def TotaleValori(regione: str, df: pd.DataFrame, azione:str ):
    y = []  
    data = []  
    for i,valore in df.iterrows():
        if(valore.denominazione_regione == regione):
                y.append(valore[azione])
                data.append(valore.data)
        print(valore)    
    print(regione , y)
    PlottingData(data,y,regione,azione)
    
fig, ax = plt.subplots()

def PlottingData(x,y,regione:str,azione:str):
   
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
    plt.xlabel('data')
    plt.ylabel(azione)
    plt.plot(x,y, label=regione)

    plt.title('Aumento ' + azione)
    fig.set_size_inches(18.5, 10.5, forward=True)
    plt.legend();
    plt.grid(True)








data = getData()

fig, ax = plt.subplots()





regioni=[]
for val in data.itertuples():
    regioni.append(val.denominazione_regione)
regioni=list(set(regioni))


for regione in regioni:
    FattoreAumento(regione,data,'totale_attualmente_positivi')






plt.show()