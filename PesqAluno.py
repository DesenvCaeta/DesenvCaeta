#Gera informações sobre os alunos
import streamlit as st
import pandas as pd

#C:\Users\prcral\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe -m streamlit run C:\Users\prcral\Documents\TESTEPYTHON\PesqAluno.py

st.set_page_config(page_title="PPE – Pesquisa de Alunos", layout="wide")

# Carrega o DataFrame a partir do arquivo 'VisaoFull.xlsx'
@st.cache_data

def load_data():
    df_alunos = pd.read_csv('DF_ALUNOS.csv')
    df_familias = pd.read_csv('DF_FAMILIAS.csv')
    df_dadosbasicos = pd.read_csv('DF_DADOSBASICOS.csv')
    df_resultados = pd.read_csv('DF_RESULTADOS.csv')
    df_beneficios = pd.read_csv('DF_BENEFICIOS.csv')
    df_contas =  pd.read_csv('DF_CONTAS.csv')
    
    return df_alunos, df_familias, df_dadosbasicos, df_resultados, df_beneficios, df_contas

df_alunos, df_familias, df_dadosbasicos, df_resultados, df_beneficios, df_contas = load_data()

# Sidebar
st.sidebar.title("Pesquisar Aluno")
st.sidebar.write("")
# *************************************************************
st.sidebar.text("Última atualização: 27/02/2025")
# *************************************************************
st.sidebar.text("")
#st.sidebar.text("Digite o nome desejado e quando\nencontrado clique no mesmo")
aluno_filtro  = st.sidebar.selectbox("Digite o nome desejado e quando\nencontrado clique no mesmo", 
       df_alunos["Aluno"])
st.sidebar.text("Na tabela ao lado, encontrado\no aluno, digite aqui o código\ndo mesmo e pressione ENTER")
st.sidebar.text("Dados detalhados do aluno serão\napresentados nas outras abas")
idt_elegivel  = st.sidebar.number_input('Código do aluno no PPE', min_value=1, value=1)

# Filtrar df_pesquisa pelo aluno selecionado no sidebar
if aluno_filtro:
    df_familias = df_familias[df_familias["Aluno"].str.contains(aluno_filtro, case=False)]

#Abas
tab1,tab2,tab3,tab4,tab5 = st.tabs(["Pesquisa","Dados Pessoais","Resultados","Benefícios","Conta Poupança" ])

with tab1:
    # Aba "Pesquisa"
    # Apresentar dataframe na aba Pesquisa
    st.dataframe(df_familias[["Cód.", "Aluno", "Nascimento", "Mae"]].reset_index(drop=True),
                height=200, use_container_width=True, hide_index=True,
                column_config={"Cód.": st.column_config.NumberColumn(format="%.0f")})

with tab2:
#Aba "Dados Pessoais"
#Realizar as instuçôes a seguir apenas se idt_elegivel existir em df_dadosbasicos
    if idt_elegivel in df_dadosbasicos["Cód."].to_list():
        dados_pessoais = df_dadosbasicos[df_dadosbasicos["Cód."] == idt_elegivel].iloc[0]

        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")
        st.text("Nascimento : " + dados_pessoais["Nascimento"])
        st.text("Mãe: " + dados_pessoais["Mae"])
        st.text("Pai: " + dados_pessoais["Pai"])

        if isinstance(dados_pessoais["Email informado"], str) and dados_pessoais["Email informado"].strip():
            st.write("Email informado: " + dados_pessoais["Email informado"])
        else:
            st.write("Email informado: não informado")

        st.write("Email CadUNICO: " + dados_pessoais["Email CadUNICO"])

        col1, col2 = st.columns(2)
        with col1:
            st.text("Sexo: " + dados_pessoais["Sexo"])

            # Dividir a string pelo ponto
            partes = str(dados_pessoais["Tel.Informado1"])
            partes = partes.split(".")
            primeira_parte = partes[0]
            #Verificar se primeira_parte é nulo
            if primeira_parte == 'nan':
                st.text("Tel.Informado1: Não informado")     
            else:
                st.text("Tel.Informado1: " + primeira_parte)
        
            # Dividir a string pelo ponto
            partes = str(dados_pessoais["CPF informado"])
            partes = partes.split(".")
            primeira_parte = partes[0]
            if primeira_parte == 'nan':
                st.text("CPF Informado: Não informado")     
            else:
                st.text("CPF Informado: " + primeira_parte)

            st.text("Bairro: " + str(dados_pessoais["Bairro"]))
            st.text("CEP: " + str(dados_pessoais["CEP"]))            
    else:
        st.header("Aluno não encontrado")

