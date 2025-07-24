import pandas as pd
from pathlib import Path
pd.set_option('mode.chained_assignment', None)
import matplotlib.pyplot as plt
from langchain_core.prompts import ChatPromptTemplate  
from langchain_ollama.llms import OllamaLLM
import re
from pathlib import Path
import subprocess
import time



def joint_soro_exam_hc(InputAdress,OutputAdress):
    data = pd.read_csv(InputAdress)
    data = data[data["DE_EXAME"].isin(["COVID-19 - PESQUISA DE ANTICORPOS IgG","CoV2-G (IgG para SARS-CoV2)"])]

    entradas = []
    pacientes = data["ID_PACIENTE"].unique()
    for paciente in list(pacientes):
        try:
            aux = data[data["ID_PACIENTE"]== paciente]
            aux["DT_COLETA"] = pd.to_datetime(aux["DT_COLETA"],format = "%Y-%m-%d")
            resultados = aux[aux["DE_ANALITO"] == "COVID-19 IgG"]
            valores = aux[aux["DE_ANALITO"] == "Índice:"]
            df = pd.DataFrame(resultados.merge(valores,on = ["DT_COLETA","ID_PACIENTE","DE_EXAME"]))
            if len(df.index):
                for index,row in df.iterrows():
                    entradas.append(row)
        except:
            continue
    aux = pd.DataFrame(entradas)
    aux = aux.drop_duplicates() 
    aux.to_csv(OutputAdress,sep = "|",index=False)

def joint_soro_exam_hsl(InputAdress,OutputAdress):
    data = pd.read_csv(InputAdress)
    data = data[data["DE_ANALITO"].isin(['Covid 19, Anticorpos IgG, índice', 'Covid 19, Anticorpos IgG'])]
    box = []
    pacientes = data["ID_PACIENTE"].unique()
    for paciente in list(pacientes):
        try:
            aux = data[data["ID_PACIENTE"]== paciente]
            aux["DT_COLETA"] = pd.to_datetime(aux["DT_COLETA"],format = "%d/%m/%Y")
            aux.sort_values(by="DT_COLETA")
            resultados = aux[aux["DE_ANALITO"] == "Covid 19, Anticorpos IgG"]
            valores = aux[aux["DE_ANALITO"].str.contains("índice")]
            df = pd.DataFrame(resultados.merge(valores,on = ["DT_COLETA","ID_PACIENTE","DE_EXAME"]))

            if len(df.index):
                for index,row in df.iterrows():
                    box.append(row)
        except:
            continue
    aux = pd.DataFrame(box)
    aux = aux.drop_duplicates() 
    aux.to_csv(OutputAdress,sep = "|",index=False)

def joint_soro_exam_fleury(InputAdress,OutputAdress):
    data = pd.read_csv(InputAdress)
    data = data[data["DE_ANALITO"].isin(["Covid 19, Anticorpos IgG, Elisa","Covid 19, Anticorpos IgG, Elisa - Índice"])]
    print(data.shape)
    box = []
    pacientes = data.ID_PACIENTE.unique()
    while(len(box)< 10000):
        i += 1 
        paciente = pacientes[i]
        try:
            aux = data[data["ID_PACIENTE"]== paciente]
            aux["DT_COLETA"] = pd.to_datetime(aux["DT_COLETA"],format = "%d/%m/%Y")
            aux.sort_values(by="DT_COLETA")
            resultados = aux[aux["DE_ANALITO"] == "Covid 19, Anticorpos IgG, Elisa"]
            valores = aux[aux["DE_ANALITO"] == "Covid 19, Anticorpos IgG, Elisa - Índice"]
            df = pd.DataFrame(resultados.merge(valores,on = ["DT_COLETA","ID_PACIENTE","DE_EXAME"]))
            if len(df.index):
                for index,row in df.iterrows():
                    box.append(row)
        except:
                continue
    aux = pd.DataFrame(box)
    aux = aux.drop_duplicates() 
    aux.to_csv(OutputAdress,sep = "|",index=False)

def joint_soro_exam_bpsp(InputAdress,OutputAdress):
    data = pd.read_csv(InputAdress)
    pacientes = data["ID_PACIENTE"].unique()
    for paciente in list(pacientes):
        try:
            aux = data[data["ID_PACIENTE"]== paciente]
            aux["DT_COLETA"] = pd.to_datetime(aux["DT_COLETA"],format = "%d/%m/%Y")
            resultados = aux[aux["DE_ANALITO"].isin(["Covid 19, Anticorpos IgG","Covid 19, Anticorpos IgG, teste rapido"])]
            valores = aux[aux["DE_ANALITO"] == "Covid 19, Anticorpos IgG, indice"]
            df = pd.DataFrame(resultados.merge(valores,on = ["DT_COLETA","ID_PACIENTE","DE_EXAME"]))
            if len(df.index):
                for index,row in df.iterrows():
                    box.append(row)
        except:
            continue
    aux = pd.DataFrame(box)
    aux.to_csv(OutputAdress,sep = "|",index=False)


