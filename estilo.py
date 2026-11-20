# Aparencia do site (CSS e pedacos de HTML). Nao tem regra de negocio aqui:
# toda a logica (estruturas e algoritmos) fica em erp.py.
import base64
import html
import os
import streamlit as st

EMPRESA = "Mercado Sol Nascente"
# a logo vira uma <img> com o arquivo embutido (o st.html remove <svg> escrito direto no HTML)
with open(os.path.join(os.path.dirname(__file__), "logo.svg"), "rb") as arquivo:
    LOGO = f'<img src="data:image/svg+xml;base64,{base64.b64encode(arquivo.read()).decode()}" alt="Logo">'

# cores da situacao do estoque (usadas no grafico e nas barras)
COR_OK = "#3f8f68"
COR_BAIXO = "#d08a1e"
COR_ZERADO = "#c0392b"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --primaria: #13263f;
  --primaria2: #1f3b5e;
  --destaque: #f2a71b;
  --texto: #0f172a;
  --suave: #64748b;
  --borda: #e2e8f0;
  --fundo: #f5f6f8;
}

html, body, [class*="css"], .stMarkdown, button, input, textarea, select, label {
  font-family: 'Inter', sans-serif !important;
}
.material-symbols-rounded, [data-testid="stIconMaterial"] { font-family: 'Material Symbols Rounded' !important; }

