# Interface grafica (site) do ERP de Varejo, feita com a biblioteca Streamlit.
# Toda a logica fica em erp.py; a aparencia fica em estilo.py.
# Aqui so montamos as telas e chamamos as funcoes do sistema.
import streamlit as st
import erp
import estilo
import pdf

st.set_page_config(page_title=estilo.EMPRESA, page_icon="logo.svg", layout="wide",
                   initial_sidebar_state="expanded")
estilo.aplicar_css()


# ================= LOGIN =================
# shortcut: senha fixa no codigo (fica visivel no GitHub); e so para a apresentacao, nao e seguranca de verdade.
USUARIO = "ERP varejo"
SENHA = "adm123ERP"

# st.session_state guarda valores de cada pessoa que abre o site (cada navegador tem o seu).
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    esquerda, direita = st.columns([1.15, 1], gap="large")
    with esquerda:
        estilo.login_painel()
    with direita:
        estilo.login_titulo()
        with st.form("login"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", use_container_width=True)
        if entrar:
            if usuario.strip() == USUARIO and senha == SENHA:
                st.session_state.logado = True
                st.rerun()
            else:
                estilo.aviso("Usuário ou senha inválidos.")
    st.stop()   # sem login, o resto do site nao e montado


def nome_produto(codigo):
    return f"#{codigo} · {erp.buscar_produto(codigo)[1]}"


def nome_fornecedor(codigo):
    return f"#{codigo} · {erp.buscar_fornecedor(codigo)[1]}"


def codigos(lista):
    resultado = []
    for registro in lista:
        resultado.append(registro[0])
    return resultado


with st.sidebar:
    estilo.logo()
    icones = {"Painel": "dashboard", "Produtos": "inventory_2", "Fornecedores": "local_shipping",
              "Movimentações": "swap_vert", "Reposição": "pending_actions", "Relatórios": "description"}
    pagina = st.radio("Menu", list(icones), label_visibility="collapsed",
                      format_func=lambda nome: f":material/{icones[nome]}: {nome}")


# ================= PAINEL =================
if pagina == "Painel":
    estilo.cabecalho("Painel", "Visão geral do estoque da loja.")

    valor = 0
    unidades = 0
    for p in erp.produtos:
        valor = valor + erp.valor_total(p)
        unidades = unidades + p[4]

    estilo.kpis([
        ["Produtos", len(erp.produtos), f"{unidades} unidades em estoque", False],
        ["Valor em estoque", estilo.dinheiro(valor), "a preço de venda", False],
        ["Abaixo do mínimo", len(erp.fila_prioridade), "aguardando reposição", len(erp.fila_prioridade) > 0],
        ["Fornecedores", len(erp.fornecedores), "cadastrados", False],
        ["Movimentações", len(erp.historico), "registradas", False],
    ])

    col1, col2 = st.columns([5, 4], gap="large")
    with col1:
        estilo.secao("Estoque por produto", "A linha vertical marca o estoque mínimo de cada item.")
        estilo.grafico_estoque(erp.produtos)
    with col2:
        estilo.secao("Próximas reposições", "Itens mais urgentes.")
        estilo.fila_visual(erp.ver_fila(), limite=3)
        estilo.secao("Últimas movimentações", "Mais recentes primeiro.")
        estilo.pilha_visual(erp.historico, erp.buscar_produto, limite=4)


# ================= PRODUTOS =================
elif pagina == "Produtos":
    estilo.cabecalho("Produtos", "Cadastre, consulte, altere e remova produtos.")
    aba1, aba2, aba3, aba4 = st.tabs(["Cadastrar", "Buscar", "Alterar", "Remover"])

    with aba1:
        with st.form("cad_produto", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            codigo = c1.number_input("Código", min_value=1, step=1)
            nome = c2.text_input("Nome *")
            categoria = c3.text_input("Categoria *")
            c4, c5, c6 = st.columns(3)
            preco = c4.number_input("Preço (R$)", min_value=0.0, step=0.5, format="%.2f")
            estoque = c5.number_input("Estoque", min_value=0, step=1)
            minimo = c6.number_input("Estoque mínimo", min_value=0, step=1)
            if st.form_submit_button("Cadastrar produto"):
                estilo.aviso(erp.cadastrar_produto(codigo, nome, categoria, preco, estoque, minimo))

    with aba2:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            estilo.secao("Por código", "Encontra o produto pelo código.")
            codigo = st.number_input("Código do produto", min_value=1, step=1, key="bus_cod")
            if st.button("Buscar por código"):
                produto = erp.buscar_produto(codigo)
                if produto == None:
                    estilo.aviso("Produto não encontrado.")
                else:
                    estilo.tabela_produtos([produto])
        with c2:
            estilo.secao("Por nome", "Lista todos os produtos cujo nome contém o texto.")
            texto = st.text_input("Nome ou parte do nome", key="bus_nome")
            if st.button("Buscar por nome"):
                estilo.tabela_produtos(erp.busca_linear_por_nome(texto))

    with aba3:
        codigo = st.selectbox("Escolha o produto", codigos(erp.produtos), format_func=nome_produto, key="alt_cod")
        if codigo != None:
            p = erp.buscar_produto(codigo)
            with st.form(f"alt_produto_{codigo}"):
                c1, c2 = st.columns(2)
                nome = c1.text_input("Novo nome (vazio = manter)", placeholder=p[1])
                categoria = c2.text_input("Nova categoria (vazio = manter)", placeholder=p[2])
                c3, c4, c5 = st.columns(3)
                preco = c3.number_input("Preço (R$)", min_value=0.0, step=0.5, format="%.2f", value=float(p[3]))
                estoque = c4.number_input("Estoque", min_value=0, step=1, value=p[4])
                minimo = c5.number_input("Estoque mínimo", min_value=0, step=1, value=p[5])
                if st.form_submit_button("Salvar alteração"):
                    estilo.aviso(erp.alterar_produto(codigo, nome, categoria, preco, estoque, minimo))

    with aba4:
        codigo = st.selectbox("Escolha o produto", codigos(erp.produtos), format_func=nome_produto, key="rem_cod")
        if codigo != None and st.button("Remover produto"):
            estilo.aviso(erp.remover_produto(codigo))

    estilo.secao("Produtos cadastrados", f"{len(erp.produtos)} produto(s).")
    estilo.tabela_produtos(erp.produtos)


# ================= FORNECEDORES =================
elif pagina == "Fornecedores":
    estilo.cabecalho("Fornecedores", "Cadastre, consulte, altere e remova fornecedores.")
    aba1, aba2, aba3, aba4 = st.tabs(["Cadastrar", "Buscar", "Alterar", "Remover"])

    with aba1:
        with st.form("cad_fornecedor", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            codigo = c1.number_input("Código", min_value=1, step=1)
            nome = c2.text_input("Nome *")
            telefone = c3.text_input("Telefone")
            if st.form_submit_button("Cadastrar fornecedor"):
                estilo.aviso(erp.cadastrar_fornecedor(codigo, nome, telefone))

    with aba2:
        codigo = st.number_input("Código do fornecedor", min_value=1, step=1, key="fbus_cod")
        if st.button("Buscar fornecedor"):
            f = erp.buscar_fornecedor(codigo)
            if f == None:
                estilo.aviso("Fornecedor não encontrado.")
            else:
                estilo.tabela_fornecedores([f])

    with aba3:
        codigo = st.selectbox("Escolha o fornecedor", codigos(erp.fornecedores), format_func=nome_fornecedor, key="falt_cod")
        if codigo != None:
            f = erp.buscar_fornecedor(codigo)
            with st.form(f"alt_fornecedor_{codigo}"):
                c1, c2 = st.columns(2)
                nome = c1.text_input("Novo nome (vazio = manter)", placeholder=f[1])
                telefone = c2.text_input("Novo telefone (vazio = manter)", placeholder=f[2])
                if st.form_submit_button("Salvar alteração"):
                    estilo.aviso(erp.alterar_fornecedor(codigo, nome, telefone))

    with aba4:
        codigo = st.selectbox("Escolha o fornecedor", codigos(erp.fornecedores), format_func=nome_fornecedor, key="frem_cod")
        if codigo != None and st.button("Remover fornecedor"):
            estilo.aviso(erp.remover_fornecedor(codigo))

    estilo.secao("Fornecedores cadastrados", f"{len(erp.fornecedores)} fornecedor(es).")
    estilo.tabela_fornecedores(erp.fornecedores)


# ================= ESTOQUE (PILHA) =================
elif pagina == "Movimentações":
    estilo.cabecalho("Movimentações", "Registre entradas e saídas de estoque. Lançou errado? Desfaça a última.")

    col1, col2 = st.columns([2, 3], gap="large")
    with col1:
        estilo.secao("Nova movimentação")
        with st.container(border=True):
            codigo = st.selectbox("Produto", codigos(erp.produtos), format_func=nome_produto, key="mov_cod")
            quantidade = st.number_input("Quantidade", min_value=1, step=1, key="mov_qtd")
            b1, b2 = st.columns(2)
            entrada = b1.button("Entrada", icon=":material/add:", use_container_width=True)
            saida = b2.button("Saída", icon=":material/remove:", use_container_width=True)
            desfazer = st.button("Desfazer última movimentação", icon=":material/undo:", use_container_width=True)
        if entrada and codigo != None:
            estilo.aviso(erp.entrada_estoque(codigo, quantidade))
        if saida and codigo != None:
            estilo.aviso(erp.saida_estoque(codigo, quantidade))
        if desfazer:
            estilo.aviso(erp.desfazer_movimentacao())
    with col2:
        estilo.secao("Histórico", f"{len(erp.historico)} movimentação(ões), mais recentes primeiro.")
        estilo.pilha_visual(erp.historico, erp.buscar_produto, limite=10)


# ================= FILA DE PRIORIDADE =================
elif pagina == "Reposição":
    estilo.cabecalho("Reposição", "Produtos abaixo do estoque mínimo, do mais urgente (o que mais falta) ao menos urgente.")

    if st.button("Atender a reposição mais urgente", icon=":material/local_shipping:"):
        estilo.aviso(erp.atender_reposicao())

    itens = erp.ver_fila()
    faltam = 0
    for item in itens:
        faltam = faltam + item[0]
    maior = "—"
    if len(itens) > 0:
        maior = itens[0][1][1]
    estilo.kpis([
        ["Pendentes", len(itens), "produtos abaixo do mínimo", len(itens) > 0],
        ["Mais urgente", maior, "será atendido primeiro", False],
        ["Unidades a repor", faltam, "para chegar ao mínimo", False],
    ])
    estilo.fila_visual(itens)


# ================= RELATORIOS =================
elif pagina == "Relatórios":
    estilo.cabecalho("Relatórios", "Consulte o estoque por categoria, veja o ranking e exporte em PDF.")
    aba1, aba2, aba3, aba4 = st.tabs(["Todos os produtos", "Por categoria", "Ranking", "Exportar PDF"])

    with aba1:
        estilo.tabela_produtos(erp.produtos)

    with aba2:
        categoria = st.selectbox("Categoria", erp.listar_categorias())
        if categoria != None:
            estilo.tabela_produtos(erp.filtrar_por_categoria(categoria))

    with aba3:
        escolha = st.radio("Ordenar por (maior primeiro)", ["Quantidade em estoque", "Valor total em estoque"],
                           horizontal=True)
        if escolha == "Quantidade em estoque":
            estilo.tabela_produtos(erp.bubble_sort("estoque"), ranking=True)
        else:
            estilo.tabela_produtos(erp.bubble_sort("valor"), ranking=True)

    with aba4:
        estilo.secao("Filtros", "O PDF inclui apenas os produtos que atendem a todos os filtros.")
        todas = erp.listar_categorias()
        situacoes_todas = ["OK", "Abaixo do mínimo", "Zerado"]
        maior_preco = 0.0
        for p in erp.produtos:
            if p[3] > maior_preco:
                maior_preco = float(p[3])

        c1, c2 = st.columns(2)
        categorias = c1.multiselect("Categorias", todas, default=todas)
        situacoes = c2.multiselect("Situação do estoque", situacoes_todas, default=situacoes_todas)
        c3, c4, c5 = st.columns(3)
        preco_min = c3.number_input("Preço mínimo (R$)", min_value=0.0, step=1.0, format="%.2f")
        preco_max = c4.number_input("Preço máximo (R$)", min_value=0.0, value=maior_preco, step=1.0, format="%.2f")
        texto = c5.text_input("Nome contém (opcional)")
        ordem = st.radio("Ordenar por", ["Código (ordem de cadastro)", "Quantidade em estoque (maior primeiro)",
                                         "Valor total em estoque (maior primeiro)"], horizontal=True)
        c6, c7 = st.columns(2)
        com_fila = c6.checkbox("Incluir reposições pendentes", value=True)
        com_pilha = c7.checkbox("Incluir histórico de movimentações")

        if ordem == "Quantidade em estoque (maior primeiro)":
            base = erp.bubble_sort("estoque")
        elif ordem == "Valor total em estoque (maior primeiro)":
            base = erp.bubble_sort("valor")
        else:
            base = erp.produtos
        filtrados = erp.filtrar_produtos(base, categorias, situacoes, preco_min, preco_max, texto)

        # frases que aparecem no topo do PDF, dizendo quais filtros foram usados
        filtros = []
        filtros.append("Categorias: " + ", ".join(categorias))
        filtros.append("Situação: " + ", ".join(situacoes))
        filtros.append(f"Preço: de {estilo.dinheiro(preco_min)} até {estilo.dinheiro(preco_max)}")
        if texto.strip() != "":
            filtros.append(f"Nome contém: {texto.strip()}")
        filtros.append("Ordenação: " + ordem)

        estilo.secao("Prévia", f"{len(filtrados)} produto(s) no relatório.")
        estilo.tabela_produtos(filtrados)
        st.write("")
        st.download_button("Baixar PDF", icon=":material/download:",
                           data=pdf.gerar(filtrados, filtros, com_fila, com_pilha),
                           file_name="relatorio_estoque.pdf", mime="application/pdf")


# resumo da barra lateral (fica no fim para ja mostrar os numeros atualizados)
with st.sidebar:
    estilo.resumo_lateral(len(erp.produtos), len(erp.fila_prioridade), len(erp.historico))
    if st.button("Sair", icon=":material/logout:", use_container_width=True):
        st.session_state.logado = False
        st.rerun()
