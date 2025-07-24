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





templates = {"attempt1":"""voce é um médico e tem que determinar 
             se o seguinte exame é reagente ou não_reagente:
             
             exame:     
             analito:{DE_ANALITO1},
             resultado:{DE_RESULTADO1},
             valor_referencia:{DE_VALOR_REFERENCIA1}

             raciocínio: pense passo a passo como realizar a tarefa
             formate sua resposta da seguinte maneira:
             resposta: [reagente ou não_reagente]""",
             "attempt2":"""voce é um médico e tem que determinar 
             se o seguinte exame é reagente ou não_reagente:
             
             exame: 
             analito:{DE_ANALITO1},
             resultado:{DE_RESULTADO1},
             valor_referencia:{DE_VALOR_REFERENCIA1}

             formate sua resposta da seguinte maneira:
             resposta:[reagente ou não_reagente]""",
             "attempt3":"""voce é um médico e tem que determinar 
             se o exame é reagente ou não_reagente:
            formate sua resposta da seguinte maneira:
            resposta: [reagente ou não_reagente]
            
            Exemplo1:
            analito:{DE_ANALITO_EX1},
            resultado:{DE_RESULTADO_EX1},
            valor_referencia:{DE_VALOR_REFERENCIA_EX1}
            resposta:{resposta1}
            

            Exemplo2:
            analito:{DE_ANALITO_EX2},
            resultado:{DE_RESULTADO_EX2},
            valor_referencia:{DE_VALOR_REFERENCIA_EX2}
            resposta:{resposta2}


            Exemplo3:
            analito:{DE_ANALITO_EX3},
            resultado:{DE_RESULTADO_EX3},
            valor_referencia:{DE_VALOR_REFERENCIA_EX3}
            resposta:{resposta3}



            exame: 
            analito:{DE_ANALITO1},
            resultado:{DE_RESULTADO1},
            valor_referencia:{DE_VALOR_REFERENCIA1}

            """
             }


def evokeModelsSoro(model:str,dataframe,prompt_type:str,outputPath,outputName,modelTemp = 0.8):
    responses = []    
    start = time.time()
    aux_df = dataframe[0]
    for index,values in dataframe[0].iterrows():
            current_model = OllamaLLM(model=f"{model}",temperature=modelTemp)
            try:
                template = templates[prompt_type]
                prompt = ChatPromptTemplate.from_template(template)
                chain = prompt | current_model
                responses.append(chain.invoke(input = {
                                                        "DE_ANALITO1":values["DE_ANALITO_x"],
                                                        "DE_RESULTADO1":values["DE_RESULTADO_y"],
                                                        "DE_VALOR_REFERENCIA1":values["DE_VALOR_REFERENCIA_y"],
                                                        # "DE_ANALITO_EX1":aux_df["DE_ANALITO_x"].iloc[-3],
                                                        # "DE_RESULTADO_EX1":aux_df["DE_RESULTADO_y"].iloc[-3],
                                                        # "DE_VALOR_REFERENCIA_EX1":aux_df["DE_VALOR_REFERENCIA_y"].iloc[-3],
                                                        # "DE_ANALITO_EX2":aux_df["DE_ANALITO_x"].iloc[-2],
                                                        # "DE_RESULTADO_EX2":aux_df["DE_RESULTADO_y"].iloc[-2],
                                                        # "DE_VALOR_REFERENCIA_EX2":aux_df["DE_VALOR_REFERENCIA_y"].iloc[-2],
                                                        # "DE_ANALITO_EX3":aux_df["DE_ANALITO_x"].iloc[-1],
                                                        # "DE_RESULTADO_EX3":aux_df["DE_RESULTADO_y"].iloc[-1],
                                                        # "DE_VALOR_REFERENCIA_EX3":aux_df["DE_VALOR_REFERENCIA_y"].iloc[-1],
                                                        # "resposta1":aux_df["DE_VALOR_REFERENCIA_x"].iloc[-3],
                                                        # "resposta2":aux_df["DE_VALOR_REFERENCIA_x"].iloc[-2],
                                                        # "resposta3":aux_df["DE_VALOR_REFERENCIA_x"].iloc[-1]
                                                        }))
            except:
                print(1)
                continue
    
    end = time.time()

    f = open(f"{outputPath}/[{model}|{dataframe[1]}|{outputName}].txt",mode="a")
    f.write("__________________________________________________")
    f.write(f"""\n {model},{prompt_type},{end-start}\n""")
    for index,value in enumerate(responses):
        f.write(f'valor real: {aux_df["DE_RESULTADO_y"].iloc[index]}|')
        f.write(f"{value}\n")
    f.write("\n__________________________________________________\n")
    f.close()        
        


