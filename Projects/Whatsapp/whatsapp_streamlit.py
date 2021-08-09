import streamlit as st
import pandas as pd
import pywhatkit as pwk

st.title('Whatsapp Sender')
#Instruções
st.header('Instruções:')
st.text('Para visualizar as intruções basta selecionar os campos:')
if st.checkbox('Instruções Arquivo'):
    st.subheader('Arquivo:')
    st.text('Para iniciarmos, é necessário que você insira um documento planilha, com um campo chamado \n\"nome\" e outro \"telefone\".')
    st.text('Exemplo:')
    st.image('https://i.ibb.co/LYgCk5d/exemplo-tabela.png')
    st.text('Os seguintes formatos são suportados: .xlsx( Excel) e .CSV( valores separados por virgula).')

if st.checkbox('Instruções Mensagem'):
    st.write('Na sessão de mensegens, é possivel inserir imagens e links.')
    st.subheader('Formatações:')
    st.text('Caso queira utilizar o nome do usuário no meio da sentença, basta inserir \'{nome}\'')
    st.text('Caso queira apresentar o texto em itálico utilize: _texto_')
    st.text('Caso queira apresentar o texto em negrito utilize: *texto*')
    st.text('Caso queira apresentar o texto em tachado utilize: ~texto~')
    st.text('Caso queira apresentar o texto em monoespaçado utilize: ```texto```')
    st.subheader('Emojis:')
    st.write('É possivel inserir emojis no meio da mensagem, para isso acesse a \n[lista de emojis](https://emojiterra.com/pt/lista/), copie e cole onde deseja usá-los.')

#Carregando arquivo.
st.header('Carregando o arquivo:')
data_file = st.file_uploader('Carregar Planilha',type=['xlsx','csv'])

if data_file is not None:
    # st.write(type(data_file))
    nome_arquivo = data_file.name
    extensao = nome_arquivo.split('.')[1]
    if extensao == 'csv':
        df = pd.read_csv(data_file)
        st.text('Conjunto de dados selecionado:')
        try:
            df = df[['nome','telefone']]
        except:    
            st.warning('Coluna nome e/ou telefone não encontradas.')
        st.dataframe(df)
    elif extensao == 'xlsx':
        df = pd.read_excel(data_file)
        st.text('Conjunto de dados selecionado:')
        try:
            df = df[['nome','telefone']]
        except:
            st.warning('Coluna nome e/ou telefone não encontradas.')
    else:
        st.warning('Formato de dados não suportado!')

st.header('Texto a ser enviado:')
user_input = st.text_input("Digite seu texto aqui:", 'Olá {nome}, _gosto_ *muito* de ~você~!',100000)
    

data_file = st.file_uploader('Carregar Imagem',type=['png','jpg','jpeg'])

if st.button('Enviar Mensagens!'):
    if data_file is not None:   
        for index in df.index:
            ntelefone = df.loc[index].telefone
            nome = df.loc[index].nome
            texto_divulgacao = user_input.replace('{nome}',nome)
            pwk.sendwhats_image(phone_no=f'+55{ntelefone}',
                            img_path=data_file,
                            caption=f'{texto_divulgacao}',wait_time=5,tab_close=True)
    else:
        for index in df.index:
            ntelefone = df.loc[index].telefone
            nome = df.loc[index].nome
            texto_divulgacao = user_input.replace('{nome}',nome)
            pwk.sendwhatmsg_instantly(phone_no=f'+55{ntelefone}',
                            message=f'{texto_divulgacao}',wait_time=5,tab_close=True)