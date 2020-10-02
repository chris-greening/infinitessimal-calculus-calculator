#Author: Chris Greening
#Date: 11/21/18
#Purpose: The Infinitesimal Calculus Differentiation Calculator! 
"""
Notes: I basically want this to be a machine that can provide all kinds of 
quick analysis on multivariable (or single-variable) functions. The end goal
is to incorporate both differential and integral calculus and have graphing
capabilities as well.

Current capabilities:

-differentiate with respect to x,y,z
-shortcut to second partials
"""

from tkinter import Label, Button, Entry, Canvas, ttk
from tkinter import filedialog 
import tkinter as tk
import sys
#import tkinter.ttk				#code for vertical lines 
#from PIL import ImageTk, Image	#allows .jpg and .png to be used

from sympy import *

x, y, z = symbols('x y z')

class CalcCalculatorGUI:

	def __init__(self,master):
		self.master = master 
		master.title("The Infinitesimal Calculus Calculator!")
		
		self.function_label_text = tk.StringVar()	#main label widget
		self.function_label_text.set(0)
		self.function_label = Label(master, 
									textvariable = self.function_label_text)
		
		self.output_text = tk.StringVar()	#output label widget
		self.output_text.set('')
		self.output_label = Label(master, textvariable = self.output_text)
		
		# self.img = ImageTk.PhotoImage(Image.open("newton.jpg"))
		# self.canvas = Canvas(root, width = 300, height = 300)
		# self.canvas.create_image(20, 20, image = self.img)
		# self.canvas.image = self.img

		#widgets associated with function entry
		self.info_label = Label(master, text = "f(x,y,z) =")#label next to entry
		self.function_entry = Entry(master, width = 50)	#user input of f(x,y,z)
		self.update_button = Button(master, 
									text = "Update Function", 
									command=self.update_function)
		
		#df/dx button
		self.diffx_button = Button(master, text = "∂f/∂x", command=self.diffx)
		self.diffxx_button = Button(master, text = "f_xx", command=self.diffxx)
		self.diffxy_button = Button(master, text = "f_xy", command=self.diffxy)
		self.diffxz_button = Button(master, text = "f_xz", command=self.diffxz)
		
		#differentiate with respect to y button
		self.diffy_button = Button(master, text = "∂f/∂y", command=self.diffy)
		self.diffyx_button = Button(master, text = "f_yx", command=self.diffxy)
		self.diffyy_button = Button(master, text = "f_yy", command=self.diffyy)
		self.diffyz_button = Button(master, text = "f_yz", command=self.diffyz)		
		
		#differentiate with respect to z button 
		self.diffz_button = Button(master, text = "∂f/∂z", command=self.diffz)
		self.diffzx_button = Button(master, text = "f_zx", command=self.diffxz)
		self.diffzy_button = Button(master, text = "f_zy", command=self.diffyz)
		self.diffzz_button = Button(master, text = "f_zz", command=self.diffzz)		
	
		self.dx_button = Button(master, text = "dx", command = self.dx)
		self.dy_button = Button(master, text = "dy", command = self.dy)
		self.dz_button = Button(master, text = "dz", command = self.dz)
	
		self.gradient_button = Button(master, 
									text = "∇f",
									command = self.gradient)
		#self.divergence_button	= Button(master, 
										#text = "∇∙f", 
										#command = self.divergence)
		#self.curl_button = Button(master, text = "∇×f", command = self.curl)
	
		self.reset_button = Button(master, text = "Reset", command = self.reset)
	
		#LAYOUT
		self.function_label.grid(row=0, column = 4)	#main function loc
		self.output_label.grid(row=7, column = 1, columnspan = 15)#output loc 
		
		self.info_label.grid(row=1, column=0)	#'f(x,y,z)='
		self.function_entry.grid(row=1, column = 1, columnspan = 15)#entry loc
		self.update_button.grid(row=1, column =16)	#update button location
	
		#self.canvas.grid(row = 3, column = 9)
	
		self.diffx_button.grid(row=4, column = 1)	#f_x button location 
		self.diffxx_button.grid(row=4, column = 2)
		self.diffxy_button.grid(row=4, column = 3)
		self.diffxz_button.grid(row=4, column = 4)
		
		self.diffy_button.grid(row=5, column = 1)	#f_y button location
		self.diffyx_button.grid(row=5, column = 2)
		self.diffyy_button.grid(row=5, column = 3)
		self.diffyz_button.grid(row=5, column = 4)		
		
		self.diffz_button.grid(row=6, column = 1)	#f_z button location
		self.diffzx_button.grid(row=6, column = 2)
		self.diffzy_button.grid(row=6, column = 3)
		self.diffzz_button.grid(row=6, column = 4)		
		
		tk.ttk.Separator(master, orient='vertical').grid(column=5, 
												row=4, 
												rowspan=3, 
												sticky='ns')
		
		self.gradient_button.grid(row = 4, column = 6)	#gradient button
		
		tk.ttk.Separator(master, orient='vertical').grid(column=7, 
												row=4, 
												rowspan=3, 
												sticky='ns')

		self.dx_button.grid(row=4, column=8)
		self.dy_button.grid(row=5, column=8)
		self.dz_button.grid(row=6, column=8)
		#self.divergence_button.grid(row = 5, column = 6)	#gradient button
		#self.curl_button.grid(row = 6, column = 6)	#gradient button
		
		self.reset_button.grid(row = 4, column = 0)	#reset button 
		self.function = 0	#f(x,y,z)
		self.current_function = 0	#whatever derivative we have calculated 
		self.gradient = 0
		
	def update_function(self):
		"""Updates both the function we're working with and the label 
		that shows the user what function is currently loaded in"""
		if len(self.function_entry.get()) == 0:
			print("Please enter a valid function.")
		else:
			try:
				diff(self.function_entry.get(), x)
				diff(self.function_entry.get(), y)
				diff(self.function_entry.get(), z)
				
				self.function_label_text.set(self.function_entry.get())
				self.function = self.function_entry.get()
				self.current_function = self.function_entry.get()
				self.function_entry.delete(0, tk.END)
			except TypeError:
				print("That is not a valid entry.")
		
		
	def diffx(self):	#df/dx
		"""Differentiate with respect to x"""
		self.current_function = diff(self.current_function, x)
		self.output_text.set(self.current_function)
	def diffxx(self):	#fxx
		self.output_text.set(diff(self.function, x, x))
	def diffxy(self):	#fxy	
		self.output_text.set(diff(self.function, x, y))
	def diffxz(self):	#fxz	
		self.output_text.set(diff(self.function, x, z))
	
	def diffy(self):	#df/dy
		"""Differentiate with respect to y"""	
		self.current_function = diff(self.current_function, y)
		self.output_text.set(self.current_function)
	def diffyy(self):	#fyy
		self.output_text.set(diff(self.function, y, y))
	def diffyz(self):	#fyz
		self.output_text.set(diff(self.function, y, z))
	
	def diffz(self):	#df/dz
		"""Differentiate with respect to z"""
		self.current_function = diff(self.current_function, z)
		self.output_text.set(self.current_function)
	def diffzz(self):	#fzz
		self.output_text.set(diff(self.function, z, z))
	
	def dx(self):
		"""Integrate the current function with respect to x"""
		self.current_function = integrate(self.current_function, x)
		self.output_text.set(self.current_function)
	def dy(self):
		"""Integrate the current function with respect to y"""
		self.current_function = integrate(self.current_function, y)
		self.output_text.set(self.current_function)
	def dz(self):
		"""Integrate the current function with respect to z"""
		self.current_function = integrate(self.current_function, z)
		self.output_text.set(self.current_function)
		
	def gradient(self):
		"""Calculate the gradient of the function"""
		gradient_text = "∇f=<" + str(diff(self.function, x))
		gradient_text += ", " + str(diff(self.function, y))
		gradient_text += ", " + str(diff(self.function, z)) + ">"
		self.output_text.set(gradient_text)
		
	def reset(self):	
		"""Reset the function to the original input given by the user"""
		self.current_function = self.function
		self.output_text.set(self.current_function)
root = tk.Tk()
#root['bg'] = "dark green"
newtons_gui = CalcCalculatorGUI(root)
# root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
root.iconbitmap('newton.ico')	#relax leibniz fans this isnt the permanent icon
root.mainloop()










