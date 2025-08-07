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
    df_financ =  pd.read_csv('DF_FINANC.csv')    
    df_pas =  pd.read_csv('DF_PAS.csv')       
    
    return df_alunos, df_familias, df_dadosbasicos, df_resultados, df_beneficios,df_contas, df_financ, df_pas

df_alunos, df_familias, df_dadosbasicos, df_resultados, df_beneficios,df_contas, df_financ, df_pas = load_data()

# Sidebar
st.sidebar.title("Pesquisar Aluno")
st.sidebar.write("")
# *************************************************************
st.sidebar.text("Última atualização: 07/08/2025")
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
tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["Pesquisa","Dados Pessoais","Resultados","Benefícios","Conta Poupança","Ficha Financeira","Inserção PA" ])

with tab1:
    # Aba "Pesquisa"
    # Apresentar dataframe na aba Pesquisa
    
    # Formatando a data
    df_familias["Nascimento"] = pd.to_datetime(df_familias["Nascimento"], errors="coerce").dt.strftime("%d/%m/%Y")
    
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
                st.write("Data da Carga: Não informada")
            else:
                st.write(f"**Data da Carga:** {dat_open}")
                       
            st.write(f"**CPF:** {num_cpf}")#{num_cpf[:2]}.{num_cpf[3:5]}.{num_cpf[6:8]}-{num_cpf[9:]}")
            st.write(f"**Banco:** {banco}")
            st.write(f"**Agência:** {agencia}")
            st.write(f"**Conta:** {conta}")
        else:
            st.write("Nenhuma conta encontrada para o aluno.")
    else:
        st.write("Aluno não possui conta-poupança registrada.")

# Aba "Ficha Financeira"

with tab6:
    if idt_elegivel in df_dadosbasicos["Cód."].to_list():
        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")

        # Filtrar e selecionar colunas
        df_financ = df_financ[df_financ["Cod"] == idt_elegivel][["Ano Letivo", "Serie", 
                                                                 "Banco", "Agencia", "Conta", 
                                                                 "Valor(R$)", "Deposito", "Numero PA"]]

        # Ordenar por data
        df_financ.sort_values(by="Deposito", inplace=True)

        # Formatando a data
        df_financ["Deposito"] = pd.to_datetime(df_financ["Deposito"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Ajustar largura visual com espaços
        df_financ["Ano Letivo"] = df_financ["Ano Letivo"].astype(str).str.strip()
        df_financ["Serie"] = df_financ["Serie"].astype(str).str.strip()
        df_financ["Banco"] = df_financ["Banco"].astype(str).str.strip()
        df_financ["Agencia"] = df_financ["Agencia"].astype(str).str.strip()
        df_financ["Valor(R$)"] = df_financ["Valor(R$)"].map(lambda x: f"{x:.2f}".strip())

        df_financ["Conta"] = df_financ["Conta"].astype(str).apply(lambda x: f"{x}      ")
        df_financ["Numero PA"] = df_financ["Numero PA"].astype(str).apply(lambda x: f"{x}   ")

        # Exibir tabela
        st.dataframe(df_financ, use_container_width=True, hide_index=True,
                     column_config={
                         "Ano Letivo": st.column_config.TextColumn(),
                         "Serie": st.column_config.TextColumn(),
                         "Banco": st.column_config.TextColumn(),
                         "Agencia": st.column_config.TextColumn(),
                         "Valor(R$)": st.column_config.TextColumn(),
                         "Conta": st.column_config.TextColumn(),
                         "Numero PA": st.column_config.TextColumn()
                     })

        # Calcular total depositado
        total_depositado = df_financ["Valor(R$)"].astype(float).sum()
        st.subheader(f"Total depositado até o momento: R$ {total_depositado:,.2f}")
    else:
        st.header("Aluno não encontrado")

# Aba "Inserção PA"
with tab7:                              
      
     if idt_elegivel in df_dadosbasicos["Cód."].to_list():
        st.header(f"{idt_elegivel} - {dados_pessoais['Aluno']}")

        # Filtrar e selecionar colunas
        df_pas = df_pas[df_pas["Cod"] == idt_elegivel][["Ano Letivo", "Serie", 
                                                   "Banco", "Agencia","Conta", "Valor(R$)", 
                                                   "Envio", "Numero PA"]]

        # Formatando a data
        df_pas["Envio"] = pd.to_datetime(df_pas["Envio"], errors="coerce").dt.strftime("%d/%m/%Y")

        # Ajustar largura visual com espaços
        df_pas["Ano Letivo"] = df_pas["Ano Letivo"].astype(str).str.strip()
        df_pas["Serie"] = df_pas["Serie"].astype(str).str.strip()
        df_pas["Banco"] = df_pas["Banco"].astype(str).str.strip()
        df_pas["Agencia"] = df_pas["Agencia"].astype(str).str.strip()
        df_pas["Valor(R$)"] = df_pas["Valor(R$)"].map(lambda x: f"{x:.2f}".strip())

        df_pas["Conta"] = df_pas["Conta"].astype(str).apply(lambda x: f"{x}      ")
        df_pas["Numero PA"] = df_pas["Numero PA"].astype(str).apply(lambda x: f"{x}   ")

        # Ordenar por data
        df_pas.sort_values(by="Envio", inplace=True)

        # Exibir tabela
        st.dataframe(df_pas, use_container_width=True, hide_index=True,
                     column_config={
                         "Ano Letivo": st.column_config.TextColumn(),
                         "Serie": st.column_config.TextColumn(),
                         "Banco": st.column_config.TextColumn(),
                         "Agencia": st.column_config.TextColumn(),
                         "Valor(R$)": st.column_config.TextColumn(),
                         "Conta": st.column_config.TextColumn(),
                         "Numero PA": st.column_config.TextColumn()
                     })
     else:
        st.header("Aluno não encontrado")