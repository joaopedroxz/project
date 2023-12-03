#ARRUMAR ORDENAÇÃO
#QUASE PRONTO COM ICONE DO WPP E BUSCA POR CATEGORIA
import time
import streamlit as st


class Contato:
    def __init__(self, nome, numero,categoria):
        self.nome = nome
        self.numero = numero
        self.categoria = categoria
        self.anterior = None
        self.proximo = None


class Listacontatos:
    def __init__(self):
        self.cabeca = None
        self.cauda = None

    def adicionar_contato(self, nome, numero, categoria):
        if self.busca_binaria(nome):
            st.warning("Este contato já existe na sua Agenda!")
            return
        novo_contato = Contato(nome, numero, categoria)

        if self.cabeca is None:
            self.cabeca = novo_contato
            self.cauda = novo_contato
        else:
            atual = self.cabeca
            while atual is not None and nome.lower() > atual.nome.lower():
                atual = atual.proximo

            if atual is None:  # Inserir no final
                self.cauda.proximo = novo_contato
                novo_contato.anterior = self.cauda
                self.cauda = novo_contato
            elif atual.anterior is None:  # Inserir no início
                novo_contato.proximo = self.cabeca
                self.cabeca.anterior = novo_contato
                self.cabeca = novo_contato
            else:  # Inserir no meio
                novo_contato.proximo = atual
                novo_contato.anterior = atual.anterior
                atual.anterior.proximo = novo_contato
                atual.anterior = novo_contato

    def mover_remover(self, nome):
        atual = self.cabeca

        while atual:

            if atual.nome == nome:
                if atual == self.cabeca:
                    return self.apagar_primeiro_contato()

                anterior = atual.anterior
                proximo = atual.proximo

                if anterior:
                    anterior.proximo = proximo
                else:
                    self.cabeca = proximo

                if proximo:
                    proximo.anterior = anterior
                else:
                    self.cauda = anterior

                atual.proximo = self.cabeca
                atual.anterior = None
                self.cabeca.anterior = atual
                self.cabeca = atual

                return self.apagar_primeiro_contato()

            if atual.proximo == None:
                print("Não encontrado")
                return
            atual = atual.proximo

    def apagar_primeiro_contato(self):
        if self.cabeca is None:
            return

        primeiro_contato = self.cabeca
        self.cabeca = primeiro_contato.proximo

        if self.cabeca:
            self.cabeca.anterior = None
        else:
            self.cauda = None

        del primeiro_contato


    def busca_binaria(self, nome):
        inicio = 0
        fim = self.contar_contatos() - 1
        while inicio <= fim:
            meio = (inicio + fim) // 2
            posicao = 0
            atual = self.cabeca
            # Encontrar o meio na lista encadeada
            while posicao < meio:
                atual = atual.proximo
                posicao += 1
            # Verificar se o nome está no meio da lista
            if atual.nome.lower() == nome.lower():
                return atual
            elif atual.nome.lower() < nome.lower():
                inicio = meio + 1
            else:
                fim = meio - 1
        return None

    def contar_contatos(self):
        contador = 0
        atual = self.cabeca
        while atual:
            contador += 1
            atual = atual.proximo
        return contador

    def obter_contatos_por_categoria(self, categoria):
        contatos_categoria = []
        atual = self.cabeca
        while atual:
            if atual.categoria.lower() == categoria.lower():
                contatos_categoria.append(atual)
            atual = atual.proximo
        return contatos_categoria

def validador_nome(nome):
    if len(nome) > 0:
        return nome
def validador_numero(numero):
    if len(numero) == 11:
        return numero
def validador_categoria(categoria):
    if categoria:
        return categoria

st.set_page_config(page_title="Agenda de Contatos")

def obter_ou_criar_lista():
    if "lista_dupla" not in st.session_state:
        st.session_state.lista_dupla = Listacontatos()
    return st.session_state.lista_dupla


