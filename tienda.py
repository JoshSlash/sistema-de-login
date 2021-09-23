# -*- coding: utf-8 -*-
# -*- coding: 1252 -*-
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import os
from os import scandir
import shutil
import csv
import codecs
import glob
import time
import unittest
tamx=50
def listarCarpeta(path): return [obj.name for obj in scandir(path) if obj.is_file()]

def crearMatriz(anio):
	M=[]
	with open("ventas"+"/"+anio+".dat", newline='') as File:
			reader = csv.reader(File)
			for row in reader:
				M.append(row)
	return M

def mensaje(texto):
	def aceptar():
		app.destroy()
		usuario()
	pos=tamx//2
	app,vp=darkmode("Mensaje")
	Label(vp,text=texto,font='arial 20 bold').grid(column=pos, row=1, sticky=(W,E))
	Button(vp, text="Aceptar",font='arial 20',fg="black",command=aceptar,bg='#F69E6B').grid(column=pos, row=2)

def crearVentana(nombre,fondo='#FAF3DD'):
	def cambioFondo():
		M=crearMatriz("color")
		if int(M[0][0])==0:
			M[0][0]=1
			N=[]
			for i in M:
				if len(i)>0:
					N.append(i)
			open("ventas/color.dat", 'w')
			myFile=open("ventas/color.dat", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(N)
			myFile.close()
		else:
			M[0][0]=0
			open("ventas/color.dat", 'w')
			myFile=open("ventas/color.dat", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(M)
			myFile.close()
		app.destroy()
		mensaje("Se cambio el tema, debe iniciar sesión nuevamente")
	#Definicion de la ventana tk
	app = Tk()
	app.title(nombre)
	app.configure(background=fondo)
	app.wm_attributes("-alpha", 0.97)
	app.resizable(0,0)
	vp = Frame(app)
	vp.grid(column=0, row=0, padx=(0,0), pady=(0,0))
	vp.columnconfigure(0, weight=0)
	vp.rowconfigure(0, weight=1)
	vp.config(bg=fondo)
	for i in range(tamx): Label(vp,text=' ',font='arial 16 bold',bg=fondo).grid(column=i, row=0, sticky=(W,E))
	if fondo=='#FAF3DD':
		Button(vp, text="DarkMode",font='arial 16',fg="white",command=cambioFondo,bg='#000000').grid(column=tamx, row=0)
		Label(vp,text=nombre,font='arial 16 bold',highlightbackground='blue',highlightcolor= "red", highlightthickness=2,bg='#FAF3DD').grid(column=tamx//2, row=0, sticky=(W,E))
	else:
		Button(vp, text="ModoClaro",font='arial 16',fg="black",command=cambioFondo,bg='#FAF3DD').grid(column=tamx, row=0)
		Label(vp,text=nombre,font='arial 16 bold',highlightbackground='blue',highlightcolor= "red", fg="white",highlightthickness=2,bg='#000000').grid(column=tamx//2, row=0, sticky=(W,E))
	return app,vp

def darkmode(nombre):
	try:
		len(listarCarpeta("ventas"))
	except FileNotFoundError:
		os.makedirs('ventas', exist_ok=True)
	if len(listarCarpeta("ventas"))==0:
		N=[]
		L=[0]
		N.append(L)
		open("ventas/color.dat", 'w')
		myFile=open("ventas/color.dat", 'w')
		with myFile:
			writer = csv.writer(myFile)
			writer.writerows(N)
		myFile.close()
	else:
		M=crearMatriz("color")
		if int(M[0][0])==0: a,v=crearVentana(nombre)
		else: a,v=crearVentana(nombre,'#000000')
	return a,v

def botonInsertar():
	app,vp=darkmode("INSERTAR")
	messagebox.showinfo(message="¡Escanea el codigo de barras del producto!", title="Escanear:")

def menu(user):
	pos=tamx//2
	def nuevo():
		app.destroy()
		nuevoUsuario()
	def salir():
		app.destroy()
		usuario()
	def insertar():
		app.destroy()
		botonInsertar()
	def actualizar():#Abre menu buscar
		app.destroy()
		#botonBuscar(user)
	def eliminar():#Abre menu formulario
		app.destroy()
		#formulario(user)
	def buscar():#Sale de la app menu
		app.destroy()
	app,vp=darkmode("Menu")
	if user==1:
		texto=["Insertar","Actualizar","Eliminar","Buscar","Agregar usuario","Cerrar sesión"]
		color=['#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7']
		botones=[insertar,actualizar,eliminar,buscar,nuevo,salir]
		for i in range(len(texto)): Button(vp,text=texto[i],font='arial 20',command=botones[i],bg=color[i]).grid(column=pos+1, row=i+1)
	else:	
		texto2=["Insertar","Buscar","Salir"]
		botones2=[insertar,buscar,salir]
		color=['#FFB6C1','#E6E6FA','#00FF00','#F0E68C','#FFA07A','#FFE4E1']
		for i in range(len(texto2)): Button(vp,text=texto2[i],font='arial 20',command=botones2[i],bg=color[i]).grid(column=pos+1, row=i+1)
	app.mainloop()

def encriptar(palabra):
	S=[]
	tam=len(palabra)
	for i in palabra: S.append(ord(str(i)))
	return S,tam 

def nuevoUsuario():
	pos=tamx//2
	app,vp=darkmode("ADMINISTRADOR")
	def entrar():
		if (str(entrada1.get())=="" or str(entrada2.get())==""):
			messagebox.showinfo(message="Escriba un usuario o contraseña", title="ERROR")
			return 0
		if  (len(crearMatriz("usuarios"))<1): messagebox.showinfo(message="¡Se registrara primero un SUPER ADMINISTRADOR!", title="Administrador:")
		M=crearMatriz("usuarios")
		L=[len(crearMatriz("usuarios"))]
		L.append(str(entrada1.get()))
		S,tam=encriptar(str(entrada2.get()))
		for i in S: L.append(i)
		L.append(tam)
		M.append(L)
		myFile = open("ventas/usuarios.dat",'w')
		with myFile:
			writer = csv.writer(myFile)
			writer.writerows(M)
		messagebox.showinfo(message="¡Se registraro correctamente: "+str(entrada1.get())+" con contraseña: "+str(entrada2.get()), title="Registro correcto:")
		app.destroy()
		usuario()
	#Creacion de botones y etiquetas
	v1=""
	e1=Label(vp,text='Usuario',font='arial 16 bold').grid(column=pos+1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 20')
	entrada1.grid(column=pos+2, row=1)
	v2=""
	e2=Label(vp,text='Contraseña',font='arial 16 bold')
	e2.grid(column=pos+1, row=2, sticky=(W,E))
	entrada2=Entry(vp, width=20, textvariable=v2,show='*',font='arial 20')
	entrada2.grid(column=pos+2, row=2)
	Button(vp, text="Aceptar",font='arial 16',command=entrar,bg='#00FF00').grid(column=pos+1, row=3)
	app.mainloop()	

def desencriptar(L,tam):
	s=""
	for i in range(2,tam+2):
		c=chr(int(L[i]))
		c=str(c)
		s=s+c
	return s

def usuario():
	def admin():#Sale de menu usuario y abre menu validar
		app.destroy()
		validar(1)
	def user():
		app.destroy()
		validar(2)
	def iniciar():
		os.makedirs('ventas/Base de Datos', exist_ok=True)
		f=open("ventas/usuarios.dat", 'w')
		app.destroy()
		f.close()
		nuevoUsuario()
	def salir():#Sale de menu usuario
		app.destroy()
	def ingresar():
		M=crearMatriz("usuarios")
		k=0
		user=str(cb.get())
		password=str(entrada2.get())
		for i in range(len(M)): 
			if user in M[i]:
				k=i
				break
		if k==0:
			if password==desencriptar(M[k],int(M[k][len(M[k])-1])):
				app.destroy()
				menu(1)
			else: messagebox.showinfo(message="Contraseña de: "+user+" INCORRECTA", title="Error")
		else:
			if password==desencriptar(M[k],int(M[k][len(M[k])-1])):
				app.destroy()
				menu(2)
			else: messagebox.showinfo(message="Contraseña de: "+user+" INCORRECTA", title="Error")
	app,vp=darkmode("Usuarios")
	try:
		len(listarCarpeta("ventas"))
	except FileNotFoundError:
		os.makedirs('ventas', exist_ok=True)
	
	if (len(listarCarpeta("ventas"))==1): 
		Button(vp, text="Iniciar",font='arial 20',command=iniciar,bg='#F69E6B').grid(column=tamx//2, row=0)	
	else:
		pos=tamx//2
		M=crearMatriz("usuarios")
		sel=[]
		for i in range(len(M)): 
			if len(M[i])>0: sel.append(M[i][1])
		Label(vp,text='Usuario: ',font='arial 16 bold').grid(column=pos+1, row=1, sticky=(W,E))
		cb=ttk.Combobox(vp,values=sel,width=15,font='arial 20 bold',state="readonly")
		cb.grid(column=pos+2, row=1)
		v2=""
		Label(vp,text='Contraseña',font='arial 16 bold',highlightbackground='blue',highlightcolor= "red", highlightthickness=2).grid(column=pos+1, row=2, sticky=(W,E))
		entrada2=Entry(vp, width=20, textvariable=v2,show='*',font='arial 16', highlightbackground='blue',highlightcolor= "red", highlightthickness=2)
		entrada2.grid(column=pos+2, row=2)
		Button(vp, text="Ingresar",font='arial 20',command=ingresar,bg='#F69E6B',fg='black').grid(column=pos+1, row=3)
		#ttk.Button(vp, text="Salir",command=salir).grid(column=2, row=3)
	Label(vp,text=time.strftime("%d/%m/%y"),font='arial 20 bold',fg="black", bg="#FAF3DD").grid(column=0, row=0, sticky=(W,E))
	app.mainloop()
usuario()