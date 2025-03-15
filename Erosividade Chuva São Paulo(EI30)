import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Carregar a planilha
dados = 'C:/eups_artigo/3_erosividade/preciptacao_.xlsx'
df = pd.read_excel(dados)



# Calcula preciptação média anual de cada estação
preciptaçao_media_anual = df.groupby('codigo')['preciptacao_mensao_total'].mean().reset_index()
preciptaçao_anual.rename(columns={'preciptacao_mensao_total': 'preciptaçao_media_anual'}, inplace=True)

# Calcular a precipitação média mensal de cada estação
precipitacao_media_mensal = df.groupby(['codigo', 'mes'])['preciptacao_mensao_total'].mean().reset_index()
precipitacao_media_mensal.rename(columns={'preciptacao_mensao_total': 'precipitacao_media_mensal'}, inplace=True)

# Juntar os DataFrames pelo 'codigo' para combinar as informações
merged_df = precipitacao_media_mensal.merge(precipitacao_media_anual, on='codigo')

# Calcular o valor de EI30 para cada estação
merged_df['EI30'] = 111.6 * (merged_df['precipitacao_media_mensal'] / merged_df['preciptaçao_media_anual']) ** 0.714

print("Valores de EI30 para cada estação:")
print(merged_df[['codigo', 'mes', 'EI30']])

# Calcular a somatória do EI30 por estação
soma_EI30 = merged_df.groupby('codigo')['EI30'].sum().reset_index()
soma_EI30.rename(columns={'EI30': 'soma_EI30'}, inplace=True)

print("Somatória do EI30 por estação:")
print(soma_EI30)

# Adicionar a somatória do EI30 ao DataFrame combinado
final_df = merged_df.merge(soma_EI30, on='codigo', how='left')

# Mesclar com os dados originais
final_df = df.merge(final_df, on=['codigo', 'mes'], how='left')

# Função para salvar o DataFrame final em um arquivo xlsx com o caminho especificado
def salvar_arquivo(df, caminho):
    df.to_excel(caminho, index=False)

# Especifique o caminho de saída aqui
caminho_saida = 'C:/eups_artigo/3_erosividade/editadodados_processados.xlsx'
salvar_arquivo(final_df, caminho_saida)

print(f"Nova tabela com todos os dados salva como '{caminho_saida}'")


# Criar um GeoDataFrame a partir dos dados filtrados
geometry = [Point(xy) for xy in zip(df['longitude'], df['Latitude'])]  # Certifique-se de usar os nomes corretos das colunas
geo_df = gpd.GeoDataFrame(final_df, geometry=geometry)

# Salvar o GeoDataFrame como um shapefile
caminho_saida_shp = 'caminho_para_salvar/dados_estacao.shp'
geo_df.to_file(caminho_saida_shp, driver='ESRI Shapefile')

print(f"Shapefile criado e salvo em '{caminho_saida_shp}'")
