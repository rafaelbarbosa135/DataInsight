import streamlit as st
import pandas as pd
import plotly.express as px
import language_tool_python

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

# Cria o corretor ortográfico
@st.cache_resource
def criar_corretor():
    return language_tool_python.LanguageTool("pt-BR")


# Botão para correção ortográfica
def verificacao_ortografica(df):

    if "mostrar_correcao_ortografica" not in st.session_state:
        st.session_state.mostrar_correcao_ortografica = False

    if st.button("Verifique possíveis erros ortográficos"):
        st.session_state.mostrar_correcao_ortografica = (
            not st.session_state.mostrar_correcao_ortografica
        )

    if st.session_state.mostrar_correcao_ortografica:

        colunas_texto = df.select_dtypes(include="object").columns

        ferramenta = criar_corretor()

        resultados = []

        for coluna in colunas_texto:

            valores = df[coluna].dropna().unique()

            for valor in valores:

                texto = str(valor).strip()

                if not texto:
                    continue

                erros = ferramenta.check(texto)

                for erro in erros:

                    if erro.replacements:

                        resultados.append({
                            "Coluna": coluna,
                            "Valor encontrado": texto,
                            "Sugestão": erro.replacements[0],
                            "Tipo": erro.rule_issue_type
                        })

        if resultados:

            st.write("Possíveis erros encontrados:")

            df_erros = pd.DataFrame(resultados)

            st.dataframe(
                df_erros,
                use_container_width=True
            )

        else:

            st.success(
                "Nenhum possível erro de escrita foi encontrado."
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


# Botão para mostrar/esconder os valores ausentes na tabela
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

            mostrar_tabela(df)

            mostrar_dados_faltantes(df)

            verificacao_ortografica(df)

            # Cria um gráfico com base na planilha anexada
            st.subheader("Gráfico de Dispersão")

            colunas_numericas = (
                df.select_dtypes(include="number").columns
            )

            if len(colunas_numericas) >= 2:

                coluna_x = st.selectbox(
                    "Escolha a variável do eixo X:",
                    colunas_numericas
                )

                coluna_y = st.selectbox(
                    "Escolha a variável do eixo Y:",
                    colunas_numericas
                )

                fig = px.scatter(
                    df,
                    x=coluna_x,
                    y=coluna_y,
                    title=f"{coluna_y} em relação a {coluna_x}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.warning(
                    "A planilha precisa possuir pelo menos duas "
                    "colunas numéricas para criar um gráfico "
                    "de dispersão."
                )

    except Exception as erro:

        st.error(
            f"Não foi possível ler a planilha: {erro}"
        )
