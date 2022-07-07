import pandas as pd



def hecto():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\01.11.csv', encoding='latin-1', sep=";")
    db = db[
        ['Código', 'Descrição','Fator Hecto']
    ]
    db.rename(columns={'Código': 'Produto'}, inplace=True)
    db.rename(columns={'Fator Hecto':'FatorHecto'}, inplace= True)
    db['Produto'] = db.Produto.astype('str')
    db['FatorHecto'] = db.FatorHecto.astype('str')
    db['FatorHecto'] = db['FatorHecto'].str.replace(',', '.', regex=True)
    db['FatorHecto'] = db.FatorHecto.astype(float)

    return db


def dbDiaB():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\03.01.36.04.csv', encoding='latin-1', sep=";")
    db = db[
        ['Pedido', 'Data Pedido', 'Operacao', 'Cod. PDV', 'Nome PDV', 'Status Pedido', 'Produto',
         'Quantidade', 'Preco S/ ADF', 'Ocorrencia', 'Origem Pedido', 'Idade', 'Fora de Rota']]
    db.rename(columns={'Fora de Rota': 'FR'}, inplace=True)
    db.rename(columns={'Cod. PDV': 'PDV'}, inplace=True)
    db['Produto'] = db.Produto.astype('str')
    db['Idade'] = db.Idade.astype('str')
    db['Idade'] = db['Idade'].str.replace(" ", "0", regex=True)
    db['Preco S/ ADF'] = db['Preco S/ ADF'].str.replace(",", ".", regex=True)
    db['Idade'] = db.Idade.astype(float).astype(int)
    #db['Preco S/ ADF'] = db['Preco S/ ADF'].astype(float)
    op = [1, 2]
    db = db[db.Operacao.isin(op)]
    db = pd.merge(db, hecto(), how='left', on='Produto')
    db = db.assign(Volume=db.Quantidade * db.FatorHecto)
    db = db.drop(['FatorHecto'], axis=1)
    db = db.round(1)
    db = pd.merge(db, PDVs(), how='left', on='PDV')
    db = db.drop(['NomeFantasia'], axis=1)
    db.rename(columns={'Vde': 'Setor'}, inplace=True)
    db = pd.merge(db, listaVDE(), how='left', on='Setor')
    db['Setor'] = db.Setor.astype('str')
    db = db.loc[db['Status Pedido'].str.contains('Exc', na=False) == False]
    
    #db['Preco S/ ADF'] = db['Preco S/ ADF'].round(2)

    return db

def listaVDE():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\01.02.46.csv', encoding='latin-1', sep=";")
    db = db[
        ['Cod', 'Nome', 'Supervisor', 'Nome Supervisor', 'Status', 'Funcao']]
    db.rename(columns={'Cod': 'Setor'}, inplace=True)
    db = db.loc[db['Setor'] > 200, :]
    db = db.loc[db['Setor'] < 704, :]
    db = db.loc[db['Funcao'] == 1, :]
    db = db.loc[db['Status'] == "A", :]
    db = db.loc[db['Setor'] != 601, :]
    db = db.loc[db['Setor'] != 606, :]
    db = db[
        ['Setor', 'Nome', 'Supervisor', 'Nome Supervisor']]

    return db

def PDVs():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\01.20.12-total.csv', encoding='latin-1', sep=";")
    db = db[
        ['CodCliente', 'NomeFantasia', 'Vde','Municipio', 'Lat', 'Long','ProxVisitaVde']
    ]
    db.rename(columns={'CodCliente': 'PDV'}, inplace=True)

    return db

def grupoProd():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\grupoProdResumo.csv', encoding='latin-1', sep=";")
    db = db.fillna(0)

    for i in db.columns:

        db[i] = db[f'{i}'].astype(int)
        db[i] = db[f'{i}'].astype(str)

    return db

def volumeSetor(data):
    df = data
    lista = []
    for Setor in df['Setor'].unique():
        lista.append(df[df['Setor'] == Setor]['Volume'].sum()) # somando todos os focos de queimadas para cada estado
    db = pd.DataFrame(columns=["Setor"])
    db["Setor"] = df['Setor'].unique()
    db["Volume"] = lista
    db["Volume"] = db['Volume'].round(1)

    return db

def diasUteis():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\DiasUteis.csv', encoding='latin-1', sep=";", header=None)

    db = [int(db[1][0]),int(db[1][1])]
    return db