[data-testid="stAppViewContainer"] { background: var(--fundo); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppDeployButton"], [data-testid="stMainMenu"], footer { display: none; }
.block-container { padding-top: 2.2rem; max-width: 1200px; }

/* ---------- barra lateral ---------- */
[data-testid="stSidebar"] { background: var(--primaria); border-right: none; }
[data-testid="stSidebar"] * { color: #cbd5e1; }
[data-testid="stSidebar"] .stElementContainer:has(.stRadio), [data-testid="stSidebar"] .stRadio,
[data-testid="stSidebar"] [role="radiogroup"], [data-testid="stSidebar"] [role="radiogroup"] > div,
[data-testid="stSidebar"] [role="radiogroup"] label { width: 100% !important; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: .15rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding: .6rem .8rem; border-radius: 8px; width: 100%; cursor: pointer;
  border-left: 3px solid transparent; transition: background .15s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:not([data-testid]) { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255, 255, 255, .05); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: rgba(255, 255, 255, .09); border-left-color: var(--destaque);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * { color: #fff; }
[data-testid="stSidebar"] [role="radiogroup"] label p { font-weight: 500; font-size: .93rem; }
[data-testid="stSidebar"] .stButton > button {
  background: transparent; border: 1px solid rgba(255, 255, 255, .18); box-shadow: none;
}
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255, 255, 255, .06); border-color: rgba(255, 255, 255, .3); }

.logo { display: flex; align-items: center; gap: .75rem; padding: .3rem 0 1.6rem; }
.logo-icone { width: 40px; height: 40px; flex: none; }
.logo-icone img { width: 100%; height: 100%; display: block; border-radius: 9px; }
.logo-nome { font-weight: 700; font-size: .98rem; color: #fff; line-height: 1.2; }
.logo-sub { font-size: .74rem; color: #94a3b8; }
.lateral-card { margin-top: 1.6rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, .1); }
.lateral-card .titulo { font-size: .7rem; text-transform: uppercase; letter-spacing: .08em; color: #94a3b8; margin-bottom: .4rem; }
.lateral-card .linha { display: flex; justify-content: space-between; font-size: .85rem; padding: .25rem 0; }
.lateral-card b { color: #fff; font-weight: 600; }

/* ---------- cabecalho de cada pagina ---------- */
.cab { padding-bottom: 1.1rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--borda); }
.cab h1 { color: var(--texto) !important; font-size: 1.6rem !important; font-weight: 700 !important; margin: 0 !important; padding: 0 !important; letter-spacing: -.01em; }
.cab p { color: var(--suave); margin: .3rem 0 0; font-size: .95rem; }

/* ---------- cartoes de indicadores ---------- */
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .9rem; margin-bottom: 1.4rem; }
.kpi { background: #fff; border-radius: 10px; padding: 1rem 1.15rem; border: 1px solid var(--borda); }
.kpi-rotulo { color: var(--suave); font-size: .8rem; font-weight: 500; }
.kpi-valor { color: var(--texto); font-size: 1.35rem; white-space: nowrap; font-weight: 700; letter-spacing: -.02em; margin-top: .2rem; }
.kpi-nota { color: var(--suave); font-size: .76rem; margin-top: .1rem; }
.kpi.alerta .kpi-valor { color: #b42318; }

/* ---------- caixas / secoes ---------- */
.secao { margin: 1.5rem 0 .7rem; }
.secao h3 { margin: 0 !important; padding: 0 !important; color: var(--texto); font-weight: 600 !important; font-size: 1.05rem !important; }
.secao p { margin: .1rem 0 0; color: var(--suave); font-size: .85rem; }
.caixa { background: #fff; border-radius: 10px; padding: 1.1rem 1.2rem; border: 1px solid var(--borda); }

/* ---------- tabelas ---------- */
.tabela-wrap { background: #fff; border-radius: 10px; border: 1px solid var(--borda); overflow: auto; }
table.tab { width: 100%; border-collapse: collapse; font-size: .86rem; }
table.tab th {
  text-align: left; padding: .7rem .5rem; color: var(--suave); font-size: .72rem; font-weight: 600; letter-spacing: .05em;
  text-transform: uppercase; background: #f8fafc; border-bottom: 1px solid var(--borda); white-space: nowrap;
}
table.tab td { padding: .7rem .5rem; color: var(--texto); border-bottom: 1px solid #f1f5f9; white-space: nowrap; }
table.tab tr:last-child td { border-bottom: none; }
table.tab tbody tr:hover { background: #f8fafc; }
.codigo { color: var(--suave); font-variant-numeric: tabular-nums; font-size: .84rem; }
.nome { font-weight: 600; }
.vazio { padding: 1.8rem; text-align: center; color: var(--suave); }

.badge { display: inline-block; padding: .15rem .55rem; border-radius: 6px; font-size: .75rem; font-weight: 600; }
.ok { color: #1f6b48; background: #e8f5ee; }
.baixo { color: #95600c; background: #fdf3e1; }
.zerado { color: #a02a20; background: #fbe9e7; }
.entrada { color: #1f6b48; background: #e8f5ee; }
.saida { color: #a02a20; background: #fbe9e7; }
.reposicao { color: #1f3b5e; background: #e6edf5; }
.neutro { color: var(--suave); background: #f1f5f9; }

.barra { width: 40px; height: 6px; border-radius: 3px; background: #eef2f6; overflow: hidden; display: inline-block; vertical-align: middle; margin-right: .5rem; }
.barra > span { display: block; height: 100%; border-radius: 3px; }

/* ---------- grafico de estoque ---------- */
.grafico .linha-g { display: grid; grid-template-columns: 150px 1fr 60px; align-items: center; gap: .8rem; padding: .4rem 0; }
.grafico .rot { font-size: .86rem; color: var(--texto); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.grafico .trilho { position: relative; height: 10px; border-radius: 3px; background: #eef2f6; }
.grafico .enche { height: 100%; border-radius: 3px; }
.grafico .minimo { position: absolute; top: -3px; bottom: -3px; width: 2px; background: var(--texto); opacity: .6; }
.grafico .num { font-size: .82rem; color: var(--suave); text-align: right; font-variant-numeric: tabular-nums; }
.legenda { display: flex; gap: 1.1rem; font-size: .78rem; color: var(--suave); margin-top: .7rem; flex-wrap: wrap; }
.legenda i { display: inline-block; width: 9px; height: 9px; border-radius: 2px; margin-right: .35rem; vertical-align: middle; }

/* ---------- listas (historico e reposicao) ---------- */
.lista { background: #fff; border: 1px solid var(--borda); border-radius: 10px; }
.lista-item { display: grid; grid-template-columns: 40px 1fr auto; align-items: center; gap: .9rem; padding: .8rem 1.1rem; border-bottom: 1px solid #f1f5f9; }
.lista-item:last-child { border-bottom: none; }
.lista-item.mov { grid-template-columns: 90px 1fr auto; }
.item-nome { font-weight: 600; color: var(--texto); font-size: .9rem; }
.item-info { color: var(--suave); font-size: .8rem; margin-top: .1rem; }
.item-valor { text-align: right; font-weight: 600; color: var(--texto); font-size: .9rem; white-space: nowrap; }
.item-valor span { display: block; font-size: .72rem; font-weight: 400; color: var(--suave); }
.posicao { width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; font-weight: 600; font-size: .82rem; background: #f1f5f9; color: var(--suave); }
.posicao.urgente { background: #fbe9e7; color: #a02a20; }
.mais { text-align: center; color: var(--suave); font-size: .8rem; padding: .6rem; }

/* ---------- avisos ---------- */
.aviso { padding: .75rem 1rem; border-radius: 8px; font-weight: 500; font-size: .9rem; margin: .6rem 0; border-left: 3px solid; }
.aviso.bom { background: #eef8f2; color: #1f6b48; border-color: #3f8f68; }
.aviso.ruim { background: #fdf0ee; color: #a02a20; border-color: #c0392b; }

/* ---------- componentes do Streamlit ---------- */
[data-testid="stForm"] { background: #fff; border-radius: 10px; padding: 1.3rem 1.4rem; border: 1px solid var(--borda); }
.stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button {
  border-radius: 8px; border: 1px solid var(--primaria); padding: .5rem 1.1rem; font-weight: 600;
  background: var(--primaria); color: #fff; box-shadow: none; transition: background .15s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, [data-testid="stDownloadButton"] > button:hover {
  background: var(--primaria2); border-color: var(--primaria2); color: #fff;
}
.stButton > button p, [data-testid="stFormSubmitButton"] > button p, [data-testid="stDownloadButton"] > button p { color: #fff; font-weight: 600; }
[data-testid="stTabs"] [role="tab"] p { font-weight: 600; }

/* ---------- tela de login ---------- */
.login-painel {
  position: relative; overflow: hidden; border-radius: 14px; padding: 2.6rem 2.4rem; min-height: 460px; color: #fff;
  background: var(--primaria); display: flex; flex-direction: column;
}
.login-painel::after {
  content: ""; position: absolute; width: 380px; height: 190px; right: -90px; bottom: -40px;
  border-radius: 190px 190px 0 0; background: rgba(255, 255, 255, .03);
}
.login-logo { width: 56px; height: 56px; }
.login-logo img { width: 100%; height: 100%; display: block; border-radius: 12px; }
.login-empresa { font-size: 1.9rem; font-weight: 700; line-height: 1.15; margin-top: 1.6rem; letter-spacing: -.02em; }
.login-sub { color: #94a3b8; font-size: .98rem; margin-top: .4rem; max-width: 360px; }
.login-lista { margin-top: 2rem; display: grid; gap: .55rem; position: relative; }
.login-lista div { color: #cbd5e1; font-size: .9rem; padding-left: 1rem; border-left: 2px solid var(--destaque); }
.login-rodape { margin-top: auto; padding-top: 2rem; font-size: .75rem; color: #64748b; position: relative; }
.login-titulo { margin-top: 3.4rem; }
.login-titulo h2 { margin: 0 !important; padding: 0 !important; font-weight: 700 !important; color: var(--texto); font-size: 1.5rem !important; }
.login-titulo p { color: var(--suave); margin: .3rem 0 1.2rem; font-size: .92rem; }
</style>
"""


def aplicar_css():
    st.markdown(CSS, unsafe_allow_html=True)


def t(texto):
    # Escapa o texto digitado pelo usuario para ele nao virar HTML.
    return html.escape(str(texto))


def dinheiro(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def logo():
    st.html(f'<div class="logo"><div class="logo-icone">{LOGO}</div><div>'
            f'<div class="logo-nome">{EMPRESA}</div><div class="logo-sub">Gestão de estoque</div></div></div>')


def login_painel():
    st.html(f'<div class="login-painel"><div class="login-logo">{LOGO}</div>'
            f'<div class="login-empresa">{EMPRESA}</div>'
            '<div class="login-sub">Sistema de gestão de estoque, compras e fornecedores.</div>'
            '<div class="login-lista"><div>Cadastro de produtos e fornecedores</div>'
            '<div>Controle de reposição por urgência</div>'
            '<div>Histórico de entradas e saídas</div>'
            '<div>Relatórios em PDF</div></div>'
            f'<div class="login-rodape">© 2026 {EMPRESA}. Uso interno.</div></div>')


def login_titulo():
    st.html('<div class="login-titulo"><h2>Acessar o sistema</h2>'
            '<p>Informe seu usuário e senha.</p></div>')


def resumo_lateral(total, pendentes, movimentacoes):
    st.html('<div class="lateral-card"><div class="titulo">Resumo</div>'
            f'<div class="linha"><span>Produtos</span><b>{total}</b></div>'
            f'<div class="linha"><span>Reposições pendentes</span><b>{pendentes}</b></div>'
            f'<div class="linha"><span>Movimentações</span><b>{movimentacoes}</b></div></div>')


def cabecalho(titulo, texto):
    st.html(f'<div class="cab"><h1>{titulo}</h1><p>{texto}</p></div>')


def secao(titulo, texto=""):
    st.html(f'<div class="secao"><h3>{titulo}</h3><p>{texto}</p></div>')


def kpis(cartoes):
    # cartoes: lista de [rotulo, valor, nota, alerta]; alerta=True deixa o numero em vermelho
    partes = '<div class="kpis">'
    for c in cartoes:
        classe = "kpi"
        if c[3]:
            classe = "kpi alerta"
        partes += (f'<div class="{classe}"><div class="kpi-rotulo">{c[0]}</div>'
                   f'<div class="kpi-valor">{c[1]}</div><div class="kpi-nota">{c[2]}</div></div>')
    st.html(partes + '</div>')


def aviso(mensagem):
    palavras_ruins = ["não", "inválid", "insuficiente", "obrigatóri", "já cadastrado", "nenhum", "descartada"]
    ruim = False
    for p in palavras_ruins:
        if p in mensagem.lower():
            ruim = True
    if ruim:
        st.html(f'<div class="aviso ruim">{t(mensagem)}</div>')
    else:
        st.html(f'<div class="aviso bom">{t(mensagem)}</div>')
        st.toast(mensagem, icon=":material/check_circle:")


def status(produto):
    if produto[4] == 0:
        return '<span class="badge zerado">Zerado</span>'
    if produto[4] < produto[5]:
        return '<span class="badge baixo">Abaixo do mínimo</span>'
    return '<span class="badge ok">OK</span>'


def cor_estoque(produto):
    if produto[4] == 0:
        return COR_ZERADO
    if produto[4] < produto[5]:
        return COR_BAIXO
    return COR_OK


def barra(produto):
    maximo = produto[5] * 2
    if maximo == 0:
        maximo = 1
    largura = produto[4] / maximo * 100
    if largura > 100:
        largura = 100
    return f'<span class="barra"><span style="width:{largura}%;background:{cor_estoque(produto)}"></span></span>'


def tabela(cabecalho_, linhas):
    if len(linhas) == 0:
        st.html('<div class="tabela-wrap"><div class="vazio">Nenhum registro encontrado.</div></div>')
        return
    partes = '<div class="tabela-wrap"><table class="tab"><thead><tr>'
    for titulo in cabecalho_:
        partes += f'<th>{titulo}</th>'
    partes += '</tr></thead><tbody>'
    for linha in linhas:
        partes += '<tr>'
        for valor in linha:
            partes += f'<td>{valor}</td>'
        partes += '</tr>'
    st.html(partes + '</tbody></table></div>')


def tabela_produtos(lista, ranking=False):
    linhas = []
    posicao = 1
    for p in lista:
        linha = [f'<span class="codigo">{p[0]}</span>', f'<span class="nome">{t(p[1])}</span>', t(p[2]),
                 dinheiro(p[3]), f'{barra(p)}{p[4]}', p[5], dinheiro(p[3] * p[4]), status(p)]
        if ranking:
            linha.insert(0, f'<b>{posicao}º</b>')
        linhas.append(linha)
        posicao += 1
    cab = ["Código", "Produto", "Categoria", "Preço", "Estoque", "Mínimo", "Valor total", "Situação"]
    if ranking:
        cab.insert(0, "Posição")
    tabela(cab, linhas)


def tabela_fornecedores(lista):
    linhas = []
    for f in lista:
        linhas.append([f'<span class="codigo">{f[0]}</span>', f'<span class="nome">{t(f[1])}</span>', t(f[2])])
    tabela(["Código", "Fornecedor", "Telefone"], linhas)


def grafico_estoque(lista):
    if len(lista) == 0:
        st.html('<div class="caixa"><div class="vazio">Nenhum produto cadastrado.</div></div>')
        return
    maior = 1
    for p in lista:
        if p[4] > maior:
            maior = p[4]
        if p[5] > maior:
            maior = p[5]
    partes = '<div class="caixa grafico">'
    for p in lista:
        largura = p[4] / maior * 100
        minimo = p[5] / maior * 100
        partes += (f'<div class="linha-g"><div class="rot">{t(p[1])}</div><div class="trilho">'
                   f'<div class="enche" style="width:{largura}%;background:{cor_estoque(p)}"></div>'
                   f'<div class="minimo" style="left:{minimo}%"></div></div><div class="num">{p[4]} un.</div></div>')
    partes += (f'<div class="legenda"><span><i style="background:{COR_OK}"></i>OK</span>'
               f'<span><i style="background:{COR_BAIXO}"></i>Abaixo do mínimo</span>'
               f'<span><i style="background:{COR_ZERADO}"></i>Zerado</span>'
               '<span><i style="background:#0f172a;opacity:.6;width:2px"></i>Estoque mínimo</span></div></div>')
    st.html(partes)


def pilha_visual(historico, buscar_produto, limite=8):
    # Mostra a pilha de movimentacoes do topo (mais recente) para a base.
    if len(historico) == 0:
        st.html('<div class="caixa"><div class="vazio">Nenhuma movimentação registrada.</div></div>')
        return
    tipos = ["entrada", "saida", "reposicao"]
    nomes = ["Entrada", "Saída", "Reposição"]
    sinais = ["+", "−", "+"]
    partes = '<div class="lista">'
    mostrados = 0
    for i in range(len(historico) - 1, -1, -1):
        if mostrados == limite:
            break
        m = historico[i]
        k = tipos.index(m[0])
        produto = buscar_produto(m[1])
        nome = "Produto removido"
        if produto != None:
            nome = produto[1]
        extra = ""
        if i == len(historico) - 1:
            extra = ' · <span class="badge neutro">Mais recente</span>'
        partes += (f'<div class="lista-item mov"><div><span class="badge {m[0]}">{nomes[k]}</span></div>'
                   f'<div><div class="item-nome">{t(nome)}</div><div class="item-info">Código {m[1]}{extra}</div></div>'
                   f'<div class="item-valor">{sinais[k]}{m[2]} un.</div></div>')
        mostrados += 1
    if len(historico) > limite:
        partes += f'<div class="mais">+ {len(historico) - limite} movimentações anteriores</div>'
    st.html(partes + '</div>')


def fila_visual(itens, limite=50):
    # Mostra a fila de prioridade: o primeiro e o mais urgente.
    if len(itens) == 0:
        st.html('<div class="caixa"><div class="vazio">Nenhuma reposição pendente.</div></div>')
        return
    partes = '<div class="lista">'
    posicao = 1
    for item in itens:
        if posicao > limite:
            break
        p = item[1]
        classe = "posicao"
        if posicao == 1:
            classe = "posicao urgente"
        partes += (f'<div class="lista-item"><div class="{classe}">{posicao}</div>'
                   f'<div><div class="item-nome">{t(p[1])} {status(p)}</div>'
                   f'<div class="item-info">Código {p[0]} · {t(p[2])} · estoque {p[4]} de {p[5]}</div></div>'
                   f'<div class="item-valor">{item[0]} un.<span>faltam</span></div></div>')
        posicao += 1
    st.html(partes + '</div>')
