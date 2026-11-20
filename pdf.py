# Monta o relatorio em PDF (biblioteca fpdf2). So aparencia do arquivo:
# os produtos ja chegam filtrados e ordenados pelas funcoes de erp.py.
import os
from datetime import datetime, timedelta, timezone
from fpdf import FPDF
from fpdf.fonts import FontFace
import erp
import estilo

BRASILIA = timezone(timedelta(hours=-3))   # horario de Brasilia (sem horario de verao desde 2019)
LOGO = os.path.join(os.path.dirname(__file__), "logo.svg")

ROXO = (19, 38, 63)   # azul-marinho da marca
ESCURO = (15, 23, 42)
CINZA = (100, 116, 139)
LINHA = (248, 250, 252)
CORES_SITUACAO = {"OK": (31, 107, 72), "Abaixo do mínimo": (149, 96, 12), "Zerado": (160, 42, 32)}


def limpo(texto):
    # As fontes padrao do PDF so tem os caracteres latin-1 (acentos do portugues ok).
    return str(texto).encode("latin-1", "replace").decode("latin-1")


def dinheiro(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


class RelatorioPDF(FPDF):
    def header(self):
        self.set_fill_color(*ROXO)
        self.rect(0, 0, self.w, 24, "F")
        self.set_fill_color(242, 167, 27)
        self.rect(0, 24, self.w, 1.5, "F")
        self.image(LOGO, x=10, y=4, w=16, h=16)
        self.set_text_color(255, 255, 255)
        self.set_xy(30, 5.5)
        self.set_font("Helvetica", "B", 17)
        self.cell(0, 8, limpo(f"{estilo.EMPRESA} - Relatório de produtos"))
        self.set_xy(30, 13.5)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, limpo(f"Gestão de estoque  ·  Gerado em {self.gerado_em}"))
        self.set_y(32)
        self.set_text_color(*ESCURO)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*CINZA)
        self.cell(0, 5, f"Página {self.page_no()} de {{nb}}", align="C")


def titulo(pdf, texto):
    if pdf.get_y() > pdf.page_break_trigger - 30:   # sem espaco para titulo + linhas: comeca outra pagina
        pdf.add_page()
    pdf.ln(3)
    y = pdf.get_y()
    pdf.set_fill_color(*ROXO)
    pdf.rect(10, y + 1, 1.6, 6, "F")
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*ESCURO)
    pdf.cell(0, 8, limpo(texto), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def cartoes(pdf, itens):
    largura = (pdf.epw - 3 * 4) / 4
    y = pdf.get_y()
    for i in range(len(itens)):
        x = 10 + i * (largura + 4)
        pdf.set_fill_color(*LINHA)
        pdf.set_draw_color(226, 232, 240)
        pdf.rect(x, y, largura, 18, "DF", round_corners=True, corner_radius=2.5)
        pdf.set_xy(x + 4, y + 2.5)
        pdf.set_font("Helvetica", "", 8.5)
        pdf.set_text_color(*CINZA)
        pdf.cell(largura - 8, 5, limpo(itens[i][0]))
        pdf.set_xy(x + 4, y + 8)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(*ESCURO)
        pdf.cell(largura - 8, 8, limpo(itens[i][1]))
    pdf.set_y(y + 22)


def tabela(pdf, cabecalho, linhas, larguras, alinhamentos, coluna_situacao=-1):
    pdf.set_font("Helvetica", "", 9)
    pdf.set_draw_color(226, 232, 240)
    pdf.set_fill_color(255, 255, 255)   # linhas pares ficam brancas
    estilo_cab = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=ROXO)
    with pdf.table(col_widths=larguras, text_align=alinhamentos, headings_style=estilo_cab,
                   cell_fill_color=LINHA, cell_fill_mode="ROWS", line_height=6.5,
                   borders_layout="HORIZONTAL_LINES", padding=1.5) as t:
        linha = t.row()
        for titulo_coluna in cabecalho:
            linha.cell(limpo(titulo_coluna))
        for valores in linhas:
            linha = t.row()
            for j in range(len(valores)):
                if j == coluna_situacao:
                    cor = CORES_SITUACAO[valores[j]]
                    linha.cell(limpo(valores[j]), style=FontFace(emphasis="BOLD", color=cor))
                else:
                    linha.cell(limpo(valores[j]))