def joint_soro_exam_einstein(InputAdress,OutputAdress):
    data = pd.read_csv(InputAdress)
    data["DE_ANALITO"].unique()
    box = []
    pacientes = data["ID_PACIENTE"].unique()
    for paciente in list(pacientes):
        try:
            aux = data[data["ID_PACIENTE"]== paciente]
            aux["DT_COLETA"] = pd.to_datetime(aux["DT_COLETA"],format = "%d/%m/%Y")
            resultados = aux[aux["DE_ANALITO"].isin(["COVID IgG Interp"])]
            valores = aux[aux["DE_ANALITO"] == "IgG, COVID19"]
            df = pd.DataFrame(resultados.merge(valores,on = ["DT_COLETA","ID_PACIENTE","DE_EXAME"]))
            if len(df.index):
                for index,row in df.iterrows():
                    box.append(row)
        except:
            continue
    aux = pd.DataFrame(box)
    aux.to_csv(OutputAdress,sep = "|",index=False)

def plot_hc(InputAdress):
    find_color = lambda valor: "red" if valor == "Reagente" else "black"

    dadinhos = pd.read_csv(InputAdress,sep = "|")

    dadinhos = dadinhos[["DE_EXAME","DE_RESULTADO_x","DE_RESULTADO_y","DE_VALOR_REFERENCIA_x"]]
    dadinhos["cor"] = dadinhos["DE_RESULTADO_x"].apply(find_color)
    preto = dadinhos[dadinhos["cor"]== "black"]
    vermelho = dadinhos[dadinhos["cor"] == "red"]
    plt.figure(figsize=(15,10))
    plt.scatter([i/len(preto) for i in range(len(preto))],[i for i in preto["DE_RESULTADO_y"].values],color = "black",label="Reagente")
    plt.scatter([i/len(vermelho) for i in range(len(vermelho))],[i for i in vermelho["DE_RESULTADO_y"].values],color = "red",label = "Não Reagente")
    plt.plot([i for i in range(0,2)],[1.1 for i in range(0,2)], label = "reta contorno")
    plt.title("COVID-19 - PESQUISA DE ANTICORPOS IgG (hc)")
    plt.xlabel('Numero do exame')
    plt.ylabel('Resultado do exame')
    plt.legend(loc="upper left")
    plt.show()

def plot_hsl(InputAdress):
    find_color = lambda valor: "red" if valor == "REAGENTE" else "black"
    dadinhos = pd.read_csv(InputAdress,sep = "|")
    dadinhos = dadinhos[["DE_EXAME","DE_RESULTADO_x","DE_RESULTADO_y","DE_VALOR_REFERENCIA_x"]]
    dadinhos["cor"] = dadinhos["DE_RESULTADO_x"].apply(find_color)
    preto = dadinhos[dadinhos["cor"]== "black"]
    vermelho = dadinhos[dadinhos["cor"] == "red"]

    plt.figure(figsize=(15,10))
    plt.scatter([i/len(preto) for i in range(len(preto))],[i for i in preto["DE_RESULTADO_y"].values],color = "black",label="Reagente")
    plt.scatter([i/len(vermelho) for i in range(len(vermelho))],[i for i in vermelho["DE_RESULTADO_y"].values],color = "red",label = "Não Reagente")
    plt.plot([i for i in range(0,2)],[1.1 for i in range(0,2)], label = "reta contorno")
    plt.title("COVID-19 - PESQUISA DE ANTICORPOS IgG (hsl)")
    plt.xlabel('Numero do exame')
    plt.ylabel('Resultado do exame')
    plt.legend(loc="upper left")
    plt.show()

