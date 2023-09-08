import streamlit as st
import pandas as pd
import io
import tempfile
from PIL import Image


about_text = """
## Sobre o CoordConverter

O CoordConverter é uma ferramenta simples para a conversão de coordenadas geográficas de grau, minuto e segundo para graus decimais. Ele é útil para transformar coordenadas em diferentes formatos para facilitar o uso em sistemas de informações geográficas (GIS), mapas e análises geoespaciais.

### Recursos Principais:

- Conversão de coordenadas de grau, minuto e segundo para graus decimais.
- Suporte para diversos formatos de arquivo, incluindo XLSX, XLS, CSV e TXT.
- Visualização dos pontos no mapa após a conversão.
- Exportação dos dados convertidos para download.

O CoordConverter é uma ferramenta prática para profissionais e entusiastas que lidam com dados geoespaciais e desejam simplificar o processo de conversão de coordenadas.

### Contato e Suporte:

Se você tiver alguma dúvida, comentários ou encontrar algum problema, não hesite em entrar em contato conosco pelo e-mail: anhambombe@gmail.com. Além disso, você pode obter suporte adicional na comunidade Streamlit: [Get help](https://streamlit.io/community).

Aproveite o uso do CoordConverter para simplificar suas tarefas de conversão de coordenadas geográficas!
"""


menu_items = {
    "About": about_text,
    "Report a bug": "mailto:anhambombe@gmail.com",  # Use o formato correto para um link de e-mail
    "Get help": "https://streamlit.io/community"  # Adicione uma entrada para a página "About" em português
}


st.set_page_config(
    page_title="CoordConverter",
    page_icon="❄",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=menu_items
    )




# Provide the file path to your image
file_path = "C:\\Users\\LENOVO\\Documents\\Eu\\WHO_2022\\DADOS\\PBI\\parceiros campanha.png"

# Open and read the image
image = Image.open("parceiros campanha.png")

# Create a Streamlit app
#st.title("Image Display Example")
st.image(image, caption=' ', use_column_width=True)



# Função para converter coordenadas de grau, minuto e segundo para graus decimais
def coordenadas_para_graus_decimais(graus, minutos, segundos, direcao):
    graus_decimais = graus + minutos / 60 + segundos / 3600
    if direcao in ['S', 'W']:
        graus_decimais = -graus_decimais
    return graus_decimais

# Função para ler e processar o arquivo
def processar_arquivo(arquivo, lat_graus_col, lat_min_col, lat_seg_col, lat_dir_col, lon_graus_col, lon_min_col, lon_seg_col, lon_dir_col):
    try:
        if arquivo.name.endswith(('.xlsx', '.xls', '.csv', '.txt')):
            if arquivo.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(arquivo)
            else:
                df = pd.read_csv(arquivo, sep=None, engine='python')

            st.write("Arquivo original:")
            st.write(df)

            # Aplicar a conversão de coordenadas para graus decimais para Latitude
            df['Latitude (Graus Decimais)'] = df.apply(lambda row: coordenadas_para_graus_decimais(
                row[lat_graus_col], row[lat_min_col], row[lat_seg_col], row[lat_dir_col]), axis=1)

            # Aplicar a conversão de coordenadas para graus decimais para Longitude
            df['Longitude (Graus Decimais)'] = df.apply(lambda row: coordenadas_para_graus_decimais(
                row[lon_graus_col], row[lon_min_col], row[lon_seg_col], row[lon_dir_col]), axis=1)

            st.write("Arquivo com coordenadas convertidas:")
            st.write(df)
            # Converter em texto
            df['Longitude (Graus Decimais)'] = df['Longitude (Graus Decimais)'].astype(str)
            df['Longitude (Graus Decimais)'] = df['Longitude (Graus Decimais)'].str.replace(",", ".")

            # Subistituir , por .
            df['Latitude (Graus Decimais)'] = df['Latitude (Graus Decimais)'].astype(str)
            df['Latitude (Graus Decimais)'] = df['Latitude (Graus Decimais)'].str.replace(",", ".")

            #converter para float
            df['Longitude (Graus Decimais)'] = df['Longitude (Graus Decimais)'].astype(float)
            df['Latitude (Graus Decimais)'] = df['Latitude (Graus Decimais)'].astype(float)


            # Salvar os dados em um arquivo temporário
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            df.to_excel(temp_file.name, index=False)
            # Ler o arquivo temporário e criar o botão de download
            with open(temp_file.name, "rb") as file:
                st.download_button("Baixar arquivo convertido", file.read(), key='xlsx_download', file_name="coordenadas_convertidas.xlsx")


            #### Fazer dos novos pontos
            st.map(latitude=df["Latitude (Graus Decimais)"], longitude=df["Longitude (Graus Decimais)"])

        else:
            st.error("Por favor, selecione um arquivo nos formatos xlsx, xls, csv ou txt.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {str(e)}")

# Configuração da aplicação Streamlit
st.title("Conversor de Coordenadas para Graus Decimais")

uploaded_file = st.file_uploader("Faça o upload de um arquivo (xlsx, xls, csv ou txt)", type=["xlsx", "xls", "csv", "txt"])

if uploaded_file:
    colunas_disponiveis = list(pd.read_excel(uploaded_file, nrows=1).columns) if uploaded_file.name.endswith(('.xlsx', '.xls')) else list(pd.read_csv(uploaded_file, nrows=1, sep=None, engine='python').columns)

    st.subheader("Selecione as colunas para Latitude:")
    lat_graus_col, lat_min_col, lat_seg_col, lat_dir_col = st.columns(4)
    lat_graus_col = lat_graus_col.selectbox("Graus:", colunas_disponiveis, key='lat_graus')
    lat_min_col = lat_min_col.selectbox("Minutos:", colunas_disponiveis, key='lat_min')
    lat_seg_col = lat_seg_col.selectbox("Segundos:", colunas_disponiveis, key='lat_seg')
    lat_dir_col = lat_dir_col.selectbox("Direção (N, S):", colunas_disponiveis, key='lat_dir')

    st.subheader("Selecione as colunas para Longitude:")
    lon_graus_col, lon_min_col, lon_seg_col, lon_dir_col = st.columns(4)
    lon_graus_col = lon_graus_col.selectbox("Graus:", colunas_disponiveis, key='lon_graus')
    lon_min_col = lon_min_col.selectbox("Minutos:", colunas_disponiveis, key='lon_min')
    lon_seg_col = lon_seg_col.selectbox("Segundos:", colunas_disponiveis, key='lon_seg')
    lon_dir_col = lon_dir_col.selectbox("Direção (E, W):", colunas_disponiveis, key='lon_dir')

    if st.button("Converter Coordenadas"):
        processar_arquivo(uploaded_file, lat_graus_col, lat_min_col, lat_seg_col, lat_dir_col, lon_graus_col, lon_min_col, lon_seg_col, lon_dir_col)


hide_st_style ="""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
<style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)


st.sidebar.title("Configurações")

# Botão de informação
if st.sidebar.button("ℹ️ Informação"):
    st.sidebar.write(about_text)

# Botão de ajuda

# Link de e-mail para obter ajuda
email = "anhambombee@gmail.com"
#st.markdown(f"❓ Para obter ajuda, envie um e-mail para [{email}](mailto:{email}) :information_source:")

if st.sidebar.button("❓ Ajuda"):
    st.sidebar.markdown(f"Para obter ajuda, envie um e-mail para [{email}](mailto:{email}) :information_source:")
