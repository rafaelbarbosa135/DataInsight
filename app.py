import streamlit as st
import pandas as pd

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


# Botão para mostrar/esconder a tabela
def mostrar_tabela(df):

    if "mostrar_tabela" not in st.session_state:
        st.session_state.mostrar_tabela = False

    if st.button("Verifique sua planilha completa"):
        st.session_state.mostrar_tabela = (
            not st.session_state.mostrar_tabela
        )

    if st.session_state.mostrar_tabela:
        st.write("Sua planilha foi executada")
        st.dataframe(df)

# Botão para mostrar/esconder os valores ausentes na tábela
def mostrar_dados_faltantes(df):

    if "mostrar_dados_faltantes" not in st.session_state:
        st.session_state.mostrar_dados_faltantes = False

    if st.button("Avaliação de dados ausentes na planilha"):
        st.session_state.mostrar_dados_faltantes = (
            not st.session_state.mostrar_dados_faltantes
        )

    if st.session_state.mostrar_dados_faltantes:
        st.write("Sua planilha foi executada")
        st.dataframe(df.isna().sum())


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

            st.success(
                f"Arquivo '{arquivo_planilha.name}' carregado com sucesso!"
            )

            st.write("Prévia dos dados:")
            st.dataframe(df.head())

            # CORREÇÃO: chamar as funções somente depois que df existe
            mostrar_tabela(df)
            mostrar_dados_faltantes(df)

    except Exception as erro:

        st.error(
            f"Não foi possível ler a planilha: {erro}"
        )