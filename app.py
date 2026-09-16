import streamlit as st
import pandas as pd

st.title("DataInsight")
st.subheader("Com o DataIsight você consegue ter acesso as principais informações, qualidades dos dados.")

st.write("Envie um arquivo CSV ou XLSX para o início da análise.")

#inserir o arquivo

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

    # Mostra uma prévia da planilha 

    st.write("Prévia dos dados:")
    st.dataframe(dados.head())

    # Botão para mostrar/esconder a tabela

    if "mostrar_tabela" not in st.session_state:
        st.session_state.mostrar_tabela = False 

    if st.button("Informações da sua planillha em forma de tabela"):
        st.session_state.mostrar_tabela = not st.session_state.mostrar_tabela 

    if st.session_state.mostrar_tabela:
        st.write("Sua planilha em forma de tabela foi executada")
        st.dataframe(dados)
