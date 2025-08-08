# EDII - Implementação II - Árvores AVL
# Objetivo: Desenvolver uma simulação da estrutura de árvore AVL (autobalanceada), 
# implementando as operações principais: inserir(), deletar() e buscar(). 
# 
# O programa deve exibir as operações de forma gráfica.


# Importação das bibliotecas gráficas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
# Básicas
import time

# __init__ = construtor de inicialização da classe
# self == this

# Início Classe que representa o NÓ da Árvore
class NO_AVL:
    # A função é referente ao construtor, de maneira a definir e inicializar a própria classe
    def __init__(self, valor): 
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1
# Fim Classe NÓ AVL

# Início Classe que representa a própria Árvore-AVL
class ARVORE_AVL:

    # Funções de Balanceamento

    # Função que realiza a rotação à esquerda
    def rotacionar_esquerda(self, x):
        # Define "y" como o filho direito de "x", que será a nova raiz após a rotação
        y = x.direita

        # Armazena temporariamente o filho esquerdo de "y", que será reatribuído
        aux = y.esquerda

        # Torna "x" o filho esquerdo de "y", realizando a principal mudança estrutural da rotação
        y.esquerda = x

        # Reatribui o filho direito de "x" para o antigo filho esquerdo de "y" (salvo em "aux")
        x.direita = aux

        # Atualiza a altura de "x" com base na altura máxima entre seus filhos, mais 1
        x.altura = 1 + max(self.obter_altura(x.esquerda), self.obter_altura(x.direita))

        # Atualiza a altura de "y", que agora é o novo nó raiz
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))

        # Retorna "y" como a nova raiz da subárvore após a rotação
        return y

    # Função que realiza a rotação à direita
    def rotacionar_direita(self, x):        
        # Define "y" como o filho esquerdo de "x", que será a nova raiz após a rotação
        y = x.esquerda

        # Armazena temporariamente o filho direito de "y", que será reatribuído
        aux = y.direita

        # Torna "x" o filho direito de "y", realizando a principal mudança estrutural da rotação
        y.direita = x

        # Reatribui o filho esquerdo de "x" para o antigo filho direito de "y" (salvo em "aux")
        x.esquerda = aux

        # Atualiza a altura de "x" com base na altura máxima entre seus filhos, mais 1
        x.altura = 1 + max(self.obter_altura(x.esquerda), self.obter_altura(x.direita))

        # Atualiza a altura de "y", que agora é o novo nó raiz
        y.altura = 1 + max(self.obter_altura(y.esquerda), self.obter_altura(y.direita))

        # Retorna "y" como a nova raiz da subárvore após a rotação
        return y


    # Construtor que inicializa a árvore e possui um parâmetro de atualização para cada mudança
    def __init__(self, update_arvore=None, update_historico=None):
        self.raiz = None # Inicialmente a raiz é iniciada como "None"
        self.update_arvore = update_arvore  # Objeto que armazena as modificações e atualiza o gráfico
        self.update_historico = update_historico # Para registrar histórico

    # Funções Básicas e contidas na classe

    # Função de Inserção que recebe dois objetos, raiz e o valor desejado, sendo "self" o referenciador
    def inserir(self, raiz, valor):
        # Caso a raiz seja nula, cria um novo nó com o valor fornecido
        if not raiz:
            return NO_AVL(valor)

        # Insere recursivamente o valor na subárvore esquerda (se o valor for menor) ou direita (se maior) que a raiz
        if valor < raiz.valor:
            raiz.esquerda = self.inserir(raiz.esquerda, valor)
        else:
            raiz.direita = self.inserir(raiz.direita, valor)

        # Atualiza a altura do nó atual com base nos filhos
        raiz.altura = 1 + max(self.obter_altura(raiz.esquerda), self.obter_altura(raiz.direita))
        
        # Calcula o fator de balanceamento para o nó atual
        balanceamento = self.obter_balanceamento(raiz)

        # Atualiza o gráfico após a mudança
        if self.update_arvore:
            self.update_arvore() 

        # Rotação simples à direita, se desbalanceado para a esquerda
        if balanceamento > 1 and valor < raiz.esquerda.valor:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação simples à direita do nó {raiz.valor}")
                
            raiz = self.rotacionar_direita(raiz)

            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()

            return raiz

        # Rotação simples à esquerda, se desbalanceado para a direita
        if balanceamento < -1 and valor > raiz.direita.valor:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação simples à esquerda do nó {raiz.valor}")
        
            raiz = self.rotacionar_esquerda(raiz)

            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()

            return raiz

        # Rotação dupla (esquerda - direita), se desbalanceado para a esquerda
        if balanceamento > 1 and valor > raiz.esquerda.valor:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação dupla (Esquerda-Direita) sobre o nó: {raiz.valor}")

            # Realiza a sub-rotação esquerda
            raiz.esquerda = self.rotacionar_esquerda(raiz.esquerda)
            
            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()
                
            # Realiza a rotação direita
            raiz = self.rotacionar_direita(raiz)
            
            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()
            return raiz

        # Rotação dupla (direita - esquerda), se desbalanceado para a direita
        if balanceamento < -1 and valor < raiz.direita.valor:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação dupla (Direita-Esquerda) sobre o nó: {raiz.valor}")
                
            # Realiza a sub-rotação direita
            raiz.direita = self.rotacionar_direita(raiz.direita)
            
            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()  # Atualiza após a sub-rotação

            # Rotação esquerda
            raiz = self.rotacionar_esquerda(raiz)
            
            # Atualiza o gráfico após a mudança
            if self.update_arvore:
                self.update_arvore()
                
            return raiz
        # Fim Balanceamentos

        return raiz

    def remover(self, raiz, valor):
        # Caso o nó não for encontrado
        if not raiz:
            # Atualiza o histórico indicando que o valor não foi encontrado
            if self.update_historico:
                self.update_historico(f"Valor {valor} não encontrado para remoção!")
            return None # Retorna a raiz inalterada
 
        # Busca o valor a ser removido na subárvore esquerda, se o valor for menor que o atual
        if valor < raiz.valor:
            raiz.esquerda = self.remover(raiz.esquerda, valor)

        elif valor > raiz.valor: # Ou na direita, se o valor for maior que o atual
            raiz.direita = self.remover(raiz.direita, valor)
        
        else: # Contudo, se, o nó a ser removido foi encontrado
            
            # Caso 1: Nó com apenas um filho ou nenhum
            if not raiz.esquerda: # Se não houver subárvore esquerda
                return raiz.direita # Retorna a subárvore direita (ou None se não houver, como padrão)
            
            elif not raiz.direita: # se não houver subárvore direita
                return raiz.esquerda  # Retorna a subárvore esquerda

            # Caso 2: Nó com dois filhos
            # Encontra o menor valor da subárvore direita (substituto para o nó a ser removido)
            menor_valor = self.obter_minimo(raiz.direita)
            
            raiz.valor = menor_valor.valor # Substitui o valor do nó atual pelo sucessor mais próximo
            raiz.direita = self.remover(raiz.direita, menor_valor.valor) # Remove o nó sucessor na subárvore direita

        # Atualiza a altura do nó atual após a remoção
        raiz.altura = 1 + max(self.obter_altura(raiz.esquerda), self.obter_altura(raiz.direita))

        # Verifica o balanceamento do nó atual para determinar se é necessário algum ajuste na arvore
        balanceamento = self.obter_balanceamento(raiz)

        # Se caso for necessário:
        
        # Rotação simples à direita (desbalanceamento à esquerda)
        if balanceamento > 1 and self.obter_balanceamento(raiz.esquerda) > 0:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação simples à direita do nó: {raiz.valor}")
            
            # Realiza a rotação simples
            return self.rotacionar_direita(raiz)
        
        # Rotação dupla (esquerda - direita) (desbalanceamento à esquerda)
        if balanceamento > 1 and self.obter_balanceamento(raiz.esquerda) < 0:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação dupla (Esquerda-Direita) sobre o nó: {raiz.valor}")

            # Realiza a rotação esquerda na subárvore esquerda
            raiz.esquerda = self.rotacionar_esquerda(raiz.esquerda)
            
            # Realiza a rotação direita no nó atual
            return self.rotacionar_direita(raiz)
        
        # Rotação simples à esquerda (desbalanceamento à direita)
        if balanceamento < -1 and self.obter_balanceamento(raiz.direita) < 0:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação simples à esquerda do nó: {raiz.valor}")
            
            # Realiza a rotação simples
            return self.rotacionar_esquerda(raiz)
        
        # Rotação dupla (direita - esquerda) (desbalanceamento à direita)
        if balanceamento < -1 and self.obter_balanceamento(raiz.direita) > 0:
            
            # Atualiza o histórico
            if self.update_historico:
                self.update_historico(f"Rotação dupla (Direita-Esquerda) sobre o nó: {raiz.valor}")

            # Realiza a rotação direita na subárvore direita
            raiz.direita = self.rotacionar_direita(raiz.direita)
            
            # Realiza a rotação esquerda no nó atual
            return self.rotacionar_esquerda(raiz)

        # Fim Balanceamentos
            
        return raiz
        
    #Função de busca
    def buscar(self, raiz, valor):
        # Se a raiz for None, o valor não está presente na árvore, então False
        if raiz is None:
            return False
        
        # Se o valor do nó atual for igual ao valor buscado, retorna True
        if valor == raiz.valor:
            return True
    
        # Determina em qual lado da árvore a busca continuará
        if valor < raiz.valor:
            # Se o valor buscado é menor que o valor do nó atual, então busca na subárvore esquerda
            return self.buscar(raiz.esquerda, valor)
        else:
            # Senão, o valor buscado é maior que o valor do nó atual, então busca na subárvore direita
            return self.buscar(raiz.direita, valor)
        
    
    # Função auxiliar para encontrar o menor valor na subárvore
    def obter_minimo(self, raiz):
        # Começa pelo nó recebido (raiz da subárvore)
        atual = raiz
        
        # Percorre para a esquerda enquanto existirem nós válidos
        # (Se espera que o menor valor estará na extremidade esquerda da subárvore)
        while atual.esquerda is not None:
            atual = atual.esquerda
            
        # Retorna o nó com o menor valor encontrado
        return atual
    
    # Função auxiliar para obter a altura de um nó
    def obter_altura(self, raiz):
        # Retorna a altura do nó (1), ou (0) se o nó for None (vazio)
        return raiz.altura if raiz else 0

    # Função auxiliar para calcular o fator de balanceamento de um nó
    def obter_balanceamento(self, raiz):
        # O fator de balanceamento é a diferença entre as alturas das subárvores esquerda e direita 
        # Retorna (0) se o nó for None.
        return self.obter_altura(raiz.esquerda) - self.obter_altura(raiz.direita) if raiz else 0

