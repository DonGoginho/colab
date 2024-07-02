
from IPython.display import Markdown as md
import pandas as pd
import requests
import io
import sys
import warnings


def load_data(status, data_source, package_name, dataset_name, **kwargs):
    """
    Diese Funktion importiert die gewünschten Daten je nach Status (Int/Prod) und Speicherort (Dropzone/Web) in Pandas ein.

    Parameter:
    - status (str): sind die Daten auf Integ ('int') oder auf Prod ('prod') zu beziehen? 
    - data_source (str): sind die Daten im Internet ('web'), LOSD ('ld') oder auf den Dropzones/Fileverzeichnis ('dropzone') zu beziehen?
    - package_name (str): Name des Packages. Dies entspricht dem Slug in der URL und auch dem Verzeichnisnamen auf der Dropzone. Z.B. 'bfs_bev_bildungsstand_seit1970_OD1002'
    - dataset_name (str): Name des Datensatzes (in CKAN der Ressource). z.B. "bev324od3242.csv"

    Optionale Parameter:
    - ckan_integ_url (str):  Pfad zur INT-Umgebung von CKAN. Default: 'https://data.integ.stadt-zuerich.ch/dataset/'
    - ckan_integ_harvester_name (str):  Name des INT-Harvesters, der in den Slug eingefügt wird. Default: 'INT_DWH'
    - ckan_prod_url (str):  Pfad zur PROD-Umgebung von CKAN. Default: 'https://data.stadt-zuerich.ch/dataset/'  
    - dropzone_path_integ (str):  Pfad zur INT-Dropzone. Default: r"\\szh\ssz\applikationen\OGD_Dropzone\INT_DWH"
    - dropzone_path_prod (str): Pfad zur PROD-Dropzone. Default: r"\\szh\ssz\applikationen\OGD_Dropzone\DWH"
    - ld_integ_url (str):  Pfad zur INT-LD. Default: 'https://ld.integ.stadt-zuerich.ch/statistics/view/'
    - ld_prod_url (str):  Pfad zu PROD-LD. Default: 'https://ld.stadt-zuerich.ch/statistics/view/'

    - file_format (str): Welches Fileformat wird eingelesen? Ist eigentlich sowieso immer ein CSV, aber für die Zusammensetzung der Downloadpfade hilft es so.
    - datums_attr (str): Weches ist oder sind die Datumsfelder die konvertiert werden sollen. Default:  ['StichtagDatJahr']
    - encoding (str): Welches Encoding enthalten die Import-Daten. Default: 'encoding', 'utf-8'
    - separator (str): Welche Trennzeichen sind im Import-Datensatz vorhanden. Default: 'separator', ','
    - na_values (liste): Welche Zeichen sollen NaN interpretiert werden?

    Rückgabe:
    - chart (alt.Chart): Das erstellte interaktive Diagramm.

    """
    try:
        ckan_integ_url = kwargs.get('ckan_integ_url', 'https://data.integ.stadt-zuerich.ch/dataset/')
        ckan_prod_url = kwargs.get('ckan_prod_url', 'https://data.stadt-zuerich.ch/dataset/')

        ckan_integ_harvester_name = kwargs.get('ckan_integ_harvster_name', 'INT_DWH') 

        dropzone_path_integ = kwargs.get('dropzone_path_integ',r"\\szh\ssz\applikationen\OGD_Dropzone\INT_DWH")
        dropzone_path_prod = kwargs.get('dropzone_path_prod',r"\\szh\ssz\applikationen\OGD_Dropzone\DWH")

        ld_integ_url = kwargs.get('ld_integ_url','https://ld.integ.stadt-zuerich.ch/statistics/view/')     
        ld_prod_url = kwargs.get('ld_prod_url', 'https://ld.stadt-zuerich.ch/statistics/view/')

        file_format  = kwargs.get('file_format', '.csv')

        datums_attr = kwargs.get('datums_attr', ['StichtagDatJahr'])
        encoding = kwargs.get('encoding', 'utf-8-sig')
        separator = kwargs.get('separator', ',')
        na_values = kwargs.get('na_values', ['','.','...','NA','NULL'])

    
        #create filepath
        # Filepath
        if status == "prod":
            if data_source == "dropzone":
                fp = dropzone_path_prod+"\\"+ package_name +"\\"+dataset_name+file_format
                print("fp lautet:"+fp)
            elif data_source == "ld":
                fp = ld_prod_url+package_name.upper()+'/observation?format=csv'
                print("fp lautet:"+fp)
                display(md(" **Überprüfe die Metadaten:**"))
                display(md(" **Dataset auf PROD-Datakatalog:** Link {} ".format(ckan_prod_url+package_name.lower())))
                display(md(" **View auf PROD-LD:** Link {} ".format(ld_prod_url+package_name.upper())))
                display(md(" **Dataset auf INTEG-Datakatalog:** Link {} ".format(ckan_integ_url+package_name.lower())))
                display(md(" **View auf INTEG-LD:** Link {} ".format(ld_integ_url+package_name.upper())))

            else:
                #fp = ckan_prod_url+package_name.lower()+'/download/'+dataset_name+file_format
                fp = ckan_prod_url+package_name.lower()+'/download/'+dataset_name.upper()+file_format
                print("fp lautet:"+fp)
                display(md(" **Überprüfe die Metadaten:**"))
                display(md(" **Dataset auf PROD-Datakatalog:** Link {} ".format(ckan_prod_url+package_name.lower())))
                display(md(" **Dataset auf INTEG-Datakatalog:** Link {} ".format(ckan_integ_url+package_name.lower())))

        else:
            if data_source == "dropzone":
                fp = dropzone_path_integ+"\\"+ package_name +"\\"+dataset_name+file_format
                print("fp lautet:"+fp)

            elif data_source == "ld":
                fp = ld_integ_url+package_name.upper()+'/observation?format=csv'
                print("fp lautet:"+fp)
                display(md(" **Überprüfe die Metadaten:**"))
                display(md(" **Dataset auf INTEG-Datakatalog:** Link {} ".format(ckan_integ_url+package_name.lower())))
                display(md(" **View auf INTEG-LD:** Link {} ".format(ld_integ_url+package_name.upper())))

            else:
                fp = ckan_integ_url+ckan_integ_harvester_name.lower()+'_'+package_name+'/download/'+dataset_name.upper()+file_format
                print("fp lautet:"+fp)
                display(md(" **Überprüfe die Metadaten:**"))
                display(md(" **Dataset auf INTEG-Datakatalog:** Link {} ".format(ckan_integ_url+ckan_integ_harvester_name.lower()+'_'+package_name.lower())))                
                display(md(" **Dataset auf PROD-Datakatalog:** Link {} ".format(ckan_prod_url+package_name.lower())))


        #import dataset
        if data_source == "dropzone":
            data2betested = pd.read_csv(
                fp
                , sep=separator
                , na_values = na_values
                , parse_dates= datums_attr
                , low_memory=False
            )
            print("data_source: dropzone")
        else:
            r = requests.get(fp, verify=False)  
            r.encoding = encoding
            data2betested = pd.read_csv(
                io.StringIO(r.text)
                , sep=separator
                , na_values = na_values                
                , parse_dates= datums_attr
                , low_memory=False)
            print("data_source: web")
               

        return data2betested



    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr) 