def imprimir_agenda():
    st.header("Sua Agenda de Contatos:")
    lista_dupla = obter_ou_criar_lista()
    contato_atual = lista_dupla.cabeca
    while contato_atual is not None:
        st.write(f"Nome: {contato_atual.nome}")
        st.write(f"Categoria: {contato_atual.categoria}")
        st.write(f"Número: {contato_atual.numero}")

        st.write("---")
        contato_atual = contato_atual.proximo



with st.container():
    st.title("Agenda de Contatos")
    st.write('---')

with st.container():
    st.subheader("Adicionar novo contato:")
    nome = st.text_input("Nome:")
    categoria = st.text_input("Categoria:")
    numero = st.text_input("Número:", help="(00) 00000-0000")

    if validador_nome(nome) and validador_numero(numero) and validador_categoria(categoria):
        if st.button("Salvar", key="salvar_contato"):
            lista_dupla = obter_ou_criar_lista()
            lista_dupla.adicionar_contato(nome, numero, categoria)
            st.success(f"O contato de  {nome} com número {numero} e categoria {categoria} foi registrado!")

    else:
        st.warning("Por favor, digite o nome do contato e o número com 11 dígitos!")

with st.container():
    st.subheader("Remover contato:")
    nome_remove = st.text_input("Nome do contato a ser removido:")
    if validador_nome(nome_remove):
        if st.button("Remover", key="remover_contato"):
            lista_dupla = obter_ou_criar_lista()
            lista_dupla.mover_remover(nome_remove)
            st.success(f"O contato de {nome_remove} foi removido da sua Agenda!")
        else:
            st.error("O contato não foi encontrado na sua Agenda")
            #st.experimental_rerun()
    else:
        st.warning("Digite um nome para ser removido")
with st.container():
    opc = st.sidebar.selectbox("Outras opções:", ("Home", "Buscar contato", "Buscar contato por categoria"))
    if opc == "Buscar contato":
        st.subheader("Buscar")
        nome_busca = st.text_input("Digite o nome de um contato para buscar:")
        if st.button("Buscar"):
            lista_dupla = obter_ou_criar_lista()
            nome_busca = nome_busca.strip().lower()  # Remover espaços extras e transformar em minúsculas
            resultado_busca = lista_dupla.busca_binaria(nome_busca)
            if resultado_busca:
                st.success(f"Contato encontrado\n- Nome: {resultado_busca.nome}\n- Número: {resultado_busca.numero}")
                st.write("Opções:")
                url_whatsapp = f"https://wa.me/{resultado_busca.numero}"
                st.markdown('<i class="fab fa-whatsapp" style="font-size: 2em;"></i>', unsafe_allow_html=True)
                st.markdown(
                    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
                    unsafe_allow_html=True)
                st.link_button('Encaminhar para o Whatsapp', url_whatsapp, help="Abrir Whatsapp")
                # st.link_button('Enviar um email')

            else:
                st.error("Contato não encontrado.")

    if opc == "Buscar contato por categoria":
        st.subheader("Buscar por categoria")
        categoria_busca = st.text_input("Digite a categoria para buscar:")

        if st.button("Buscar"):
            lista_dupla = obter_ou_criar_lista()

            # Exibindo contatos por categoria
            contatos_por_categoria = lista_dupla.obter_contatos_por_categoria(categoria_busca)
            if contatos_por_categoria:
                st.subheader(f"Contatos da categoria '{categoria_busca}':")
                for contato in contatos_por_categoria:
                    st.success(f"Nome: {contato.nome}")
                    st.success(f"Número: {contato.numero}")
            else:
                st.warning(f"Nenhum contato encontrado na categoria '{categoria_busca}'.")




if st.sidebar.button('Atualizar página'):
    with st.spinner("Atualizando..."):
        time.sleep(2)
        st.experimental_rerun()
        st.empty()



imprimir_agenda()
st.caption("Desenvolvido por João Pedro, Roberth e Jonata.")