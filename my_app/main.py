from tkinter import*

#create the root widget 
root = Tk()
root.title("Desktop Summer App")


#create input widget 
item = Entry (root)
item.insert(0, "First Name: ")

#Radio Buttons 
var = IntVar()
Radiobutton(root, text="Option1",variable=var,value=1, command=lambda:rbutton(var.get())).grid(row=0,column=1)
Radiobutton(root, text="Option2",variable=var,value=2, command=lambda:rbutton(var.get())).grid(row=1,column=1)
Radiobutton(root, text="Option3",variable=var,value=3, command=lambda:rbutton(var.get())).grid(row=2,column=1)

def rbutton(value):
    labelR = Label(root,text=var.get())
    labelR.grid(row=4,column=0)



#Widget Packing 
item.grid(row=3, column=0)


root.mainloop()