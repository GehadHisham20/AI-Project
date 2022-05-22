from tkinter import *

root = Tk()
root.geometry('700x700')
# root.columnconfigure(0, minsize=250)
# root.rowconfigure([0, 1], minsize=100)
root.title("KENKEN Game")
# def KENKEN_Construct(start_boarder_x, start_boarder_y, end_boarder_x, end_boarder_y, kenken_order):
#     canvas = Canvas(root, height=500, width=500)
#     canvas.create_rectangle(start_boarder_x, start_boarder_y, end_boarder_x, end_boarder_y)
#     canvas.create_rectangle(
#     (start_boarder_x + (end_boarder_x - start_boarder_x)/kenken_order), start_boarder_y,
#     start_boarder_x + 2*(end_boarder_x - start_boarder_x) / kenken_order, end_boarder_y)
#
#     canvas.create_rectangle(    start_boarder_x, start_boarder_y+(end_boarder_y-start_boarder_y)/kenken_order,
#     end_boarder_x, start_boarder_y+2*(end_boarder_y-start_boarder_y)/kenken_order)
#     canvas.pack()
#####################choose puzzle size############################
def test(a):
    a = clicked.get()
    print(a)
puzzleSize= Label(root, text = "Size:",font=("Arial",10))
puzzleSize.pack()
options = [
    "3x3",
    "4x4",
    "5x5",
    "6x6",
    "7x7",
    "8x8",
    "9x9"
]
clicked = StringVar()
clicked.set("3x3")
drop = OptionMenu(root, clicked, *options)
drop.pack()

#################### choose algorithm #####################
algo= Label(root, text = "Algorithm:",font=("Arial",10))
algo.pack()
v = StringVar(root, "1")
values = {"Backtracking": "1",
          "Backtracking with forward checking": "2",
          "Backtracking with forward checking and arc consistency": "3"}
for (text, value) in values.items():Radiobutton(root, text = text, variable= v,font=("Arial",10),
        value = value).pack()



#KENKEN_Construct(100, 100, 400, 400, 3)
btn = Button(root, text = 'Click me !',
                command = test).pack()





root.mainloop() #placewindow on computer screen and listen for eventss




