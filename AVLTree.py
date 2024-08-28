from typing import Any, Optional, Tuple
import networkx as nx, matplotlib.pyplot as plt,tkinter as tk,numpy as np,csv
from tkinter import messagebox
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
            print(node.data, end = ' ')
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
        """Escribir algoritmo no recursivo para la altura de un arbol"""
        return self.__height_r(self.root)

    def __height_r(self, node: Optional["Node"]) -> int:
        if node is None:
            return 0
        return 1 + max(self.__height_r(node.left), self.__height_r(node.right))
    
    def balance(self,node: "Node") -> int:
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
            if pad is not None:
                self.check_balance(pad)
            return True
        return False

    def check_balance(self, node: "Node"):
        p,pad=self.search(node.data)
        while pad is not None:
            if self.balance(pad)==-2:
                if self.balance(p)==-1:
                    if pad==self.root:
                            self.root=self.simple_right_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.simple_right_rotation(pad)#Si un nodo tiene balance -2 y su hijo -1 se hace una rotacion simple derecha
                        else:
                            grand.right=self.simple_right_rotation(pad)
                elif self.balance(p)==1:
                    if pad==self.root:
                            self.root=self.double_left_right_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.double_left_right_rotation(pad)#Si un nodo tiene balance -2 y su hijo 1 se hace una rotacion doble izquierda derecha
                        else:
                            grand.right=self.double_left_right_rotation(pad)
                elif self.balance(p)==0:
                    if pad==self.root:
                            self.root=self.simple_right_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.simple_right_rotation(pad)#Si un nodo tiene balance -2 y su hijo 0 se hace una rotacion simple derecha
                        else:
                            grand.right=self.simple_right_rotation(pad)
                return True
            elif self.balance(pad)==2:
                if self.balance(p)==-1:
                    if pad==self.root:
                            self.root=self.double_right_left_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.double_right_left_rotation(pad)#Si un nodo tiene balance 2 y su hijo -1 se hace una rotacion doble derecha izquierda
                        else:
                            grand.right=self.double_right_left_rotation(pad)
                elif self.balance(p)==1:
                    if pad==self.root:
                            self.root=self.simple_left_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.simple_left_rotation(pad)#Si un nodo tiene balance 2 y su hijo 1 se hace una rotacion simple izquierda
                        else:
                            grand.right=self.simple_left_rotation(pad)
                elif self.balance(p)==0:
                    if pad==self.root:
                            self.root=self.simple_left_rotation(pad)
                    else:
                        pad,grand = self.search(pad.data)
                        if pad==grand.left:
                            grand.left=self.simple_left_rotation(pad)#Si un nodo tiene balance 2 y su hijo 0 se hace una rotacion simple izquierda
                        else:
                            grand.right=self.simple_left_rotation(pad)
                return True
            else:
                p,pad=self.search(pad.data)

    def simple_left_rotation(self, node: "Node") -> Node:
        aux=node.right
        node.right=aux.left
        aux.left=node
        return aux
    
    def simple_right_rotation(self, node: "Node") -> Node:
        aux=node.left
        node.left=aux.right
        aux.right=node
        return aux
    
    def double_right_left_rotation(self, node: "Node") -> Node:
        node.right=self.simple_right_rotation(node.right)
        return self.simple_left_rotation(node)
    
    def double_left_right_rotation(self, node: "Node") -> Node:
        node.left=self.simple_left_rotation(node.left)
        return self.simple_right_rotation(node)




#Arbol De Ejemplo
arbol=AVLT()

with open("dataset_movies.csv",newline='') as f:
    data = csv.reader(f,delimiter=',')
    movies = list(data)

"""
for i in range(20):    #Se escogen elementos aleatorios de la lista de peliculas
    e=random.randint(1,4000)
    arbol.insert(Node(data=movies[e][0],
                      year=int(movies[e][6]),
                      worldwideEarnings=float(movies[e][1]),
                      domesticEarnings=float(movies[e][2]),
                      foreignEarnings=float(movies[e][4]),
                      domesticPercentEarnings=float(movies[e][3]),
                      foreignPercentEarnings=float(movies[e][5])))
"""




#Interfaz Grafica con TKinter

