from tkinter import *
from tkinter import ttk
from kenken import *
import time
import psutil
from random import random, shuffle, randint, choice

def setSize_Algorithm(s,a):
    global size
    global algorithm
    size=s
    algorithm=a
#--------------------------kenken puzzle---------------------------------
class MyPuzzle: 
    def __init__(self):
        cageList= generateCages(size)
        self.output = Kenken(size, cageList)

        if(algorithm=='1'):
                self.MyPuzzleSolution=csp.BTAlgorithm(self.output) 
 
        elif(algorithm=='2'):
            self.MyPuzzleSolution=csp.BTAlgorithm(self.output, filter="FC")

        elif(algorithm=='3'):
                self.MyPuzzleSolution=csp.BTAlgorithm(self.output, filter="AC3")       
          
        # prepare outputs to display in GUI
        self.guiCages,self.cages_background = parseCagesToGuiFormat(cageList)
        self.solutionGui=parseResultsToGuiFormat(self.MyPuzzleSolution)

    #to send result to the gui class
    def getResult(self):
        return self.solutionGui


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.MyPuzzle = MyPuzzle()                   
        self.guiCages = self.MyPuzzle.guiCages 
        self.cages_background = self.MyPuzzle.cages_background   
        self.canv = Canvas(master, width=size*70, height=size*70)
        self.canv.pack()
        self.secondWindowContent()   
        self.pack()

    def secondWindowContent(self):
        # Display kenken structure in GUI
        self.canv.create_rectangle(0, 0, size*70,size*70) 
        self.sqlist = []
        itr=0
        for i in range(0, size*70, 70):
            for j in range(0, size*70, 70):
                x = j + 70
                y = i + 70
                self.sqlist.append(self.canv.create_rectangle(j, i, x, y,fill=self.cages_background[itr]))
                itr+=1

        # Display cages in GUI
        x = 20
        y = 15
        i=0
        for element in self.guiCages:
            if i==size or i==2*size or i==3*size or i==4*size or i==5*size or i==size*6 or i==7*size or i==8*size or i==9*size: 
                x += 70
                y =15
            self.canv.create_text(x, y, font="Arial 9", text=element)
            y += 70
            i+=1

        # Display the solution in GUI
        self.MyPuzzleSolution = [[1 for x in range(size)] for y in range(size)]
        x = 35
        y = 35
        for m in range(len(self.MyPuzzleSolution)):
            for n in range(len(self.MyPuzzleSolution)):
                self.MyPuzzleSolution[m][n] = self.canv.create_text(x, y, font="Arial 20", text = '')
                y += 70
            y = 35
            x += 70
       
        #display buttons
        self.solveBtn = Button(self, text="Solve",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff")
        self.solveBtn.bind("<ButtonRelease-1>", self.solve)
        self.closeBtn = Button(self, text="Close",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff")
        self.closeBtn.bind("<ButtonRelease-1>", self.close)
        self.exitBtn = Button(self, text="Exit",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff")
        self.exitBtn.bind("<ButtonRelease-1>", self.exist)
         
        self.solveBtn.pack(side = LEFT, expand=YES,padx=12,pady=12)
        self.closeBtn.pack(side = LEFT, expand = YES,padx=12,pady=12)
        self.exitBtn.pack(side = LEFT, expand = YES,padx=12,pady=12)
        
    #close all game
    def exist(self, event):
        exit()        
        
    #display the solution in GUI
    def solve(self, event):
        solution = self.MyPuzzle.getResult()  
        for row in range(len(solution)):  
            for column in range(len(solution)):
                self.canv.itemconfigure(self.MyPuzzleSolution[row][column], text=solution[row][column])


    #close the solver window only
    def close(self, event):
      self.canv.delete('all') 
      window.destroy()

def calculateTime(generatedoutput,f):
    if(f=='none'):
        t=time.time()
        solution=csp.BTAlgorithm(generatedoutput) 
        t=time.time()-t
    else:
        t=time.time()
        solution=csp.BTAlgorithm(generatedoutput,filter=f) 
        t=time.time()-t
    return t


def boardGenerator():
    lines = []

    for i in range(100):
        lines.append("----------------Board "+str(i+1)+"--------------------")
        generatedSize=randint(3,8)
        generatedcageList= generateCages(generatedSize)
        generatedoutput = Kenken(generatedSize, generatedcageList)
        lines.append("Size = "+str(generatedSize))
        lines.append("BT Time: "+str(calculateTime(generatedoutput, "none")))
        lines.append("FC Time: "+str(calculateTime(generatedoutput, "FC")))
        lines.append("AC Time:"+str(calculateTime(generatedoutput, "AC3")))  

    with open('performance.txt', 'w') as f:
        f. truncate(0)
        f.write("\n".join(lines)) 
        print("Performace Analysis has been saved in performance.txt")


#-----------------------------Display GUI--------------------------------------
def main():
    #first window
    root = Tk()
    root.geometry('400x400')
    root.title("KENKEN Game")
    root.config(bg="#1b4a75")
    
    #second window
    def secondWindow():
        size=int(inputSize.get())
        algorithm =alg_choice.get()
        setSize_Algorithm(size,algorithm)
        getSize(size)

        global window
        window = Tk() 
        window.title("KenKen Solver")
        window.geometry(f"{size*100}x{size*100}")
        
        #make scroller
        main_frame=Frame(window)
        main_frame.pack(fill=BOTH,expand=1)
        my_canvas=Canvas((main_frame))
        my_canvas.pack(side=LEFT,fill=BOTH,expand=YES)

        yscroll=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
        yscroll.pack(side=RIGHT,fill=Y)
        my_canvas.configure(yscrollcommand=yscroll.set)

        my_canvas.bind('<Configure>',lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        second_frame=Frame(my_canvas)
        my_canvas.create_window((15*size,5),window=second_frame,anchor=NW)
        
        f = GUI(second_frame) 
        window.mainloop()

    #choose kenken size
    lable1= Label(root, text = "Size:",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff").place(x=5,y=10)
    inputSize=Entry(root,width=15)
    inputSize.place(x=50,y=13)

    #choose algorithm
    label2= Label(root, text = "Algorithm: Backtracking",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff").place(x=5,y=70)
    lable3= Label(root, text = "Filter:",font=("Arial",10,"bold"),bg="#1b4a75",fg="#fff").place(x=5,y=120)
    alg_choice = StringVar(root,"1")
    values = {"None": "1",
            "Forward Checking": "2",
            "Arc Consistency": "3"}
    itr=0
    for (text, value) in values.items():
        Radiobutton(root, text = text, variable= alg_choice,font=("Arial",10),value = value,
        bg="#1b4a75",fg="#fff",activebackground="#1b4a75",activeforeground="#fff",selectcolor="#1b4a75").place(x=60,y=120+itr)
        itr+=40
    
    #diplay button
    generateBtn = Button(root, text = 'Generate',font=("Arial",10,"bold"),command = secondWindow).place(x=170,y=300)
    root.mainloop()

if __name__ == "__main__":
    #boardGenerator()
    main()