# Fim classe AVL    

# Função que ilustra a Árvore-AVL graficamente, sempre mantendo na última instância
def ilustrar_Arvore_AVL(novo_no, x=0, y=0, distancia=1, objeto=None, nivel=1):
    # Se o nó atual for None (não existe), a função simplesmente retorna
    if not novo_no: 
        return

    # plot(): Cria gráficos bidimensionais
    # 'k-' : É uma característica da linha

    # Se existir um nó à esquerda
    if novo_no.esquerda:
        # Desenha uma linha conectando o nó atual ao seu filho esquerdo
        objeto.plot([x, x - distancia], [y, y - 1], 'k-')
        
        # Chama recursivamente a função para desenhar o filho esquerdo
        # Atualiza as coordenadas (x, y) e divide a distância para o próximo nível
        ilustrar_Arvore_AVL(novo_no.esquerda, x - distancia, y - 1, distancia / 2, objeto, nivel + 1)

    # Se existir um nó à direita
    if novo_no.direita:
        # Desenha uma linha conectando o nó atual ao seu filho direito
        objeto.plot([x, x + distancia], [y, y - 1], 'k-')
        # Chama recursivamente a função para desenhar o filho direito
        # Atualiza as coordenadas (x, y) e divide a distância para o próximo nível
        ilustrar_Arvore_AVL(novo_no.direita, x + distancia, y - 1, distancia / 2, objeto, nivel + 1)

    # Adiciona o valor do nó atual no gráfico como texto, alguns atributos são:
    # "size" : Define o tamanho do texto
    # "ha"`: Define o posicionamento
    # "bbox": Configura o estilo da "Bolinha" ao redor do texto
    objeto.text(x, y, str(novo_no.valor), size=12, ha='center', bbox=dict(boxstyle='circle', facecolor='white', edgecolor='black'))

