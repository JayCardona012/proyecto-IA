import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
import time


class NodoArbol:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.hijos = []

print("hola")
class Laberinto:
    def __init__(self, root, rows=4, cols=4, expansiones_por_actualizacion=2):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_width = 100  # aqui acomoda el Ancho de cada celda
        self.cell_height = 80  # lo mismo Alto de cada celda
        self.image_scale_factor = 0.93  # esta mkd es para que la imagen no tape los bordes de las celdas, se escala un poco menos al 93
        self.expansiones_por_actualizacion = expansiones_por_actualizacion

        self.maze = [[0 for _ in range(cols)] for _ in range(rows)]  
        
        
        self.raton_pos = (2, 0)  # aqui define la Posición del ratón
        self.queso_pos = (1, 3)  # lo mismo con la Posición del queso
        self.bloques_grises = [(2, 1), (1, 1), (1, 2), (3, 3)]  # aqui ubica las Paredes/bloques grises donde le de la gana

        
        self.raton_image = self.cargar_imagenes(r"C:\\Users\\jayCg\\OneDrive\\Escritorio\\proyecto IA\\Images\\Raton.png")#no se le olvide combiar la ruta de las imagenes o paila no se ejecuta esta monda
        self.queso_image = self.cargar_imagenes(r"C:\\Users\\jayCg\\OneDrive\\Escritorio\\proyecto IA\\Images\\queso.png")

        self.iniciar_laberinto()

      
        self.dibujar_laberinto()
        self.crear_area_arbol()

        
        self.boton_iniciar = tk.Button(self.root, text="Iniciar", command=self.iniciar_busqueda)
        self.boton_iniciar.grid(row=1, column=0, pady=100000)
    print("hola")
    def cargar_imagenes(self, path):
        adjusted_width = int(self.cell_width * self.image_scale_factor)
        adjusted_height = int(self.cell_height * self.image_scale_factor)
        image = Image.open(path).resize((adjusted_width, adjusted_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def iniciar_laberinto(self):
        for bloque in self.bloques_grises:
            row, col = bloque
            self.maze[row][col] = 1  # esto representa un bloque o pared

    def dibujar_laberinto(self):
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_width, height=self.rows * self.cell_height)
        self.canvas.grid(row=0, column=0)


        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_width
                y1 = i * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height


                if self.maze[i][j] == 1:  
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

   
        raton_x, raton_y = self.raton_pos
        raton_cx = raton_y * self.cell_width + (self.cell_width - self.raton_image.width()) // 2
        raton_cy = raton_x * self.cell_height + (self.cell_height - self.raton_image.height()) // 2
        self.canvas.create_image(raton_cx, raton_cy, anchor="nw", image=self.raton_image)


        queso_x, queso_y = self.queso_pos
        queso_cx = queso_y * self.cell_width + (self.cell_width - self.queso_image.width()) // 2
        queso_cy = queso_x * self.cell_height + (self.cell_height - self.queso_image.height()) // 2
        self.canvas.create_image(queso_cx, queso_cy, anchor="nw", image=self.queso_image)


    def crear_area_arbol(self):
        self.canvas_arbol = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas_arbol.grid(row=0, column=1, padx=20, pady=20)
        self.nodo_padre_coords = {}  

    def iniciar_busqueda(self):
        self.boton_iniciar.config(state=tk.DISABLED)  # Desactivar el botón para evitar múltiples búsquedas
        self.realizar_bfs()  # Comenzar la búsqueda por amplitud la unica que tengo daa

    def realizar_bfs(self):
        cola = deque([NodoArbol(self.raton_pos)])
        visitados = set([self.raton_pos])
        expansiones = 0

        while cola:
            nodo_actual = cola.popleft()
            posicion_actual = nodo_actual.posicion

            if posicion_actual == self.queso_pos:
                print("Queso encontrado!")
                self.mostrar_camino(nodo_actual)
                return


            for movimiento in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nueva_posicion = (posicion_actual[0] + movimiento[0], posicion_actual[1] + movimiento[1])


                if (0 <= nueva_posicion[0] < self.rows and
                    0 <= nueva_posicion[1] < self.cols and
                    self.maze[nueva_posicion[0]][nueva_posicion[1]] == 0 and
                    nueva_posicion not in visitados):
                    
                    nuevo_nodo = NodoArbol(nueva_posicion, nodo_actual)
                    nodo_actual.hijos.append(nuevo_nodo)
                    cola.append(nuevo_nodo)
                    visitados.add(nueva_posicion)

                    expansiones += 1

                    self.dibujar_nodo_lab(nueva_posicion)
                    self.dibujar_arbol(nodo_actual, nuevo_nodo)
                    

                    self.root.update()
                    time.sleep(0.5)  # ajustar el tiempo e expansion del arbol

        print("No se encontró el queso.")

    def dibujar_nodo_lab(self, posicion):
        x1 = posicion[1] * self.cell_width
        y1 = posicion[0] * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")

    def dibujar_arbol(self, nodo_padre, nodo_hijo):
        if nodo_padre not in self.nodo_padre_coords:
            self.nodo_padre_coords[nodo_padre] = (200, 20)  
            self.canvas_arbol.create_oval(195, 15, 205, 25, fill="blue")  


        x_padre, y_padre = self.nodo_padre_coords[nodo_padre]
        x_hijo = x_padre + len(nodo_padre.hijos) * 50 - 25
        y_hijo = y_padre + 50


        self.canvas_arbol.create_line(x_padre, y_padre, x_hijo, y_hijo, fill="black")
        self.canvas_arbol.create_oval(x_hijo - 5, y_hijo - 5, x_hijo + 5, y_hijo + 5, fill="blue")


        self.nodo_padre_coords[nodo_hijo] = (x_hijo, y_hijo)

    def mostrar_camino(self, nodo):
        while nodo:
            self.dibujar_nodo_lab(nodo.posicion)
            nodo = nodo.padre
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Laberinto - Búsqueda por Amplitud")
    app = Laberinto(root, expansiones_por_actualizacion=2)
    root.mainloop()
