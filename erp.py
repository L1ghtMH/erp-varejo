# Este arquivo e o SISTEMA (estruturas de dados + algoritmos).
# O app.py e so a TELA (interface grafica) que chama estas funcoes.


# ================= ESTRUTURAS DE DADOS =================

# LISTA de cadastro. Cada produto e [codigo, nome, categoria, preco, estoque, minimo]
produtos = []

# LISTA de cadastro. Cada fornecedor e [codigo, nome, telefone]
fornecedores = []

# PILHA de movimentacoes. Cada item e [tipo, codigo, quantidade]
# So usamos append() (empilhar no topo) e pop() (desempilhar do topo): O(1).
historico = []

# FILA DE PRIORIDADE de reposicao. Cada item e [prioridade, codigo]
# Fica ORDENADA da menor para a maior prioridade.
# A MAIOR prioridade fica no FIM, entao atender e so um pop(): O(1).
fila_prioridade = []


# ================= ALGORITMOS =================

def busca_linear(lista, codigo):
    # Olha registro por registro, do primeiro ao ultimo, comparando o codigo.
    # Devolve a POSICAO (indice) do registro, ou -1 se nao achar.
    # Melhor caso O(1): e o primeiro da lista.
    # Pior caso O(n): e o ultimo ou nao existe.
    for i in range(len(lista)):
        if lista[i][0] == codigo:
            return i
    return -1


def busca_linear_por_nome(texto):
    # Mesma ideia, mas compara o nome e guarda TODOS que contem o texto.
    # Aqui sempre percorre a lista toda: O(n).
    texto = texto.strip().lower()
    encontrados = []
    for produto in produtos:
        if texto in produto[1].lower():
            encontrados.append(produto)
    return encontrados


def valor_total(produto):
    return produto[3] * produto[4]


def chave_ordenacao(produto, criterio):
    if criterio == "estoque":
        return produto[4]
    return valor_total(produto)


def bubble_sort(criterio):
    # Ordena do MAIOR para o MENOR, numa COPIA da lista (o cadastro original nao muda).
    # Compara vizinhos e troca se estiverem fora de ordem; repete ate nao haver trocas.
    # Melhor caso O(n): lista ja ordenada, nenhuma troca, para na 1a passada.
    # Pior caso O(n^2): dois lacos aninhados.
    copia = list(produtos)
    n = len(copia)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            if chave_ordenacao(copia[j], criterio) < chave_ordenacao(copia[j + 1], criterio):
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                trocou = True
        if not trocou:
            break
    return copia


# ================= PRODUTOS (CRUD) =================

def buscar_produto(codigo):
    i = busca_linear(produtos, codigo)
    if i == -1:
        return None
    return produtos[i]


def cadastrar_produto(codigo, nome, categoria, preco, estoque, minimo):
    if buscar_produto(codigo) != None:
        return "Produto já cadastrado."
    if nome.strip() == "" or categoria.strip() == "":
        return "Nome e categoria são obrigatórios."
    if preco < 0 or estoque < 0 or minimo < 0:
        return "Preço, estoque e mínimo não podem ser negativos."

    produto = [codigo, nome.strip(), categoria.strip(), preco, estoque, minimo]
    produtos.append(produto)
    atualizar_fila(produto)
    return "Produto cadastrado."


def alterar_produto(codigo, nome, categoria, preco, estoque, minimo):
    produto = buscar_produto(codigo)
    if produto == None:
        return "Produto não encontrado."
    if preco < 0 or estoque < 0 or minimo < 0:
        return "Preço, estoque e mínimo não podem ser negativos."

    if nome.strip() != "":
        produto[1] = nome.strip()
    if categoria.strip() != "":
        produto[2] = categoria.strip()
    produto[3] = preco
    produto[4] = estoque
    produto[5] = minimo

    atualizar_fila(produto)
    return "Produto alterado."


def remover_produto(codigo):
    i = busca_linear(produtos, codigo)
    if i == -1:
        return "Produto não encontrado."
    produtos.pop(i)
    tirar_da_fila(codigo)
    return "Produto removido."


def filtrar_por_categoria(categoria):
    # Filtro: percorre a lista toda (O(n)) e guarda quem e da categoria.
    categoria = categoria.strip().lower()
    encontrados = []
    for produto in produtos:
        if produto[2].lower() == categoria:
            encontrados.append(produto)
    return encontrados


def situacao(produto):
    if produto[4] == 0:
        return "Zerado"
    if produto[4] < produto[5]:
        return "Abaixo do mínimo"
    return "OK"


def filtrar_produtos(lista, categorias, situacoes, preco_min, preco_max, texto):
    # Filtro com varios criterios ao mesmo tempo (usado no relatorio em PDF).
    # Percorre a lista uma vez (O(n)) e so guarda quem passa em TODOS os criterios.
    texto = texto.strip().lower()
    resultado = []
    for produto in lista:
        ok_categoria = produto[2] in categorias
        ok_situacao = situacao(produto) in situacoes
        ok_preco = produto[3] >= preco_min and produto[3] <= preco_max
        ok_nome = texto in produto[1].lower()
        if ok_categoria and ok_situacao and ok_preco and ok_nome:
            resultado.append(produto)
    return resultado


def listar_categorias():
    categorias = []
    for produto in produtos:
        if produto[2] not in categorias:
            categorias.append(produto[2])
    return categorias


# ================= FORNECEDORES (CRUD) =================

def buscar_fornecedor(codigo):
    i = busca_linear(fornecedores, codigo)
    if i == -1:
        return None
    return fornecedores[i]


def cadastrar_fornecedor(codigo, nome, telefone):
    if buscar_fornecedor(codigo) != None:
        return "Fornecedor já cadastrado."
    if nome.strip() == "":
        return "Nome é obrigatório."

    fornecedores.append([codigo, nome.strip(), telefone.strip()])
    return "Fornecedor cadastrado."


