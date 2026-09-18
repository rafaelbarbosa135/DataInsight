import streamlit as st
import pandas as pd
import numpy as np

st.title("DataInsight")

st.subheader(
    "Com o DataInsight, você consegue acessar as principais "
    "informações e avaliar a qualidade dos seus dados."
)

st.write("Envie um arquivo CSV ou XLSX para o início da análise.")

# Inserir o arquivo
arquivo_planilha = st.file_uploader(
    "Escolha o tipo de arquivo correspondente à sua planilha:",
    type=["csv", "xlsx"]
)

if arquivo_planilha is not None:

    try:

        # Identificar o tipo de arquivo e realizar a leitura
        if arquivo_planilha.name.endswith(".xlsx"):
            df = pd.read_excel(arquivo_planilha)

        elif arquivo_planilha.name.endswith(".csv"):
            df = pd.read_csv(
                arquivo_planilha,
                encoding="latin1"
            )

        # Verificar se a planilha está vazia
        if df.empty:
            st.warning(
                "A planilha inserida não possui dados para análise."
            )

        else:

            # Arquivo válido e com dados
            st.success(
                f"Arquivo '{arquivo_planilha.name}' carregado com sucesso!"
            )

            # Mostrar uma prévia da planilha
            st.write("Prévia dos dados:")
            st.dataframe(df.head())

            # Botão para mostrar/esconder a tabela
            if "mostrar_tabela" not in st.session_state:
                st.session_state.mostrar_tabela = False

            if st.button("Informações da sua planilha em forma de tabela"):
                st.session_state.mostrar_tabela = (
                    not st.session_state.mostrar_tabela
                )

            if st.session_state.mostrar_tabela:
                st.write("Sua planilha foi executada")
                st.dataframe(df)

    except Exception as erro:

        st.error(
            f"Não foi possível ler a planilha: {erro}"
        )