def insert_movie(index: str) -> None:
    if index.isdigit():
        index=int(index)
        if index>len(movies)-1:
            messagebox.showerror(title="Error", message="El indice ingresado esta fuera del rango de peliculas.\nLa lista contiene "+str(len(movies)-1)+" peliculas.")
        else:
            arbol.insert(Node(data=movies[index][0],
                      year=int(movies[index][6]),
                      worldwideEarnings=float(movies[index][1]),
                      domesticEarnings=float(movies[index][2]),
                      foreignEarnings=float(movies[index][4]),
                      domesticPercentEarnings=float(movies[index][3]),
                      foreignPercentEarnings=float(movies[index][5])))
            arbol.print_tree()
    else:
        messagebox.showerror(title="Error", message="El indice ingresado debe ser un numero entero positivo")
    
def delete_movie(title: str) ->None:
    if arbol.delete(title):
        arbol.print_tree()
    else:
        messagebox.showerror(title="Error", message="El titulo de la pelicula no se encuentra en el arbol")

def show_root(frame):
    frame.withdraw() 
    root.deiconify()

def show_window2(frame):
    frame.withdraw() 
    window2.deiconify()

def show_window3(frame):
    frame.withdraw() 
    window3.deiconify()

def show_window4(frame):
    frame.withdraw() 
    window4.deiconify()

def show_window5(frame):
    frame.withdraw() 
    window5.deiconify()

# Función para cerrar la aplicación
def close_app():
    root.destroy()
    window2.destroy()
    window3.destroy()

# Primera ventana
root = tk.Tk()
root.title("Inicio")
root.geometry("500x300")
label1 = tk.Label(root, text="Peliculas", font=("Arial", 14))
label1.pack(pady=20)
button1 = tk.Button(root, text="Continuar", command=lambda: show_window2(root))
button1.place(rely=0.7,relx=0.45)

# Segunda ventana
window2 = tk.Toplevel()
window2.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
window2.title("Funciones")
window2.geometry("600x500")
window2.withdraw()  # Esconde la ventana al inicio
label2 = tk.Label(window2, text="Funciones", font=("Arial", 14))
label2.pack(pady=20)
button3_1 = tk.Button(window2, text="Volver", command=lambda: show_root(window2))
button3_1.place(x=10,y=10)
button2_1 = tk.Button(window2, text="Inserción", command=lambda: show_window3(window2))
button2_1.pack(pady=5)
button2_2 = tk.Button(window2, text="Eliminación", command=lambda: show_window4(window2))
button2_2.pack(pady=5)
button2_3 = tk.Button(window2, text="Busqueda", command=lambda: show_window5(window2))
button2_3.pack(pady=5)
button2_4 = tk.Button(window2, text="Visualización",command=lambda: arbol.print_tree())
button2_4.pack(pady=5)

# Tercera ventana
window3 = tk.Toplevel()
window3.title("Inserción")
window3.geometry("600x300")
window3.withdraw()
window3.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
label3 = tk.Label(window3, text="Ingrese el indice de la pelicula a insertar:", font=("Arial", 14))
label3.pack(pady=20)
entry3 = tk.Entry(window3, width=30)
entry3.pack(pady=10)
button3_1 = tk.Button(window3, text="Volver", command=lambda: show_window2(window3))
button3_1.place(x=10,y=10)
button3_2 = tk.Button(window3, text="Insertar", command=lambda: insert_movie(entry3.get()))
button3_2.pack(pady=20)

# Cuarta ventana
window4 = tk.Toplevel()
window4.title("Eliminación")
window4.geometry("600x300")
window4.withdraw()
window4.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
label4 = tk.Label(window4, text="Ingrese el nombre de la pelicula a eliminar:", font=("Arial", 14))
label4.pack(pady=20)
entry4 = tk.Entry(window4, width=30)
entry4.pack(pady=10)
button4_1 = tk.Button(window4, text="Volver", command=lambda: show_window2(window4))
button4_1.place(x=10,y=10)
button4_2 = tk.Button(window4, text="Eliminar", command=lambda: delete_movie(entry4.get()))
button4_2.pack(pady=20)

# Quinta ventana
window5 = tk.Toplevel()
window5.title("Busqueda")
window5.geometry("600x300")
window5.withdraw()
window5.protocol('WM_DELETE_WINDOW', lambda: root.destroy())
label5 = tk.Label(window5, text="Busqueda", font=("Arial", 14))
label5.pack(pady=20)
button5_1 = tk.Button(window5, text="Volver", command=lambda: show_window2(window5))
button5_1.place(x=10,y=10)
button5_2 = tk.Button(window5, text="Buscar", command=lambda: print("En desarrollo"))
button5_2.pack(pady=20)


# Inicia el bucle principal de la aplicación
root.mainloop()