# Início Classe para a interface
class INTERFACE_ARVORE_AVL:

    # Função responsável por atualizar a representação gráfica da Árvore-AVL
    def atualizar_AVL(self):
        # Limpa o gráfico atual, removendo qualquer desenho ou marcações anteriores
        self.eixo.clear()
        # Remove os eixos do gráfico para que fique visualmente mais limpo
        self.eixo.axis('off')

        # Desenha a árvore AVL atual no gráfico, começando pela raiz
        ilustrar_Arvore_AVL(self.raiz, objeto=self.eixo)

        # "Canvas" é conceito que define o que realiza a ligação entre gráfico e interface
        # Enquanto o método draw atualiza o desenho no canvas com o estado mais recente
        self.desenho.draw()
        
        # Atualiza a janela para refletir as mudanças feitas no gráfico
        self.janela.update()

        time.sleep(0.5)  # Pausa para criar o efeito de transição e suavização 

    # Função responsável por atualizar o histórico de operações feitas
    def atualizar_historico(self, mensagem):
        # Permite que o conteúdo do histórico seja editado pela função configure
        self.historico.configure(state=tk.NORMAL)
        
        # Insere a nova mensagem no final do histórico, adicionando uma quebra de linha ao final
        self.historico.insert(tk.END, mensagem + "\n")
        
        # Bloqueia a edição do histórico após a inserção da nova mensagem
        self.historico.configure(state=tk.DISABLED)
        
        # Garante que a última linha do histórico seja sempre visível, rolando até o final
        self.historico.see(tk.END)
        
    # Função que insere valores, atuando na camada mais mais alta (próxima ao usuário)
    def inserir_valor(self):
        try:
            # Tenta converter o valor inserido no campo de entrada para inteiro
            valor = int(self.entrada.get())
            
            # Chama a função de inserção na árvore AVL e atualiza a raiz com o novo nó
            self.raiz = self.arvore.inserir(self.raiz, valor)
            
            # Atualiza o histórico registrando a operação de inserção
            self.atualizar_historico(f"Inserção do valor: {valor}")
            
            # Atualiza o gráfico após a mudança
            self.atualizar_AVL()
            
        except ValueError:  # Se ocorrer um erro de conversão (Caso o valor não seja um inteiro)
            # Registra no histórico a tentativa de inserção inválida
            self.atualizar_historico("Tentativa de entrada inválida!")
            
            pass # Retorna silenciosamente sem realizar nenhuma ação adicional
    
    # Função que remove valores, atuando na camada mais alta (próxima ao usuário)
    def remover_valor(self):
        try:
            # Tenta converter o valor inserido no campo de entrada para inteiro
            valor = int(self.entrada.get())
            
            # Verifica se o valor existe antes de tentar removê-lo
            if not self.arvore.buscar(self.raiz, valor):
                self.atualizar_historico(f"Valor {valor} não encontrado para remoção.")
                return  # Retorna sem fazer nada se o valor não for encontrado

            # Tenta remover o valor da árvore, atualizando a raiz da árvore
            self.raiz = self.arvore.remover(self.raiz, valor)
            
            # Verifica se o valor ainda está presente após a remoção
            if self.arvore.buscar(self.raiz, valor):
                # Caso o valor ainda exista, registra um erro no histórico
                self.atualizar_historico(f"Erro: Não foi possível remover o valor {valor}.")
            else:
                # Senão, confirma a remoção no histórico e atualiza a árvore
                self.atualizar_historico(f"Remoção do valor {valor} concluída.")
                self.atualizar_AVL()
        
        except ValueError: # Caso a entrada seja inválida, registra no histórico
            self.atualizar_historico("Tentativa de remoção inválida!")
            
            pass  # Retorno silencioso para entradas inválidas
    
    # Função que busca valores, atuando na camada mais alta (próxima ao usuário)
    def buscar_valor(self):
        try:
            # Tenta converter o valor inserido no campo de entrada para inteiro
            valor = int(self.entrada.get())
            
            # Realiza a busca do valor na árvore chamando a função de busca
            isEncontrado = self.arvore.buscar(self.raiz, valor)
            
            if isEncontrado:
                # Se o valor for encontrado, registra no histórico que o valor foi encontrado
                self.atualizar_historico(f"valor: {valor} encontrado na árvore")
            else:
                # Senão, que o valor não foi encontrado
                self.atualizar_historico(f"Valor Não encontrado na árvore")
            
        except ValueError: # Se houver alguma entrada inválida
            # Registra que houve uma tentativa de busca inválida no histórico
            self.atualizar_historico("Tentativa de busca inválida!")
            
            pass # Retorno silencioso para entradas inválidas
            
    # Função responsável por manter a janela gráfica da aplicação em execução contínua (Loop)
    def rodar(self):
        # Inicia o loop contínuo da janela, mantendo a interface gráfica em execução
        self.janela.mainloop()

    # Fim funções essenciais

    # Início das chamadas de conteúdo da interface (Janela Principal)
    def __init__(self):
        # Criação da janela principal da aplicação usando Tkinter
        self.janela = tk.Tk()   # Cria a janela principal, associando-a ao atributo "janela"
        self.janela.title("Simulação - Árvore AVL")  # Define o título da janela

        # "pack()": Adiciona e Atualiza o que for criado/inserido
        
        # Criação do bloco (frame) que armazenará o gráfico da árvore
        self.bloco_retangulo = tk.Frame(self.janela)  # Cria um container 'Frame' que será usado para exibir o gráfico da árvore
        self.bloco_retangulo.pack() # Adiciona o 'Frame' à janela, fazendo com que ele seja exibido na interface

        # Criação do bloco para os controles da interface (entrada de dados e botões em geral)
        self.bloco_de_controle = tk.Frame(self.janela)   # Cria um container 'Frame' para os controles como botões e campo de entrada
        self.bloco_de_controle.pack() # Adiciona o 'Frame' à janela para que os controles sejam visíveis

        # Criação do gráfico para exibir a árvore usando Matplotlib
        self.bolinha, self.eixo = plt.subplots(figsize=(8, 6)) # Cria uma figura para o gráfico (tamanho 8x6 em polegadas) por padrão
        self.eixo.axis('off')  # Desativa os eixos para tornar o gráfico mais limpo (sem linhas de coordenadas)

        # Criação do "Canvas" (área dos desenhos) que integrará o gráfico à interface Tkinter
        self.desenho = FigureCanvasTkAgg(self.bolinha, master=self.bloco_retangulo) # Vincula o gráfico ao 'Frame' para ser mostrado na interface
        self.desenho.get_tk_widget().pack()  # Exibe o widget no layout, tornando o gráfico visível na tela

        # Criação do campo de entrada para o usuário inserir um valor
        self.entrada = tk.Entry(self.bloco_de_controle) # Cria um campo de texto onde o usuário pode digitar um valor
        self.entrada.pack(side=tk.LEFT) # Posiciona o campo de entrada à esquerda dentro do 'Frame' de controles

        # Criação do botão para inserir o valor digitado na árvore
        self.botao_de_inserir = tk.Button(self.bloco_de_controle, text="Inserir", command=self.inserir_valor) # Botão que chama a função de inserção ao ser clicado
        self.botao_de_inserir.pack(side=tk.LEFT) # Posiciona o botão à esquerda dentro do 'Frame' de controles
        
        # Criação do botão para remover um valor da árvore
        self.botao_de_remover = tk.Button(self.bloco_de_controle, text="Remover", command=self.remover_valor) # Botão que chama a função de remoção ao ser clicado
        self.botao_de_remover.pack(side=tk.LEFT) # Posiciona o botão à esquerda dentro do 'Frame' de controles
        
        # Criação de um campo de texto para exibir o histórico das operações realizadas na árvore
        self.historico = tk.Text(self.janela, height=10, state=tk.DISABLED, wrap=tk.WORD) # Cria um campo de texto desativado (não editável) para mostrar mensagens de histórico
        self.historico.pack(fill=tk.BOTH, expand=True) # Exibe o campo de histórico na interface, permitindo que ocupe o espaço restante
        
        # Criação do botão de busca, que chama a função de busca ao ser pressionado
        self.botao_de_busca = tk.Button(self.bloco_de_controle, text="buscar", command=self.buscar_valor) # Botão de busca
        self.botao_de_busca.pack(side=tk.LEFT) # Posiciona o botão à esquerda dentro do 'Frame' de controles
        
        # Inicialização da árvore AVL 
        # Cria a árvore AVL, passando funções de atualização do gráfico e do histórico
        self.arvore = ARVORE_AVL(update_arvore=self.atualizar_AVL, update_historico=self.atualizar_historico)
        self.raiz = None  # Inicializa a raiz da árvore como None, indicando que a árvore começa vazia
        
# Fim Classe da interface

# Chamada para a execução principal
if __name__ == "__main__":
    # Cria uma instância da classe INTERFACE_ARVORE_AVL
    programa = INTERFACE_ARVORE_AVL()
   
    # Chama o método 'rodar()' que inicia o loop principal da interface gráfica
    programa.rodar()