with tab3:
    #Aba Resultados
    #Realizar as instruçôes a seguir apenas se idt_elegivel existir em df_dadospessoais
    if idt_elegivel in df_dadosbasicos["Cód."].to_list():
        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")

        #Apresentar dataframe que mostre resultados
        df_results = df_resultados[df_resultados["Cód."] == idt_elegivel][["Ano Letivo", "Serie", 
                                                   "Andamento adesao", "Situacao", 
                                                   "Matricula", "Escola"]]
        df_results.sort_values(by="Ano Letivo", inplace=True)
        st.dataframe(df_results, use_container_width=True, hide_index=True,
                 column_config={"Ano Letivo": st.column_config.NumberColumn(format="%.0f")})
    else:
        st.header("Aluno não encontrado")

# Aba Benefícios
with tab4:
    # Realizar as instruções a seguir apenas se idt_elegivel existir em df_beneficios
    if idt_elegivel in df_dadosbasicos["Cód."].to_list():
        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")

        # Apresentar dataframe que mostre benefícios
        df_beneficio = df_beneficios[df_beneficios["Cód."] == idt_elegivel][["Ano Letivo", "Serie", 
                                                   "Depositado", "Poupanca","Num. PA", "CPF conta", 
                                                   "Banco", "Num.Agência", "Conta"]]
        df_beneficio.sort_values(by="Ano Letivo", inplace=True)
        st.dataframe(df_beneficio, use_container_width=True, hide_index=True,
                 column_config={"Ano Letivo": st.column_config.NumberColumn(format="%.0f"),
                                "Serie": st.column_config.NumberColumn(format="%.0f"),
                                 "Poupanca": st.column_config.NumberColumn(format="%.0f"),
                                 "Depositado": st.column_config.NumberColumn(format="%.0f"),
                                 "Num.Agência": st.column_config.NumberColumn(format="%.0f"),
                                 "CPF conta": st.column_config.NumberColumn(format="%.0f")})
    else:
        st.header("Aluno não encontrado")

# Aba "Conta Poupança"
with tab5:
    # Realizar as instruções a seguir apenas se idt_elegivel existir em df_dadosbasicos
    if idt_elegivel in df_contas["cod_aluno"].to_list():
        dados_pessoais = df_dadosbasicos[df_dadosbasicos["Cód."] == idt_elegivel].iloc[0]

        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")

        # Localizar e apresentar os valores de cod_conta, dat_open, num_cpf, Banco, Agência e conta
        conta_info = df_contas[df_contas["cod_aluno"] == idt_elegivel]

        if not conta_info.empty:
            cod_conta = conta_info["cod_conta"].values[0]
            dat_open = conta_info["dat_open"].values[0]#.strftime("%d/%m/%Y")
            num_cpf = conta_info["num_cpf"].values[0]
            banco = conta_info["Banco"].values[0]
            agencia = conta_info["Agencia"].values[0]
            conta = conta_info["Conta"].values[0]

            st.subheader("Informações da Conta")
            st.write(f"**Código da Conta:** {cod_conta}")
            
            if pd.isna(dat_open):
                st.write("Data de abertura: Não informada")
            else:
                st.write(f"**Data de Abertura:** {dat_open}")
                       
            st.write(f"**CPF:** {num_cpf}")#{num_cpf[:2]}.{num_cpf[3:5]}.{num_cpf[6:8]}-{num_cpf[9:]}")
            st.write(f"**Banco:** {banco}")
            st.write(f"**Agência:** {agencia}")
            st.write(f"**Conta:** {conta}")
        else:
            st.write("Nenhuma conta encontrada para o aluno.")
    else:
        st.write("Aluno não possui conta-poupança registrada.")
