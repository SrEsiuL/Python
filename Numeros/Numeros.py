from tkinter import* #pip install tkinter
from PIL import ImageTk, Image #pip install pillow
from playsound import playsound #pip install playsound==1.2.2

#cosas del tk (https://guia-tkinter.readthedocs.io/es/develop/chapters/7-options/7.1-Intro.html)

#configuración de la ventana
raiz = Tk()
raiz.title("Jueguito") #titulo
raiz.geometry("530x780") #dimensión
raiz.iconbitmap("Imagenes\Mesa.ico") #imagen ico
raiz.config(bg="alice blue") #color de fondo (https://www.tcl.tk/man/tcl8.5/TkCmd/colors.html)
raiz.resizable(0,0) #bloqueo que modifiquen el tamaña de la entana

class test:
	#escribir el numero
	def nombre(self, a):
		texto = Label(frame, text = a.upper(), width = 35)
		texto.grid(row = 4, column = 0, columnspan = 3, padx = 5, pady = 5)
		ruta = "Song\\" + a + ".mp3"
		self.ruta = ruta
		return

	#reproducir el audio
	def audio(self):
		playsound(self.ruta)
		self.ruta = ""

prueba = test()

#grid
frame = Frame(raiz, bg="white", bd=5)
frame.pack(padx=12, pady=12)

#uno
img = ImageTk.PhotoImage(Image.open(r"Imagenes\Uno.png").resize((150, 150)))
boton = Button(frame, image = img, relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Uno"))
boton.grid(row=0, column=0, padx=5, pady=5)

#dos
img2 = ImageTk.PhotoImage(Image.open(r"Imagenes\Dos.png").resize((150, 150)))
boton2 = Button(frame, image = img2,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Dos"))
boton2.grid(row=0, column=1, padx=5, pady=5)

#3
img3 = ImageTk.PhotoImage(Image.open(r"Imagenes\Tres.png").resize((150, 150)))
boton3 = Button(frame, image = img3,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Tres"))
boton3.grid(row=0, column=2, padx=5, pady=5)

#4
img4 = ImageTk.PhotoImage(Image.open(r"Imagenes\Cuatro.png").resize((150, 150)))
boton4 = Button(frame, image = img4,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Cuatro"))
boton4.grid(row=1, column=0, padx=5, pady=5)

#5
img5 = ImageTk.PhotoImage(Image.open(r"Imagenes\Cinco.png").resize((150, 150)))
boton5 = Button(frame, image = img5,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Cinco"))
boton5.grid(row=1, column=1)

#6
img6 = ImageTk.PhotoImage(Image.open(r"Imagenes\Seis.png").resize((150, 150)))
boton6 = Button(frame, image = img6,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Seis"))
boton6.grid(row=1, column=2)

#7
img7 = ImageTk.PhotoImage(Image.open(r"Imagenes\Siete.png").resize((150, 150)))
boton7 = Button(frame, image = img7,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Siete"))
boton7.grid(row=2, column=0, padx=5, pady=5)

#8
img8 = ImageTk.PhotoImage(Image.open(r"Imagenes\Ocho.png").resize((150, 150)))
boton8 = Button(frame, image = img8,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Ocho"))
boton8.grid(row=2, column=1)

#9
img9 = ImageTk.PhotoImage(Image.open(r"Imagenes\Nueve.png").resize((150, 150)))
boton9 = Button(frame, image = img9,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Nueve"))
boton9.grid(row=2, column=2)

#0
img0 = ImageTk.PhotoImage(Image.open(r"Imagenes\Cero.png").resize((150, 150)))
boton0 = Button(frame, image = img0,  relief="flat", overrelief="raised", background="CadetBlue", command = lambda: prueba.nombre("Cero"))
boton0.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

#instrucción
texto = Label(frame, text="Presiona cualquier imagen", width=35)
texto.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

imgA = ImageTk.PhotoImage(Image.open(r"Imagenes\Audio.png").resize((50, 40)))
botonA = Button(frame, image = imgA, state="active", command = lambda: prueba.audio())
botonA.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


raiz.mainloop()