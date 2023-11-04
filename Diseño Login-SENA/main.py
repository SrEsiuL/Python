from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import CTkEntry, CTkButton #pip install customtkinter

#####configuración#####
root = Tk()#iniciación de la ventana
root.title("Login")#titulo
root.geometry('925x500+300+200')#dimensión ventana
root.configure(bg = "#fff")#color de fondo
root.resizable(False, False)#evitar reajustamiento de la ventana
color_verde = "#39A900" #color corporativo
logo_verde = "images/logo_verde.png"#ruta imagen
img = ImageTk.PhotoImage(Image.open(logo_verde).resize((300, 300)))#imagen fondo
logo = ImageTk.PhotoImage(Image.open(logo_verde).resize((50, 50)))#imagen ico
root.call('wm', 'iconphoto', root._w, logo)#asignación imagen ico
#####fin configuración#####

#####parte Blanca#####
Label(root, image = img, bg = 'white').place(x = 40, y = 90)#asignación imagen fondo
frame = Frame(root, width = 550, height = 500, bg = color_verde)
frame.place(x = 400, y = 0)
#####fin parte blanca#####

#####parte verde#####
cabezera = Label(frame, text = 'Iniciar Sección', fg = 'white', bg = color_verde, font = ('Work Sans',23,'bold'))
cabezera.place(x = 140, y = 70)

Label(frame, text = 'Nombre de Usuario:', fg = 'white', bg = color_verde, font = ('Work Sans',11,'bold')).place(x = 110, y = 140)
usuario = CTkEntry(frame, width = 300, fg_color = 'white', border_width = 0, placeholder_text_color = color_verde, placeholder_text = "User",
                   text_color = color_verde, font = ('Work Sans',15))
usuario.place(x = 110, y = 170)#caja de usuario

Label(frame, text = 'Contraseña:', fg = 'white', bg = color_verde, font = ('Work Sans',11,'bold')).place(x = 110, y = 220)
contrasena = CTkEntry(frame, width = 300, fg_color = 'white', border_width = 0, placeholder_text = "****", placeholder_text_color = color_verde,
                      text_color = color_verde, font = ('Work Sans',15), show = '*')
contrasena.place(x = 110, y = 250)#caja de contraseña


CTkButton(frame, width = 100, text = 'Ingresar', text_color = color_verde, border_width = 0, fg_color = 'white', hover_color = '#81F79F', 
          font = ('Work Sans',15,'bold'), cursor = 'hand2').place(x = 200, y = 350)#boton ingresar
#####fin parte verde#####

root.mainloop()#bucle de ejecución