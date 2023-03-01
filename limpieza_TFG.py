import pandas as pd
import numpy as np
import sys


nombres_donantes = {
    'D001': 'Vedruna',
    'D002': 'Colegio Mayor Aquinas',
    'D003': 'Funway Academic Resort',
    'D004': 'Estamos bien',
    'D005': 'Bonjour',
    'D006': 'Fruteria Valencia',
    'D008': 'Eñe + que una letra',
    'D009': 'LomiRock',
    'D011': 'Q Pastelitos',
    'D012': 'Frutería Las Gemelas',
    'D013': 'El Cebón',
    'D014': 'Fruteria El Moreno',
    'D015': 'CHIPA',
    'D016': 'Tercer Tiempo Bar',
    'D017': 'Fruterias Ignacio',
    'D018': 'Bonjour',
    'D019': 'CM Loyola',
    'D021': 'Zara frutas y verdura',
    'D022': 'Casa Ramona',
    'D023': 'Fruterias Andrés',
    'D024': 'Shurma Huerta',
    'D025': 'Hoy es Mañana',
    'D026': 'Pastelería Ludavi',
    'D030': 'Roscaffé',
    'D035': 'FRUTERIA TETUAN',
    'D034': 'FRUTERIA MARIANO',
    'D033': 'FUNDACIÓN ESCLEROSIS MULTIPLE',
    'D031': 'AMOR AL PLATO',
    'D028': 'M.BENAVENTE',
    'D027': 'COLEGIO MAYOR ALCALA',
    'OTRO': 'Otros'
}


def decimal_converter(value):
    try:
        return float(str(value).replace(',', '.'))
    except ValueError:
        return value

    
def crear_columnas_kg_rac(data,tipo_alimento):

    data["Cantidad"] = pd.to_numeric(data["Cantidad"], downcast="float")

    data['Kilos rescatados'] = np.where((data[tipo_alimento].str.lower() == 'comida preparada') & (data['Tipo medida'] == 'Raciones'),
                                        data['Cantidad'] * 0.2,
                                        np.where((data[tipo_alimento].str.lower() == 'alimentos frescos') & (data['Tipo medida']=='Raciones'),
                                                 data['Cantidad'] * 1.5,
                                                 np.where((data[tipo_alimento].str.lower() == 'pan') & (data['Tipo medida']=='Raciones'),
                                                          data['Cantidad'] * 0.2, data['Cantidad'])))

    data['Raciones rescatadas'] = np.where((data[tipo_alimento].str.lower() == 'comida preparada') & (data['Tipo medida']=='Kg'),
                                           data['Cantidad'] * 4,
                                           np.where((data[tipo_alimento].str.lower() == 'alimentos frescos') & (data['Tipo medida']=='Kg'),
                                                    data['Cantidad'] * 3,
                                                    np.where((data[tipo_alimento].str.lower() == 'pan') & (data['Tipo medida']=='Kg'),
                                                             data['Cantidad'] * 2, data['Cantidad'])))

    return data


def anadir_columna_nombres(data,fecha):

    donantes = data['ID Donante'].unique()
    data['Nombres'] = data['ID Donante']
    for donante in donantes:
        data['Nombres'] = data['Nombres'].replace([donante], nombres_donantes[donante])
    print("Fechas en el fichero por donantes:")
    print(data.groupby('Nombres')[fecha].agg(['min', 'max']).rename(columns={'min': 'first', 'max': 'last'}))
    
    return data


def leer_archivo_excel(nombre_archivo, tipo_historico):

    nombre_archivo = nombre_archivo
    if(tipo_historico == 'entradas'):
        nombre_hoja = 'Entrada de alimentos'
        fecha = 'Fecha de entrada'
        nombre_csv = 'Entradas'
        tipo_alimento = 'Tipo de alimento'
    elif(tipo_historico == 'salidas'):
        nombre_hoja = 'Salida de alimentos'
        fecha = 'Fecha '
        nombre_csv = 'Salidas'
        tipo_alimento = 'Tipo de comida'

    df = pd.df = pd.read_excel(nombre_archivo, sheet_name=nombre_hoja,
                               parse_dates=[fecha], dtype=str, converters={"Cantidad":decimal_converter})

    df['ID Donante'] = df['ID Donante'].astype(str)
    df.drop(df[df['ID Donante'] == 'D007'].index, inplace=True)
    df.drop(df[df['ID Donante'] == 'D010'].index, inplace=True)
    df['ID Donante'].replace('D005','D018')
    df['ID Donante'] = df['ID Donante'].apply(lambda x: x.upper())
    
    df[fecha] = pd.to_datetime(df[fecha])
    
    df.set_index('ID Alimento', inplace=True)
    
    df = df.replace('Kilos', 'Kg')
    
 
    #       Error Mencionado en notion
#     df['Cantidad'] = df['Cantidad'].str.extract('(\d+\.?\d{0,2})', expand=False)
#     df['Cantidad'] = df['Cantidad'].apply(pd.to_numeric)
    df = df.dropna()
#     df['Cantidad'] = np.where(df['Cantidad'] > 100, df['Cantidad'] * 0.001, df['Cantidad'])


    df[fecha] = df[fecha].dt.strftime('%m-%d-%Y')
    fecha_minima = df[fecha].iloc[0]
    fecha_maxima = df[fecha].iloc[-1]
    

    
    
    print(df)
#     df.to_csv("test_datos")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        df = leer_archivo_excel(sys.argv[1],sys.argv[2])
    else:
        print("No arguments")