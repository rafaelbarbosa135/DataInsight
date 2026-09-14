import streamlit as st
import pandas as pd

st.title("DataInsight")
st.write("Envie um arquivo CSV ou XLSX para o início da análise.")

arquivo_planilha = st.file_uploader(
    "Escolha o tipo de arquivo correspondente à sua planilha:",
    type=["csv", "xlsx"]
)

if arquivo_planilha is not None:

    if arquivo_planilha.name.endswith(".csv"):
        dados = pd.read_csv(arquivo_planilha)

    elif arquivo_planilha.name.endswith(".xlsx"):
        dados = pd.read_excel(arquivo_planilha)

    st.success(
        f"Arquivo '{arquivo_planilha.name}' carregado com sucesso!"
    )

    st.write("Prévia dos dados:")
    st.dataframe(dados)