def plot_fleury(InputAdress):
    find_color = lambda valor: "red" if valor == "REAGENTE" else "gray" if valor == "Indeterminado" else "black"

    dadinhos = pd.read_csv(InputAdress,sep = "|")
    dadinhos = dadinhos.drop_duplicates()
    dadinhos = dadinhos[dadinhos["DE_RESULTADO_y"] != 'inferior a 1.01']
    dadinhos = dadinhos[["DE_RESULTADO_x","DE_RESULTADO_y"]]
    dadinhos["cor"] = dadinhos["DE_RESULTADO_x"].apply(find_color)
    dadinhos["DE_RESULTADO_y"] =dadinhos["DE_RESULTADO_y"].astype("float")

    preto = dadinhos[dadinhos["cor"]== "black"]
    vermelho = dadinhos[dadinhos["cor"] == "red"]
    cinza = dadinhos[dadinhos["cor"] == "gray"]

    plt.figure(figsize=(15,10))

    plt.scatter([i/len(preto) for i in range(len(preto))],[i for i in preto["DE_RESULTADO_y"].values],color = "black",label="Reagente")
    plt.scatter([i/len(vermelho) for i in range(len(vermelho))],[i for i in vermelho["DE_RESULTADO_y"].values],color = "red",label = "Não Reagente")
    plt.scatter([i/len(cinza) for i in range(len(cinza))],[i for i in cinza["DE_RESULTADO_y"].values],color = "gray",label = "Indeterminado")

    plt.plot([i for i in range(0,2)],[1.1 for i in range(0,2)], label = "reta contorno")
    plt.ylim((10**-1)*2,10**1)
    plt.title("COVID-19 - PESQUISA DE ANTICORPOS IgG (fleury)")
    plt.xlabel('Numero do exame')
    plt.ylabel('Resultado do exame')
    plt.legend(loc="upper left")
    plt.show()

def plot_bpsp(InputAdress):
    find_color= lambda valor : "red" if valor == "REAGENTE" else "black"

    dadinhos = pd.read_csv(InputAdress,sep = "|")
    dadinhos = dadinhos.drop_duplicates()
    dadinhos = dadinhos[["DE_RESULTADO_x","DE_RESULTADO_y"]]
    dadinhos["cor"] = dadinhos["DE_RESULTADO_x"].apply(find_color)
    dadinhos["DE_RESULTADO_y"] =dadinhos["DE_RESULTADO_y"].astype("float")

    preto = dadinhos[dadinhos["cor"]== "black"]
    vermelho = dadinhos[dadinhos["cor"] == "red"]

    plt.figure(figsize=(15,10))
    plt.scatter([i/len(preto) for i in range(len(preto))],[i for i in preto["DE_RESULTADO_y"].values],color = "black",label="Reagente")
    plt.scatter([i/len(vermelho) for i in range(len(vermelho))],[i for i in vermelho["DE_RESULTADO_y"].values],color = "red",label = "Não Reagente")
    plt.plot([i for i in range(0,2)],[1.1 for i in range(0,2)], label = "reta contorno")
    plt.title("COVID-19 - PESQUISA DE ANTICORPOS IgG (bpsp)")
    plt.xlabel('Numero do exame')
    plt.ylabel('Resultado do exame')
    plt.legend(loc="upper left")
    plt.show()

def plot_einstein(InputAdress):
    find_color = lambda valor: "red" if valor == "Reagente" else "gray" if valor == "Indeterminado" else "black"

        
    dadinhos = pd.read_csv(InputAdress,sep = "|")
    dadinhos = dadinhos.drop_duplicates()
    dadinhos = dadinhos[["DE_RESULTADO_x","DE_RESULTADO_y"]]
    dadinhos["DE_RESULTADO_y"].unique()

    dadinhos= dadinhos[dadinhos["DE_RESULTADO_y"] != "NOVA COLETA"]
    dadinhos= dadinhos[dadinhos["DE_RESULTADO_y"] != "nova coleta"]
    dadinhos= dadinhos[dadinhos["DE_RESULTADO_y"] != '>200.00']

    dadinhos["cor"] = dadinhos["DE_RESULTADO_x"].apply(find_color)
    dadinhos["DE_RESULTADO_y"] =dadinhos["DE_RESULTADO_y"].astype("float")


    preto = dadinhos[dadinhos["cor"]== "black"]
    vermelho = dadinhos[dadinhos["cor"] == "red"]
    cinza =  dadinhos[dadinhos["cor"] == "gray"]

    plt.figure(figsize=(15,10))
    plt.scatter([i/len(preto) for i in range(len(preto))],[i for i in preto["DE_RESULTADO_y"].values],color = "black",label="Reagente")
    plt.scatter([i/len(vermelho) for i in range(len(vermelho))],[i for i in vermelho["DE_RESULTADO_y"].values],color = "red",label = "Não Reagente")
    plt.scatter([i/len(cinza) for i in range(len(cinza))],[i for i in cinza["DE_RESULTADO_y"].values],color = "gray",label = "Indeterminado")
    plt.plot([i for i in range(0,2)],[1.1 for i in range(0,2)], label = "reta contorno")
    plt.title("COVID-19 - PESQUISA DE ANTICORPOS IgG (einstein)")
    plt.xlabel('Numero do exame')
    plt.ylabel('Resultado do exame')
    plt.ylim((10**-1)*2,10**1)
    plt.title
    plt.legend(loc="upper left")
    plt.show()

plot_fleury()