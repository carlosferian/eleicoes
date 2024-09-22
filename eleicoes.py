import streamlit as st
import webbrowser

# Título da página
st.title("Projeto de Divulgação de Dados Históricos de Eleições no Paraná")

# Descrição do projeto
st.markdown("""
## Bem-vindo ao Projeto de Divulgação de Dados Históricos de Eleições no Paraná

Este projeto tem como objetivo disponibilizar e facilitar o acesso a dados históricos das eleições realizadas no estado do Paraná. Aqui você poderá encontrar informações sobre eleições passadas, resultados, estatísticas e análises que contribuem para a compreensão do processo eleitoral no estado.

**Observação:** Este não é um projeto oficial. Os dados apresentados podem apresentar ligeiras divergências em relação aos resultados computados oficialmente pela Justiça Eleitoral. Trata-se de uma atividade em fase de testes e de iniciativa particular do desenvolvedor.
""")

# Botão para acessar o site oficial do TSE
btn = st.button("Acesse os dados no Site Oficial do TSE")
if btn:
    webbrowser.open_new_tab("https://www.tse.jus.br/eleicoes/estatisticas")
