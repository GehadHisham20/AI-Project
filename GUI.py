class TheGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.kenken = KenKen()                   
        self.puzzles = self.kenken.puzzlelist 
        self.backgrounds = self.kenken.backgrounds   
        self.w = Canvas(master, width=size*70, height=size*80)
        self.w.pack()
        self.create_widgets()   
        self.pack()

    def create_widgets(self):
        # Display kenken structure in GUI
        self.w.create_rectangle(3, 3, size*70,size*70) 
        self.sqlist = []
        itr=0
        for i in range(0, size*70, 70):
            for j in range(0, size*70, 70):
                x = j + 70
                y = i + 70
                self.sqlist.append(self.w.create_rectangle(j, i, x, y,fill=self.backgrounds[itr]))
                itr+=1

        # Display cages in GUI
        x = 20
        y = 15
        i=0
        for element in self.puzzles:
            if i==size or i==2*size or i==3*size or i==4*size or i==5*size or i==size*6 or i==7*size or i==8*size or i==9*size: 
                y += 70
                x =20
            self.w.create_text(x, y, font="Arial 9 bold", text=element)
            x += 70
            i+=1

        # Display the results in GUI
        self.numbers = [[1 for x in range(size)] for y in range(size)]
        x = 35
        y = 35
        for m in range(len(self.numbers)):
            for n in range(len(self.numbers)):
                self.numbers[m][n] = self.w.create_text(x, y, font="Arial 20", text = '')
                y += 70
            y = 35
            x += 70

        #----------------------------buttons------------------------------------
        self.buttonlist = []
        self.btn_solve = Button(self, text="Solve",font=("Arial",10,"bold"))
        self.btn_solve.bind("<ButtonRelease-1>", self.solve)
        self.btn_close = Button(self, text="Close",font=("Arial",10,"bold"))
        self.btn_close.bind("<ButtonRelease-1>", self.close)
        self.btn_exit = Button(self, text="Exit",font=("Arial",10,"bold"))
        self.btn_exit.bind("<ButtonRelease-1>", self.click_Exit)

        self.btn_solve.pack(side = LEFT, fill = Y, expand=YES,padx=12)
        self.btn_close.pack(side = LEFT, fill = Y, expand = YES,padx=12)
        self.btn_exit.pack(side = LEFT, fill = Y, expand = YES,padx=12)

        self.buttonlist.append(self.btn_solve)
        self.buttonlist.append(self.btn_exit)
        self.buttonlist.append(self.btn_close)

    #close all game
    def click_Exit(self, event):
        exit()
        
    #display the solution in GUI
    def solve(self, event):
        solution = self.kenken.getResult()  
        for row in range(len(solution)):  
            for column in range(len(solution)):
                self.w.itemconfigure(self.numbers[row][column], text=solution[row][column]) 

    #close the solver window only
    def close(self, event):
      self.w.delete('all') 
      window.destroy()
       
#-----------------------------main GUI--------------------------------------
#Starts up the game
def main():
    root = Tk()
    root.geometry('400x400')
    root.title("KENKEN Game")
    #second window
    def secondWindow():
        global window
        window = Tk() 
        window.title("KenKen Game")
        size=options[clicked.get()]
        algorithm =alg_choice.get()
        setSize_Algorithm(size,algorithm)
        getSize(size)
        window.geometry(f"{size*100}x{size*110}")
        f = TheGUI(window) 
        window.mainloop()


    #---------------------choose kenken size--------------------------
    lable1= Label(root, text = "Size:",font=("Arial",10,"bold")).place(x=5,y=10)
    options = {
        "3x3":3,
        "4x4":4,
        "5x5":5,
        "6x6":6,
        "7x7":7,
        "8x8":8,
        "9x9":9
    }
    clicked = StringVar()
    clicked.set("3x3")
    drop = OptionMenu(root, clicked, *options).place(x=50,y=5)

    #----------------------- choose algorithm --------------------------
    label2= Label(root, text = "Algorithm: Backtracking",font=("Arial",10,"bold")).place(x=5,y=70)
    lable3= Label(root, text = "Filter:",font=("Arial",10,"bold")).place(x=5,y=120)
    alg_choice = StringVar(root,"1")
    values = {"None": "1",
            "Forward Checking": "2",
            "Forward Checking + Arc Consistency": "3"}
    itr=0
    for (text, value) in values.items():
        Radiobutton(root, text = text, variable= alg_choice,font=("Arial",10),value = value).place(x=60,y=120+itr)
        itr+=40

    generateBtn = Button(root, text = 'Generate',font=("Arial",10,"bold"),command = secondWindow).place(x=170,y=300)
    root.mainloop()



if __name__ == "__main__":
    main()