def gerar(produtos, filtros, com_fila, com_pilha):
    pdf = RelatorioPDF(orientation="L", format="A4")
    pdf.gerado_em = datetime.now(BRASILIA).strftime("%d/%m/%Y às %H:%M")
    pdf.set_auto_page_break(True, margin=16)
    pdf.add_page()

    titulo(pdf, "Filtros aplicados")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*CINZA)
    for f in filtros:
        pdf.cell(0, 5.5, limpo("-  " + f), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    unidades = 0
    valor = 0
    criticos = 0
    for p in produtos:
        unidades = unidades + p[4]
        valor = valor + erp.valor_total(p)
        if p[4] < p[5]:
            criticos = criticos + 1
    cartoes(pdf, [["Produtos no relatório", str(len(produtos))], ["Unidades em estoque", str(unidades)],
                  ["Valor total em estoque", dinheiro(valor)], ["Abaixo do mínimo", str(criticos)]])

    titulo(pdf, "Produtos")
    if len(produtos) == 0:
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(*CINZA)
        pdf.cell(0, 8, "Nenhum produto atende aos filtros escolhidos.", new_x="LMARGIN", new_y="NEXT")
    else:
        linhas = []
        for p in produtos:
            linhas.append([str(p[0]), p[1], p[2], dinheiro(p[3]), str(p[4]), str(p[5]),
                           dinheiro(erp.valor_total(p)), erp.situacao(p)])
        tabela(pdf, ["Código", "Produto", "Categoria", "Preço", "Estoque", "Mínimo", "Valor total", "Situação"],
               linhas, (16, 60, 34, 28, 22, 22, 36, 40),
               ("CENTER", "LEFT", "LEFT", "RIGHT", "CENTER", "CENTER", "RIGHT", "LEFT"), coluna_situacao=7)

    if com_fila:
        titulo(pdf, "Reposições pendentes (mais urgente primeiro)")
        linhas = []
        posicao = 1
        for item in erp.ver_fila():
            p = item[1]
            linhas.append([f"{posicao}º", str(p[0]), p[1], str(p[4]), str(p[5]), str(item[0])])
            posicao = posicao + 1
        if len(linhas) == 0:
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 8, "Nenhum produto precisa de reposição.", new_x="LMARGIN", new_y="NEXT")
        else:
            tabela(pdf, ["Posição", "Código", "Produto", "Estoque", "Mínimo", "Faltam (un.)"], linhas,
                   (20, 20, 90, 30, 30, 40), ("CENTER", "CENTER", "LEFT", "CENTER", "CENTER", "CENTER"))

    if com_pilha:
        titulo(pdf, "Histórico de movimentações (mais recentes primeiro)")
        nomes = {"entrada": "Entrada", "saida": "Saída", "reposicao": "Reposição"}
        linhas = []
        for i in range(len(erp.historico) - 1, -1, -1):
            m = erp.historico[i]
            p = erp.buscar_produto(m[1])
            nome = "produto removido"
            if p != None:
                nome = p[1]
            topo = ""
            if i == len(erp.historico) - 1:
                topo = "Mais recente"
            linhas.append([topo, nomes[m[0]], str(m[1]), nome, str(m[2])])
        if len(linhas) == 0:
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 8, "Nenhuma movimentação registrada.", new_x="LMARGIN", new_y="NEXT")
        else:
            tabela(pdf, ["", "Tipo", "Código", "Produto", "Quantidade"], linhas,
                   (28, 30, 22, 90, 30), ("CENTER", "LEFT", "CENTER", "LEFT", "CENTER"))

    return bytes(pdf.output())