def metas():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\05.10.csv', encoding='latin-1', sep=";", dtype='str')
    db['Objetivo'] = db['Objetivo'].str.replace('.', "", regex=True)
    db['Objetivo'] = db.Objetivo.astype('int')

    db = db[['Setor     ','Codigo','Objetivo']]
    db.rename(columns={'Setor     ': 'Setor'}, inplace=True)
    db['Setor'] = db.Setor.astype('int')
    db.rename(columns={'Codigo': 'Produto'}, inplace=True)
    db['Produto'] = db.Produto.astype('int')
    db['Produto'] = db.Produto.astype('str')
    db = pd.merge(db, hecto(), how='left', on='Produto')
    db = db.assign(Meta=db.Objetivo * db.FatorHecto)

    db = db.drop(['Objetivo','Descrição','FatorHecto'], axis=1)
    db = db.loc[db['Setor'] > 200, :]
    db = db.loc[db['Setor'] < 704, :]
    db = db.loc[db['Setor'] != 601, :]
    db = db.loc[db['Setor'] != 606, :]
    db['Setor'] = db.Setor.astype('str')
    return db
metas()
def volumeMes():
    db = pd.read_csv(r'\\192.168.0.252\dados\TI\Robo\DadosAv\03.02.37.csv', encoding='latin-1', sep=";", dtype='str')

    db['Qtde'] = db['Qtde'].str.replace('.', "", regex=True)

    db['Cliente'] = db['Cliente'].astype(int)
    db['Qtde'] = db['Qtde'].astype(int)
    db['Produto'] = db.Produto.astype('str')

    db['Operacao .'] = db['Operacao .'].astype(int)
    db.rename(columns={'Operacao .': 'Operacao'}, inplace=True)
    db = db[['Operacao', 'Status', 'Cliente', 'Produto', 'Qtde', 'Total']]
    hectos = hecto()
    db['Produto'] = db['Produto'].astype(int)
    hectos['Produto'] = hectos['Produto'].astype(int)
    db = pd.merge(db,hectos,how='left',on='Produto')
    db = db.assign(Volume=db.Qtde * db.FatorHecto)
    db = db.drop(['Descrição'], axis=1)
    stat = ['A', 'E']
    op = [1, 2]
    db = db[db.Status.isin(stat)]
    db = db[db.Operacao.isin(op)]
    db['Produto'] = db.Produto.astype('str')
    return db

def volumePDVdia(data):
    df = data
    grupo = grupoProd()
    ambev = []
    cerv = []
    nab = []
    rgb = []
    heco = []
    pm = []
    for PDV in df['PDV'].unique():
        ambev.append(df[df['PDV'] == PDV]['Volume'].sum())  # Ambev
        cerv.append(df[(df.Produto.isin(list(grupo['Cerv TT'].unique()))) & (df['PDV'] == PDV)].Volume.sum())  # somando todos os focos de queimadas para cada estado
        nab.append(df[(df.Produto.isin(list(grupo['NAB'].unique()))) & (df['PDV'] == PDV)].Volume.sum())  # somando todos os focos de queimadas para cada estado
        rgb.append(df[(df.Produto.isin(list(grupo['RGB'].unique()))) & (df['PDV'] == PDV)].Volume.sum())  # somando todos os focos de queimadas para cada estado
        heco.append(df[(df.Produto.isin(list(grupo['HECO'].unique()))) & (df['PDV'] == PDV)].Volume.sum())  # somando todos os focos de queimadas para cada estado
        pm.append(df[(df.Produto.isin(list(grupo['Puro Malte'].unique()))) & (df['PDV'] == PDV)].Volume.sum())  # somando todos os focos de queimadas para cada estado

    db = pd.DataFrame(columns=["PDV"])
    db["PDV"] = df['PDV'].unique()
    db["Ambev"] = ambev
    db['Cerveja'] = cerv
    db['NAB'] = nab
    db['RGB'] = rgb
    db['HECO'] = heco
    db['PuroMalte'] = pm
    db = db.round(1)
    db = pd.merge(db,PDVs(),how='left', on='PDV')
    db = db.drop(['Vde', 'Municipio', 'Lat', 'Long', 'ProxVisitaVde'], axis=1)
    db = db[['PDV','NomeFantasia', 'Ambev', 'Cerveja', 'NAB', 'RGB', 'HECO', 'PuroMalte']]

    #print(db[db.Cerveja == db.Cerveja.max()])

    return db

def pedidosDia(buffer="T", falta="T"):
    pedidos = dbDiaB()
    if buffer == "S":
        pedidos = pedidos.loc[pedidos['Idade'] != 0, :]


    elif buffer == "N":
        pedidos = pedidos.loc[pedidos['Idade'] == 0, :]

    # Falta
    if falta == "S":
        pedidos = pedidos[pedidos.Ocorrencia.str.contains("Falta", regex=False)]


    elif falta == "N":
        pedidos = pedidos[pedidos.Ocorrencia.str.contains("Falta", regex=False) == False]

    return pedidos