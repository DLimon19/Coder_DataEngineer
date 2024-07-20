import pandas as pd
import urllib.request
import json


try:
    flag = True
    #print(f"Adquiriendo data para la fecha: {kwargs["exec_date"]}")
    #date = datetime.strptime(kwargs["exec_date"], '%Y-%m-%d %H')
    # Se hace el request a la API de covid 
    if flag == True:
        response = urllib.request.urlopen("https://coronavirus.m.pipedream.net/").read()
        if response:
            print('Llamada a la API exitosa!')
            # Se convierte la respuesta en un json
            data = json.loads(response)
            # Se crea un archivo json en el directorio ./raw_data/ y se le cargan los datos
            #with open(kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json", "w") as json_file:
            #        json.dump(data["rawData"], json_file)
            data_pd = pd.json_normalize(data["rawData"])
            #print(data_pd.head())
        else:
            print('An error has occured!')

    #request a api de paises de habla hispana
    
    response2 = urllib.request.urlopen("https://restcountries.com/v3.1/lang/spanish").read()
    if response2:
        print('Llamada a la API exitosa!')
        # Se convierte la respuesta en un json
        data2 = json.loads(response2)
        # Se crea un archivo json en el directorio ./raw_data/ y se le cargan los datos
        #with open(kwargs["dag_path"]+'/raw_data/'+"data_"+str(date.year)+'-'+str(date.month)+'-'+str(date.day)+'-'+str(date.hour)+".json", "w") as json_file:
        #        json.dump(data["rawData"], json_file)
        #data_pd2 = pd.DataFrame(data2)
        #data_names = dict(data_pd2["name"])
        #pd_names = pd.DataFrame(data_names)
        list_paises = [i["name"]["common"] for i in data2]
        #filtered_data = data_pd[data_pd[data_pd["Country_Region"]].isin(list_paises)]
        filtered = data_pd[data_pd["Country_Region"].isin(list_paises)]
        print(filtered.to_json())
    else:
        print('An error has occured!')
except Exception as e:
    #logging.error(e)
    print(e)
#finally:
    #print("Check the data format")