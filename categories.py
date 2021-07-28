import pandas as pd
from sys import argv
script, csv = argv

dataframe = pd.read_csv(csv)

categories = {  0:"NEWS DALL'EUROPA",
                1:'ISTRUZIONE, SCIENZA, RICERCA E INNOVAZIONE',
                2:'ECONOMIA',
                3:'AZIONI PER IL CLIMA',
                4:'AMBIENTE',
                5:'AGRICOLTURA, CIBO E SVILUPPO RURALE',
                6:'ENERGIA',
                7:'MOBILITA  E TRASPORTI',
                8:'EUROSTAT',
                9:'LAVORO, INCLUSIONE E AFFARI SOCIALI',
                10:'POLITICHE REGIONALI',
                11:'GIUSTIZIA E CONSUMATORI',
                12:'POLITICHE MIGRATORIE',
                13:'MIGRAZIONI E AFFARI INTERNI',
                14:'AFFARI MARITTIMI',
                15:'SALUTE E SICUREZZA ALIMENTARE',
                16:'RACCOLTA E GESTIONE DEI RIFIUTI',
                17:'FORMAZIONE',
                18:'COMMERCIO',
                19:'POSSIBILITA DI FINANZIAMENTO',
                20:'STRUMENTI FINANZIARI',
                21:'BANDI',
                22:'WEBINAR ED EVENTI ONLINE',
                23:'SAVE THE DATE'}

dataframe['section'] = dataframe['section'].astype(int)
dataframe['section_id'] = dataframe['section']
dataframe['section'] = dataframe['section'].map(categories)

dataframe = dataframe.sort_values(by=['section_id', 'title'])

dataframe.to_csv(csv, index = False)
