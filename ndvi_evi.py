!pip install rasterio
import rasterio
import numpy as np
import os

#Acessar google drive
from google.colab import drive
drive.mount('/content/gdrive')

# Caminho do arquivo TIF
imagem = '/content/gdrive/MyDrive/estudo_geo_d/planet_img/mesclado.tif'

try:
    # Abrindo o arquivo TIF
    with rasterio.open(imagem) as img:
        # Mostrando informações básicas da imagem, e fazer algumas verificações 
        print("Imagem carregada com sucesso!")
        print(f"Dimensões: {img.width} x {img.height}")
        print(f"Número de bandas: {img.count}")
        print(f"Tipo de dado: {img.dtypes[0]}")
        print(f"Sistema de coordenadas: {img.crs}")
        print(f"Extensão espacial: {img.bounds}")
except Exception as e:
    print("Erro ao carregar a imagem:", e)


# Caminhos para salvar os arquivos de saída
caminho_saida_ndvi = '/content/gdrive/MyDrive/estudo_geo_d/saida/ndvi.tif'
caminho_saida_evi = '/content/gdrive/MyDrive/estudo_geo_d/saida/evi.tif'

try:
    # Garantir que os diretórios de saída existam
    os.makedirs(os.path.dirname(caminho_saida_ndvi), exist_ok=True)
    os.makedirs(os.path.dirname(caminho_saida_evi), exist_ok=True)

    # Abrindo a imagem de entrada
    with rasterio.open(imagem) as src:
        # Lendo as bandas necessárias
        red = src.read(1).astype(float)   # Banda Vermelha
        nir = src.read(2).astype(float)  # Banda Infravermelho Próximo (NIR)
        blue = src.read(3).astype(float) # Banda Azul (necessária para o EVI)

        # Calculando o NDVI
        ndvi = (nir - red) / (nir + red)
        ndvi = np.clip(ndvi, -1, 1)  # Garantindo que os valores fiquem dentro do intervalo [-1, 1]

        # Calculando o EVI
        G = 2.5
        C1 = 6
        C2 = 7.5
        L = 1
        evi = G * ((nir - red) / (nir + C1 * red - C2 * blue + L))
        evi = np.clip(evi, -1, 1)  # Garantindo que os valores fiquem dentro do intervalo [-1, 1]

        # Salvando o NDVI como um novo arquivo GeoTIFF
        perfil = src.profile  # Mantendo o perfil da imagem original
        perfil.update(dtype=rasterio.float32, count=1)  # Atualizando o tipo e número de bandas

        with rasterio.open(caminho_saida_ndvi, 'w', **perfil) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)

        # Salvando o EVI como um novo arquivo GeoTIFF
        with rasterio.open(caminho_saida_evi, 'w', **perfil) as dst:
            dst.write(evi.astype(rasterio.float32), 1)

        print(f"NDVI salvo em: {caminho_saida_ndvi}")
        print(f"EVI salvo em: {caminho_saida_evi}")

except Exception as e:
    print("Erro ao processar a imagem:", e)