def alterar_fornecedor(codigo, nome, telefone):
    fornecedor = buscar_fornecedor(codigo)
    if fornecedor == None:
        return "Fornecedor não encontrado."

    if nome.strip() != "":
        fornecedor[1] = nome.strip()
    if telefone.strip() != "":
        fornecedor[2] = telefone.strip()
    return "Fornecedor alterado."


def remover_fornecedor(codigo):
    i = busca_linear(fornecedores, codigo)
    if i == -1:
        return "Fornecedor não encontrado."
    fornecedores.pop(i)
    return "Fornecedor removido."


# ================= ESTOQUE (PILHA) =================

def registrar_movimentacao(tipo, codigo, quantidade):
    historico.append([tipo, codigo, quantidade])   # push: O(1)


def entrada_estoque(codigo, quantidade):
    produto = buscar_produto(codigo)
    if produto == None:
        return "Produto não encontrado."
    if quantidade <= 0:
        return "Quantidade inválida."

    produto[4] = produto[4] + quantidade
    registrar_movimentacao("entrada", codigo, quantidade)
    atualizar_fila(produto)
    return "Entrada registrada."


def saida_estoque(codigo, quantidade):
    produto = buscar_produto(codigo)
    if produto == None:
        return "Produto não encontrado."
    if quantidade <= 0:
        return "Quantidade inválida."
    if quantidade > produto[4]:
        return "Estoque insuficiente."

    produto[4] = produto[4] - quantidade
    registrar_movimentacao("saida", codigo, quantidade)
    atualizar_fila(produto)
    return "Saída registrada."


def desfazer_movimentacao():
    if len(historico) == 0:
        return "Nenhuma movimentação para desfazer."

    movimento = historico[-1]   # peek: olha o topo sem tirar
    tipo = movimento[0]
    codigo = movimento[1]
    quantidade = movimento[2]
    produto = buscar_produto(codigo)

    if produto != None and tipo != "saida" and produto[4] < quantidade:
        return "Não dá para desfazer: o estoque ficaria negativo."

    historico.pop()   # pop: O(1)

    if produto == None:
        return "Movimentação descartada: o produto foi removido."

    if tipo == "saida":
        produto[4] = produto[4] + quantidade
    else:   # entrada ou reposicao
        produto[4] = produto[4] - quantidade

    atualizar_fila(produto)
    return f"Desfeita a última movimentação: {tipo} de {quantidade} un. de {produto[1]}."


# ================= FILA DE PRIORIDADE =================

def tirar_da_fila(codigo):
    # Percorre a fila e tira o produto, se ele estiver nela. O(n)
    for item in fila_prioridade:
        if item[1] == codigo:
            fila_prioridade.remove(item)
            return


def inserir_por_prioridade(item):
    # Anda ate achar uma prioridade maior ou igual e insere antes dela.
    # Assim a fila continua ordenada e a maior prioridade fica sempre no fim. O(n)
    i = 0
    while i < len(fila_prioridade) and fila_prioridade[i][0] < item[0]:
        i = i + 1
    fila_prioridade.insert(i, item)


def atualizar_fila(produto):
    # So o produto que mudou e atualizado, e ele entra ja na posicao certa
    # (fila sempre ordenada), sem refazer a fila nem procurar o maior toda vez.
    tirar_da_fila(produto[0])
    if produto[4] < produto[5]:
        prioridade = produto[5] - produto[4]   # quanto falta para o minimo
        inserir_por_prioridade([prioridade, produto[0]])


def ver_fila():
    # Devolve a fila da MAIOR para a menor prioridade (percorre de tras para frente).
    resultado = []
    for i in range(len(fila_prioridade) - 1, -1, -1):
        item = fila_prioridade[i]
        resultado.append([item[0], buscar_produto(item[1])])
    return resultado


def atender_reposicao():
    if len(fila_prioridade) == 0:
        return "Nenhuma reposição pendente."

    item = fila_prioridade.pop()   # maior prioridade esta no fim: O(1)
    quantidade = item[0]
    produto = buscar_produto(item[1])

    produto[4] = produto[4] + quantidade   # repoe ate o estoque minimo
    registrar_movimentacao("reposicao", produto[0], quantidade)
    return f"Reposição atendida: {produto[1]} recebeu {quantidade} unidades."


# ================= DADOS DE EXEMPLO =================

def carregar_exemplos():
    cadastrar_produto(101, "Arroz 5kg", "Alimentos", 27.90, 40, 20)
    cadastrar_produto(102, "Feijão 1kg", "Alimentos", 8.50, 5, 15)
    cadastrar_produto(103, "Café 500g", "Alimentos", 19.90, 8, 10)
    cadastrar_produto(104, "Açúcar 1kg", "Alimentos", 4.79, 32, 15)
    cadastrar_produto(201, "Detergente", "Limpeza", 2.99, 2, 10)
    cadastrar_produto(202, "Sabão em pó", "Limpeza", 15.49, 25, 10)
    cadastrar_produto(203, "Água sanitária", "Limpeza", 5.20, 0, 8)
    cadastrar_produto(301, "Refrigerante 2L", "Bebidas", 9.99, 60, 24)
    cadastrar_produto(302, "Suco de uva 1L", "Bebidas", 12.90, 14, 12)
    cadastrar_fornecedor(1, "Distribuidora Nordeste", "(79) 3211-0000")
    cadastrar_fornecedor(2, "Atacadão Limpeza", "(79) 3222-1111")
    cadastrar_fornecedor(3, "Bebidas Sergipe", "(79) 3233-2222")
    entrada_estoque(101, 10)
    saida_estoque(301, 6)


carregar_exemplos()
