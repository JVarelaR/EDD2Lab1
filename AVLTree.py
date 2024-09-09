from typing import Any, Optional, Tuple
import networkx as nx, matplotlib.pyplot as plt,tkinter as tk,numpy as np,csv
from tkinter import messagebox, scrolledtext
import random


class Node:

    def __init__(self, data: Any,year: int,worldwideEarnings: float,domesticEarnings: float, foreignEarnings: float, domesticPercentEarnings: float, foreignPercentEarnings: float) -> None:
        self.data = data
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.year=year
        self.worldwideEarnings=worldwideEarnings
        self.domesticEarnings=domesticEarnings
        self.foreignEarnings=foreignEarnings
        self.domesticPercentEarnings=domesticPercentEarnings
        self.foreignPercentEarnings=foreignPercentEarnings

class BinaryTree:

    def __init__(self, root: Optional["Node"] = None) -> None:
        self.root = root

    def conditional_search(self,year: int, foreignEarnings: float) -> list: #Busqueda condicional que devuelve una lista de las coincidencias encontradas
        coincidences=[]
        s = []
        p = self.root
        while p is not None or len(s) > 0:
            if p is not None:
                if p.year==year and p.domesticPercentEarnings<p.foreignPercentEarnings and p.foreignEarnings >= foreignEarnings:
                    coincidences.append(p)
                s.append(p)
                p = p.left
            else:
                p = s.pop()
                p = p.right
        return coincidences

    def preorder(self) -> None:
        self.__preorder_r(self.root)
        print()

    def __preorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            print(node.data, end = ' ')
            self.__preorder_r(node.left)
            self.__preorder_r(node.right)

    def preorder_nr(self) -> None:
        s = []
        p = self.root
        while p is not None or len(s) > 0:
            if p is not None:
                print(p.data, end = ' ')
                s.append(p)
                p = p.left
            else:
                p = s.pop()
                p = p.right
        print()

    def inorder(self) -> None:
        self.__inorder_r(self.root)
        print()

    def __inorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__inorder_r(node.left)
            print(node.data, end = '\t')
            self.__inorder_r(node.right)

    def inorder_nr(self) -> None:
        s = []
        p = self.root
        while p is not None or len(s) > 0:
            if p is not None:
                s.append(p)
                p = p.left
            else:
                p = s.pop()
                print(p.data, end = ' ')
                p = p.right
        print()

    def postorder(self) -> None:
        self.__postorder_r(self.root)
        print()

    def __postorder_r(self, node: Optional["Node"]) -> None:
        if node is not None:
            self.__postorder_r(node.left)
            self.__postorder_r(node.right)
            print(node.data, end = ' ')

    def levels_nr(self) -> None:
        q = []
        p = self.root
        q.append(p)
        while len(q) > 0:
            p = q.pop(0)
            print(p.data, end = ' ')
            if p.left is not None:
                q.append(p.left)
            if p.right is not None:
                q.append(p.right)
        print()
    
    def level_nodes(self,node: Optional["Node"], level: int) ->str: # Función para obtener todos los nodos en un nivel dado
        if node is None:
            return ""
        if level == 0:
            return "\t'"+node.data + "'\t"
        elif level > 0:
            left_values = self.level_nodes(node.left, level - 1)
            right_values = self.level_nodes(node.right, level - 1)
            return left_values + right_values

    def levels_r(self): # Función para realizar el recorrido por niveles recursivamente
        node=self.root
        h = self.height()
        result = ""
        for i in range(0, h):
            result += str(i)+": "+self.level_nodes(node, i)+"\n"
        return result.strip()

    def nodes_and_edges(self) -> Tuple[Optional["list"], Optional["list"]]:
        nodes = []
        edges = []
        node=self.root
        def dfs(nodo: Optional["Node"]):
            if nodo is None:
                return
            if not nodo in nodes:
                nodes.append(nodo.data) #Si el nodo existe se agrega a la lista de nodos

            if nodo.left:
                if not (nodo.data, nodo.left.data) in edges:
                    edges.append((nodo.data, nodo.left.data))  # Si existe un nodo izquierdo se agrega el enlace izquierdo a la lista de enlaces
                dfs(nodo.left)

            if nodo.right:
                if not (nodo.data, nodo.right.data) in edges:
                    edges.append((nodo.data, nodo.right.data))  # Si existe un nodo derecho se agrega el enlace derecho a la lista de enlaces
                dfs(nodo.right)
        dfs(node)
        return nodes, edges

    def print_tree(self):
        if plt.show:
            plt.close()
        G=nx.Graph()
        nodes, edges = self.nodes_and_edges()
        G.add_nodes_from(nodes) #Cada nodo de la lista se agrega al arbol
        for e in edges:
            G.add_edge(e[0],e[1]) #Cada enlace de la lista se agrega al arbol
        
        positions = nx.circular_layout(G)
        self.assign_positions(self.root,0,0,1,positions)

        nx.draw(G,pos=positions, with_labels=True)
        plt.margins(0.2)
        plt.show()

    def assign_positions(self,node: Node,x: int, y: int, distancia: int,positions: list):
        if node is None:
            return 

        # Se asignan coordenadas al nodo actual
        positions[node.data] = np.array([x,y])

        # Se asignan coordenadas al hijo izquierdo
        self.assign_positions(node.left, x - distancia, y - 2, distancia / 2,positions)

        # Se asignan coordenadas al hijo derecho
        self.assign_positions(node.right, x + distancia, y - 2, distancia / 2,positions)

    def height(self) -> int:
        return self.__height_r(self.root)

    def __height_r(self, node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return 1 + max(self.__height_r(node.left), self.__height_r(node.right))
    
    def balance(self,node: "Node") -> int:
        if node is None:
            return 0
        return self.__height_r(node.right)-self.__height_r(node.left)

    @staticmethod
    def generate_sample_tree() -> "BinaryTree":
        T = BinaryTree(Node('A'))
        T.root.left = Node('B')
        T.root.right = Node('C')
        T.root.left.left = Node('D')
        T.root.left.right = Node('E')
        T.root.right.right = Node('F')
        T.root.left.left.left = Node('G')
        T.root.left.left.right = Node('H')
        T.root.right.right.left = Node('I')
        T.root.right.right.right = Node('J')
        T.root.left.left.right.left = Node('K')

        return T
    
class BST(BinaryTree):

    def __init__(self, root: Optional["Node"] = None) -> None:
        super().__init__(root)

    def search(self, data: Any) -> Tuple[Optional["Node"], Optional["Node"]]:
        p, pad = self.root, None
        while p is not None:
            if data == p.data:
                return p, pad
            else:
                pad = p
                if data < p.data:
                    p = p.left
                else:
                    p = p.right
        return p, pad

    def insert(self, data: Any) -> bool:
        to_insert = Node(data)
        if self.root is None:
            self.root = to_insert
            return True
        else:
            p, pad = self.search(data)
            if p is not None:
                return False
            else:
                if data < pad.data:
                    pad.left = to_insert
                else:
                    pad.right = to_insert
                return True

    def delete(self, data: Any, mode: bool = True) -> bool:
        p, pad = self.search(data)
        if p is not None:
            if p.left is None and p.right is None:
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                del p
            elif p.left is None and p.right is not None:
                if p == pad.left:
                    pad.left = p.right
                else:
                    pad.right = p.right
                del p
            elif p.left is not None and p.right is None:
                if p == pad.left:
                    pad.left = p.left
                else:
                    pad.right = p.left
                del p
            else:
                if mode:
                    pred, pad_pred, son_pred = self.__pred(p)
                    p.data = pred.data
                    if p == pad_pred:
                        pad_pred.left = son_pred
                    else:
                        pad_pred.right = son_pred
                    del pred
                else:
                    sus, pad_sus, son_sus = self.__sus(p)
                    p.data = sus.data
                    if p == pad_sus:
                        pad_sus.right = son_sus
                    else:
                        pad_sus.left = son_sus
                    del sus
            return True
        return False

    def pred(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.left, node
        while p.right is not None:
            p, pad = p.right, p
        return p, pad, p.left

    def sus(self, node: "Node") -> Tuple["Node", "Node", Optional["Node"]]:
        p, pad = node.right, node
        while p.left is not None:
            p, pad = p.left, p
        return p, pad, p.right
    
    def node_level(self,node: Node) -> int: #El nivel del nodo se encuentra hallando la distancia que se recorre desde la raiz del arbol hasta el nodo
        level=0
        p=self.root
        while p is not None:
            if p==node:
                return level
            else:
                if node.data<p.data:
                    p=p.left
                else:
                    p=p.right
            level+=1

    def node_dad(self,node: Node) -> Optional["Node"]:
        p,pad=self.search(node.data) #Para obtener al padre de un nodo se usa nodo retornado por el algoritmo de busqueda
        return pad

    def node_granddad(self,node: Node) -> Optional["Node"]:
        dad=self.node_dad(node) #Para obtener al abuelo de un nodo primero se obtiene al padre
        if dad is not None:
            return self.node_dad(dad)#Luego se obtiene al padre del padre, el cual es el abuelo
        return None
    
    def node_uncle(self,node: Node) -> Optional["Node"]:
        granddad=self.node_granddad(node)
        dad=self.node_dad(node)
        if dad is None:
            return None
        if granddad is None:
            return None
        if dad==granddad.left:
            return granddad.right
        else:
            return granddad.left

class AVLT(BST):
    def __init__(self, root: Optional["Node"] = None) -> None:
        super().__init__(root)
    
    def insert(self, node: Node) -> bool: #Insercion con autobalanceo
        to_insert = node
        data=node.data
        if self.root is None:
            self.root = to_insert
            return True
        else:
            p, pad = self.search(data)
            if p is not None:
                return False
            else:
                if data < pad.data:
                    pad.left = to_insert
                else:
                    pad.right = to_insert

                p=to_insert
                self.check_balance(pad)
                return True
            

    def delete(self, data: Any, mode: bool = True) -> bool: #Eliminacion con autobalanceo
        p, pad = self.search(data)
        if p is not None:
            if p.left is None and p.right is None:
                if p==self.root:
                    self.root=None
                if p == pad.left:
                    pad.left = None
                else:
                    pad.right = None
                
            elif p.left is None and p.right is not None:
                if p == pad.left:
                    pad.left = p.right
                else:
                    pad.right = p.right
                
            elif p.left is not None and p.right is None:
                if p == pad.left:
                    pad.left = p.left
                else:
                    pad.right = p.left
                
            else:
                if mode:
                    pred, pad_pred, son_pred = self.pred(p)
                    p.data = pred.data
                    if p == pad_pred:
                        pad_pred.left = son_pred
                    else:
                        pad_pred.right = son_pred
                    del pred
                else:
                    sus, pad_sus, son_sus = self.sus(p)
                    p.data = sus.data
                    if p == pad_sus:
                        pad_sus.right = son_sus
                    else:
                        pad_sus.left = son_sus
                    del sus
            
            # Chequeo del balance después de eliminar el nodo
            if p == self.root:
                self.check_balance(self.root)
            else:
                self.check_balance(pad)
            return True
        return False

    def check_balance(self, node: "Node"):
        while node is not None:
            balanceFactor = self.balance(node)

            # Rotación a la izquierda si el árbol está desequilibrado a la derecha
            if balanceFactor == 2:
                if self.balance(node.right)==-1:
                    node=self.double_right_left_rotation(node)#Caso(2,-1)
                else: 
                    node = self.simple_left_rotation(node)#Caso(2,0) y (2,1)

            # Rotación a la derecha si el árbol está desequilibrado a la izquierda
            elif balanceFactor == -2:
                if self.balance(node.left)==1:
                    node = self.double_left_right_rotation(node) #Caso(-2,1)
                else: 
                    node = self.simple_right_rotation(node)#Caso(-2,0) y (-2,-1)
                    

            # Subir un nivel en el árbol para verificar el balance del padre
            if node == self.root:
               break
            node = self.node_dad(node)


    def simple_left_rotation(self, node: "Node") -> Node:
        aux = node.right
        node.right = aux.left
        aux.left = node
        if node == self.root:
            self.root = aux
        else:
            pad = self.node_dad(node)
            if pad.left == node:
                pad.left = aux
            else:
                pad.right = aux
        return aux
    
    def simple_right_rotation(self, node: "Node") -> Node:
        aux = node.left
        node.left = aux.right
        aux.right = node
        if node == self.root:
            self.root = aux
        else:
            pad = self.node_dad(node)
            if pad.left == node:
                pad.left = aux
            else:
                pad.right = aux
        return aux
    
    def double_right_left_rotation(self, node: "Node") -> Node:
        node.right = self.simple_right_rotation(node.right)
        return self.simple_left_rotation(node)
    
    def double_left_right_rotation(self, node: "Node") -> Node:
        node.left = self.simple_left_rotation(node.left)
        return self.simple_right_rotation(node)




#Arbol De Ejemplo
arbol=AVLT()



#Lectura del dataset
with open("dataset_movies.csv",newline='') as f:
    data = csv.reader(f,delimiter=',')
    movies = list(data)

"""
for i in range(30):    #Se escogen elementos aleatorios de la lista de peliculas
    while True:
        e=random.randint(1,len(movies)-1)
        if arbol.insert(Node(data=movies[e][0],
                          year=int(movies[e][6]),
                          worldwideEarnings=float(movies[e][1]),
                          domesticEarnings=float(movies[e][2]),
                          foreignEarnings=float(movies[e][4]),
                          domesticPercentEarnings=float(movies[e][3]),
                          foreignPercentEarnings=float(movies[e][5]))):
            arbol.print_tree()#Pausa para revisar la insercion del nodo
            break
"""





#Interfaz Grafica con TKinter

def insert_movie(title: str) -> None:
    index=1
    found=False
    while index<len(movies): #Se busca el indice de la pelicula en el dataset
        if movies[index][0]==title:
            found=True
            break
        index+=1
    
    if found: # Si se encuentra el indice se toman los datos de esa pelicula de la lista de peliculas
            if arbol.insert(Node(data=movies[index][0],
                      year=int(movies[index][6]),
                      worldwideEarnings=float(movies[index][1]),
                      domesticEarnings=float(movies[index][2]),
                      foreignEarnings=float(movies[index][4]),
                      domesticPercentEarnings=float(movies[index][3]),
                      foreignPercentEarnings=float(movies[index][5]))):
                arbol.print_tree()
            else:
                messagebox.showerror(title="Error", message="La película ya se encuentra en el arbol")
    else:
        messagebox.showerror(title="Error", message="La película no se encuentra en el dataset")

def delete_movie(title: str) ->None:
    if arbol.delete(title):
        arbol.print_tree()
    else:
        messagebox.showerror(title="Error", message="La película no se encuentra en el arbol")

def search_movie(title: str) ->None:
    p,pad=arbol.search(title)
    if p is not None:
        messagebox.showinfo(title="Película", message="Titulo: "+p.data+"\nAño: "+str(p.year)+"\nIngresos a nivel mundial: "+str(p.worldwideEarnings)+"\nIngresos a nivel nacional: "+str(p.domesticEarnings)+"\nIngresos a nivel internacional: "+str(p.foreignEarnings)+"\nPorcentaje de ingresos nacionales respecto a los mundiales: "+str(p.domesticPercentEarnings)+"%\nPorcentaje de ingresos internacionales respecto a los mundiales: "+str(p.foreignPercentEarnings)+"%")
    else:
        messagebox.showerror(title="Error", message="La película no se encuentra en el arbol")

def coinditional_search_movie(year: str, foreignEarnings: str) -> None:
    try:
        year=int(year)
        if year<0:
            messagebox.showerror(title="Error", message="El año debe ser un numero positivo")
            return
    except:
        messagebox.showerror(title="Error", message="El año debe ser un numero")
        return
    try:
        foreignEarnings=float(foreignEarnings)
        if foreignEarnings<0:
            messagebox.showerror(title="Error", message="Los ingresos deben tener valor positivo")
            return
    except:
        messagebox.showerror(title="Error", message="Los ingresos deben ser un numero")
        return
    coincidences=arbol.conditional_search(year,foreignEarnings)
    if len(coincidences)==0:
        messagebox.showerror(title="Error", message="No se encontraron coincidencias")
    else:
        show_conditionalSearchResultsWindow(conditionalSearchWindow,coincidences)

def get_movie_level(index: str,coincidences: list) -> None:
    try:
        index=int(index)
        if index<0 or index>len(coincidences)-1:
            messagebox.showerror(title="Error", message="El indice se encuentra fuera del rango")
            return
    except:
        messagebox.showerror(title="Error", message="El indice debe ser un numero entero")
        return
    messagebox.showinfo(title="Nivel del nodo", message="El nivel del nodo es: "+str(arbol.node_level(coincidences[index])))

def get_movie_dad(index: str,coincidences: list) -> None:
    try:
        index=int(index)
        if index<0 or index>len(coincidences)-1:
            messagebox.showerror(title="Error", message="El indice se encuentra fuera del rango")
            return
    except:
        messagebox.showerror(title="Error", message="El indice debe ser un numero entero")
        return
    dad=arbol.node_dad(coincidences[index])
    if dad is None:
        messagebox.showinfo(title="Padre del nodo", message="El nodo no tiene padre")
        return
    messagebox.showinfo(title="Padre del nodo", message="El padre de '"+coincidences[index].data+"' es: '"+dad.data+"'")

def get_movie_granddad(index: str,coincidences: list) -> None:
    try:
        index=int(index)
        if index<0 or index>len(coincidences)-1:
            messagebox.showerror(title="Error", message="El indice se encuentra fuera del rango")
            return
    except:
        messagebox.showerror(title="Error", message="El indice debe ser un numero entero")
        return
    grand=arbol.node_granddad(coincidences[index])
    if grand is None:
        messagebox.showinfo(title="Abuelo del nodo", message="El nodo no tiene abuelo")
        return
    messagebox.showinfo(title="Abuelo del nodo", message="El abuelo de '"+coincidences[index].data+"' es: '"+grand.data+"'")

def get_movie_uncle(index: str,coincidences: list) -> None:
    try:
        index=int(index)
        if index<0 or index>len(coincidences)-1:
            messagebox.showerror(title="Error", message="El indice se encuentra fuera del rango")
            return
    except:
        messagebox.showerror(title="Error", message="El indice debe ser un numero entero")
        return
    uncle=arbol.node_uncle(coincidences[index])
    if uncle is None:
        messagebox.showinfo(title="Tio del nodo", message="El nodo no tiene tio")
        return
    messagebox.showinfo(title="Tio del nodo", message="El tio de '"+coincidences[index].data+"' es: '"+uncle.data+"'")

def get_movie_balance(index: str,coincidences: list) -> None:
    try:
        index=int(index)
        if index<0 or index>len(coincidences)-1:
            messagebox.showerror(title="Error", message="El indice se encuentra fuera del rango")
            return
    except:
        messagebox.showerror(title="Error", message="El indice debe ser un numero entero")
        return
    messagebox.showinfo(title="Balance del nodo", message="El balance del nodo es: "+str(arbol.balance(coincidences[index])))

def get_levels() ->None:
    window8 = tk.Toplevel()
    window8.title("Recorrido Por Niveles")
    window8.geometry("800x300")
    tk.Label(window8, text="Recorrido Por Niveles", font=("Arial", 14)).pack(pady=20)
    coincidencesText=scrolledtext.ScrolledText(window8, width=95,height=10)
    coincidencesText.place(relx=0.01,rely=0.3)
    coincidencesText.config(state="normal")
    coincidencesText.insert(tk.INSERT,arbol.levels_r())
    coincidencesText.config(state="disabled")

def show_root(frame):
    frame.withdraw() 
    root.deiconify()
def show_functionsWindow(frame):
    frame.withdraw() 
    functionsWindow.deiconify()
def show_insertionWindow(frame):
    frame.withdraw() 
    insertionWindow.deiconify()
def show_eliminationWindow(frame):
    frame.withdraw() 
    eliminationWindow.deiconify()
def show_searchWindow(frame):
    frame.withdraw() 
    searchWindow.deiconify()
def show_conditionalSearchWindow(frame):
    frame.withdraw() 
    conditionalSearchWindow.deiconify()
def show_conditionalSearchResultsWindow(frame,coincidences: list):
    frame.withdraw() 
    # Septima ventana (Resultados Busqueda Condicional)
    conditionalSearchResultsWindow = tk.Toplevel()
    conditionalSearchResultsWindow.title("Resultados Busqueda Condicional")
    conditionalSearchResultsWindow.geometry("700x600")
    conditionalSearchResultsWindow.resizable(False,False) 
    conditionalSearchResultsWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
    tk.Label(conditionalSearchResultsWindow, text="Resultados Busqueda Condicional", font=("Arial", 14)).pack(pady=20)
    tk.Label(conditionalSearchResultsWindow, text="Se encontraron "+str(len(coincidences))+" resultados.\nSi desea realizar alguna accion con uno de los resultados \ningrese el indice correspondiente y seleccione una de las acciones.", font=("Arial", 10)).pack(pady=7)
    tk.Label(conditionalSearchResultsWindow, text="Indice:", font=("Arial", 10)).place(relx=0.3,rely=0.7)
    coincidencesText7=scrolledtext.ScrolledText(conditionalSearchResultsWindow, width=47,height=10)
    coincidencesText7.config(state="normal")
    coincidencesText7.insert(tk.INSERT,"Indice:\tPelicula:\n")
    for i in range(len(coincidences)):
        coincidencesText7.insert(tk.INSERT,str(i)+"\t"+coincidences[i].data+"\n")
    coincidencesText7.config(state="disabled")
    coincidencesText7.place(relx=0.22,rely=0.3)
    entryIndex7 = tk.Entry(conditionalSearchResultsWindow, width=30)
    entryIndex7.place(relx=0.4,rely=0.7)
    backButton7 = tk.Button(conditionalSearchResultsWindow, text="Volver", command=lambda: show_conditionalSearchWindow(conditionalSearchResultsWindow))
    backButton7.place(x=10,y=10)
    getLevelButton7 = tk.Button(conditionalSearchResultsWindow, text="Obtener Nivel", command=lambda: get_movie_level(entryIndex7.get(),coincidences))
    getLevelButton7.place(rely=0.8,relx=0.01)
    getBalanceButton7 = tk.Button(conditionalSearchResultsWindow, text="Obtener Balanceo", command=lambda: get_movie_balance(entryIndex7.get(),coincidences))
    getBalanceButton7.place(rely=0.8,relx=0.2)
    getDadButton7 = tk.Button(conditionalSearchResultsWindow, text="Obtener Padre", command=lambda: get_movie_dad(entryIndex7.get(),coincidences))
    getDadButton7.place(rely=0.8,relx=0.4)
    getGranddadButton7 = tk.Button(conditionalSearchResultsWindow, text="Obtener Abuelo", command=lambda: get_movie_granddad(entryIndex7.get(),coincidences))
    getGranddadButton7.place(rely=0.8,relx=0.6)
    getUncleButton7 = tk.Button(conditionalSearchResultsWindow, text="Obtener Tio", command=lambda: get_movie_uncle(entryIndex7.get(),coincidences))
    getUncleButton7.place(rely=0.8,relx=0.8)



# Primera ventana (Inicio)
root = tk.Tk()
root.title("Inicio")
root.geometry("500x300")
root.resizable(False,False) 
label1 = tk.Label(root, text="Peliculas", font=("Arial", 14))
label1.pack(pady=20)
continue_button = tk.Button(root, text="Continuar", command=lambda: show_functionsWindow(root))
continue_button.place(rely=0.7,relx=0.45)

# Segunda ventana (Funciones)
functionsWindow = tk.Toplevel()
functionsWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
functionsWindow.title("Funciones")
functionsWindow.geometry("600x300")
functionsWindow.resizable(False,False) 
functionsWindow.withdraw()  # Esconde la ventana al inicio
label2 = tk.Label(functionsWindow, text="Funciones", font=("Arial", 14))
label2.pack(pady=20)
backButton2 = tk.Button(functionsWindow, text="Volver", command=lambda: show_root(functionsWindow))
backButton2.place(x=10,y=10)
insertionButton2 = tk.Button(functionsWindow, text="Inserción", command=lambda: show_insertionWindow(functionsWindow))
insertionButton2.pack(pady=5)
eliminationButton2 = tk.Button(functionsWindow, text="Eliminación", command=lambda: show_eliminationWindow(functionsWindow))
eliminationButton2.pack(pady=5)
searchButton2 = tk.Button(functionsWindow, text="Busqueda", command=lambda: show_searchWindow(functionsWindow))
searchButton2.pack(pady=5)
conditionalSearchButton2 = tk.Button(functionsWindow, text="Busqueda Condicional", command=lambda: show_conditionalSearchWindow(functionsWindow))
conditionalSearchButton2.pack(pady=5)
displayButton2 = tk.Button(functionsWindow, text="Visualización",command=lambda: arbol.print_tree())
displayButton2.pack(pady=5)
levelButton2 = tk.Button(functionsWindow, text="Recorrido Por Niveles",command=lambda: get_levels())
levelButton2.pack(pady=5)

# Tercera ventana (Inserción)
insertionWindow = tk.Toplevel()
insertionWindow.title("Inserción")
insertionWindow.geometry("600x300")
insertionWindow.resizable(False,False) 
insertionWindow.withdraw()
insertionWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
tk.Label(insertionWindow, text="Inserción", font=("Arial", 14)).pack(pady=20)
tk.Label(insertionWindow, text="Ingrese el titulo de la pelicula a insertar:", font=("Arial", 12)).pack(pady=20)
movieTitleEntry3 = tk.Entry(insertionWindow, width=30)
movieTitleEntry3.pack(pady=10)
backButton3 = tk.Button(insertionWindow, text="Volver", command=lambda: show_functionsWindow(insertionWindow))
backButton3.place(x=10,y=10)
insertButton3 = tk.Button(insertionWindow, text="Insertar", command=lambda: insert_movie(movieTitleEntry3.get()))
insertButton3.pack(pady=20)

# Cuarta ventana (Eliminación)
eliminationWindow = tk.Toplevel()
eliminationWindow.title("Eliminación")
eliminationWindow.geometry("600x300")
eliminationWindow.resizable(False,False) 
eliminationWindow.withdraw()
eliminationWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
tk.Label(eliminationWindow, text="Eliminación", font=("Arial", 14)).pack(pady=20)
tk.Label(eliminationWindow, text="Ingrese el nombre de la película a eliminar:", font=("Arial", 12)).pack(pady=20)
movieTitleEntry4 = tk.Entry(eliminationWindow, width=30)
movieTitleEntry4.pack(pady=10)
backButton4 = tk.Button(eliminationWindow, text="Volver", command=lambda: show_functionsWindow(eliminationWindow))
backButton4.place(x=10,y=10)
eliminateButton4 = tk.Button(eliminationWindow, text="Eliminar", command=lambda: delete_movie(movieTitleEntry4.get()))
eliminateButton4.pack(pady=20)

# Quinta ventana (Busqueda)
searchWindow = tk.Toplevel()
searchWindow.title("Busqueda")
searchWindow.geometry("600x300")
searchWindow.resizable(False,False) 
searchWindow.withdraw()
searchWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
tk.Label(searchWindow, text="Busqueda", font=("Arial", 14)).pack(pady=20)
tk.Label(searchWindow, text="Ingrese el nombre de la pelicula a buscar:", font=("Arial", 12)).pack(pady=22)
movieTitleEntry5 = tk.Entry(searchWindow, width=30)
movieTitleEntry5.pack(pady=10)
backButton5 = tk.Button(searchWindow, text="Volver", command=lambda: show_functionsWindow(searchWindow))
backButton5.place(x=10,y=10)
searchButton5 = tk.Button(searchWindow, text="Buscar", command=lambda: search_movie(movieTitleEntry5.get()))
searchButton5.pack(pady=20)

# Sexta ventana (Busqueda Condicional)
conditionalSearchWindow = tk.Toplevel()
conditionalSearchWindow.title("Busqueda Condicional")
conditionalSearchWindow.geometry("600x300")
conditionalSearchWindow.resizable(False,False) 
conditionalSearchWindow.withdraw()
conditionalSearchWindow.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
tk.Label(conditionalSearchWindow, text="Busqueda Condicional", font=("Arial", 14)).pack(pady=20)
tk.Label(conditionalSearchWindow, text="Buscar las peliculas estrenadas en el año ingresado, que sus ingresos nacionales sean menores que \nlos internacionales y que los ingresos internacionales sean mayores o iguales que el valor ingresado:", font=("Arial", 10)).pack(pady=7)
tk.Label(conditionalSearchWindow, text="Año:", font=("Arial", 10)).place(relx=0.1,rely=0.5)
tk.Label(conditionalSearchWindow, text="Ingresos Internacionales:", font=("Arial", 10)).place(relx=0.1,rely=0.6)
entryYear6 = tk.Entry(conditionalSearchWindow, width=30)
entryForeignEarnings6 = tk.Entry(conditionalSearchWindow, width=30)
entryYear6.place(relx=0.4,rely=0.5)
entryForeignEarnings6.place(relx=0.4,rely=0.6)
backButton6 = tk.Button(conditionalSearchWindow, text="Volver", command=lambda: show_functionsWindow(conditionalSearchWindow))
backButton6.place(x=10,y=10)
conditionalSearchButton6 = tk.Button(conditionalSearchWindow, text="Buscar", command=lambda: coinditional_search_movie(entryYear6.get(),entryForeignEarnings6.get()))
conditionalSearchButton6.place(rely=0.8,relx=0.45)


# Inicia el bucle principal de la aplicación
root.mainloop()