def callSoro(models:list,prompts:list,outputName,outputPath,InputPath,iterationNumber=1,modelsTemperature=None):
    """
    calls LLMs completion for serology experiment

    Args:
        models (list): Models to evaluate.
        prompts (list): Prompts to use.
        iterationNumber (int) : amount of times to complet 
        modelsTemperature(list[float]) : temperature parameter for each model

    """
    if modelsTemperature:
        assert len(modelsTemperature) == len(models)
        assert all(isinstance(i, float) for i in modelsTemperature)
    else:
        modelsTemperature = [0.8 for _ in models]
    path = Path(InputPath)
    
    for dataset in path.iterdir():
            data = pd.read_csv(dataset,sep = "|")
            for j,model in enumerate(models):
                for prompt in prompts:
                    for i in range(iterationNumber):
                        evokeModelsSoro(model=models[j],outputPath=outputPath,prompt_type=prompt,dataframe=[data.head(100),dataset.stem],outputName=outputName,modelTemp=modelsTemperature[j])










template_corona = {"attempt1":"""voce é um médico e tem que determinar o resultado 
             do seguinte exame de covid como detectado ou não detectado:
             exame:{EXAME},
             resultado:{RESULTADO}.

             formate sua resposta da seguinte maneira:
             resposta: [detectado ou não_detectado]"""
             }


def evokeModelsCorona(model:str,dataframe,prompt_type:str):
    """
    calls LLMs completion for Corona experiment

    Args:
        models (list): Model to evaluate.
        prompts (list): Prompt to use.
        dataframe : data for experiment
    """

    responses = []    
    start = time.time()
    for index,values in dataframe[0].iterrows():
        template = template_corona[prompt_type]
        prompt = ChatPromptTemplate.from_template(template)
        current_model = OllamaLLM(model=f"{model}")
        chain = prompt | current_model
        responses.append(chain.invoke(input = {
                                                "EXAME":values["DE_EXAME"],
                                                "RESULTADO":values["DE_RESULTADO"]
                                                }))
    end = time.time()
    f = open(f"/home/rose/Área de Trabalho/pesq2/dados/dados_exames_covid/[bode|{dataframe[1]}|novo].txt",mode="a+")
    f.write("__________________________________________________")
    f.write(f"""\n {model},{prompt_type},{end-start}\n""")
    for aux,response in enumerate(responses):
        f.write("\n==================================================\n")
        f.write(f"""valor real :{dataframe[0]["DE_RESULTADO"].iloc[aux]}""")
        f.write(response)
        f.write("\n==================================================\n")
    f.write("__________________________________________________")
    f.close()        
        


def CoronaExperiment():
    caminho = Path("/home/rose/Área de Trabalho/pesq2/dados/dados_exames_covid/entradas")
    models = ["splitpierre/bode-alpaca-pt-br:latest"]
    prompts = ["attempt1"]
    for dataset in caminho.iterdir():
        if(dataset.stem != "predições"):
            data = pd.read_csv(dataset,sep = "|")
            for model in models:
                try:
                    for prompt in prompts:
                        for i in range(1):
                            evokeModelsCorona(model=model,prompt_type=prompt,dataframe=[data.head(500),dataset.stem])
                except ValueError:
                    print(ValueError)
                    continue




callSoro(["splitpierre/bode-alpaca-pt-br:latest"],prompts=["attempt1"],iterationNumber=1,outputName="teste",)
