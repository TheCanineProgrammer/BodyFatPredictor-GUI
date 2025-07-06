from tkinter import *
from tkinter import messagebox as mb
from tkinter.filedialog import *
from sklearn.tree import DecisionTreeRegressor
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

window = Tk()
window.title("welcome screen".title())
window.geometry("400x200")
window.resizable(False, False)
data = pd.read_csv('data.csv')
X = np.column_stack((data['Weight'].to_numpy() / 2.2046244201837775, data['Height'].to_numpy() / 38.20786239358456 * 100, data['Age'].to_numpy()))
X = np.vstack((X, np.array([[57.6, 167, 13]]), np.array([[73, 163, 52]])))
y = data['BodyFat'].to_numpy()
y = np.hstack((y, np.array([21.9, 36.7])))
dt = DecisionTreeRegressor(max_depth = 20)
dt.fit(X, y)
info = {}
con = sqlite3.connect('server.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS bodyfat(id TEXT, weight TEXT, height TEXT, age TEXT, BMI TEXT, fat real)')
con.commit()
def Register():
    global con, cur
    global window
    window.destroy()
    win1 = Tk()
    win1.geometry('400x170')
    win1.title('register'.title())
    win1.resizable(False, False)
    L2 = Label(win1, text = 'Your ID:', font = ('helvetica', 15))
    L2.grid(row = 1, column = 0)
    E1 = Entry(win1, width = 20, bd = 4)
    E1.focus_set()
    info['ID'] = str(E1.get())
    E1.grid(row = 1, column = 1)
    L3 = Label(win1, text = 'Your weight(Kilo):', font = ('helvetica', 15))
    L3.grid(row = 2, column = 0)
    E2 = Entry(win1, width = 20, bd = 4)
    info['Weight'] = str(E2.get())
    E2.grid(row = 2, column = 1)
    L4 = Label(win1, text = 'Your Height(meters):', font = ('helvetica', 15))
    L4.grid(row = 3, column = 0)
    E3 = Entry(win1, width = 20, bd = 4)
    info['Height'] = str(E3.get())
    E3.grid(row = 3, column = 1)
    L5 = Label(win1, text = 'Your age:', font = ('helvetica', 15))
    L5.grid(row = 4, column = 0)
    E4 = Entry(win1, width = 20, bd = 4)
    info['Age'] = str(E4.get())
    E4.grid(row = 4, column = 1)
    def reg():
        if E1.get() == '' or E2.get() == '' or E3.get() == '' or E4.get() == '':
            mb.showerror('Error!', 'You should fill all the entries!')
        else:    
            cur.execute(('SELECT * FROM bodyfat WHERE id = ?'), [(E1.get())])
            if cur.fetchall():
                mb.showerror('Error!', 'The ID is already taken!')
            else:
                info['ID'] = str(E1.get())
                info['Weight'] = str(E2.get())
                info['Height'] = str(E3.get())
                if eval(info['Height']) < 4:
                    info['Height'] = eval(info['Height']) * 100
                elif eval(info['Height']) > 4:
                    info['Height'] = eval(info['Height'])
                info['Age'] = str(E4.get())
                if float(info['Height']) < 4:
                    info['BMI'] = float(info['Weight']) / float(info['Height']) ** 2
                elif float(info['Height'])> 4:
                    info['BMI'] = float(info['Weight']) / ((float(info['Height']) / 100) ** 2)
                datatup = []
                for _, v in info.items():
                    datatup.append(v)
                ypred = float(dt.predict(np.array([float(info['Weight']), float(info['Height']), float(info['Age'])]).reshape(1, -1)))
                #print(ypred)
                datatup.append(ypred)
                cur.execute('INSERT INTO bodyfat values(?,?,?,?,?,?)', tuple(datatup))
                con.commit()
                win1.destroy()
                win2 = Tk()
                win2.title('Login')
                win2.geometry('250x100')
                win2.resizable(False, False)
                lbl = Label(win2, text = 'Your ID:', font = ('Helvetica', 15))
                lbl.grid(row = 0, column = 0)
                E5 = Entry(win2, width = 20, bd = 4)
                E5.focus_set()
                E5.grid(row = 0, column = 1)
                def log():
                    cur.execute(('SELECT * FROM bodyfat WHERE id = ?'), [(E5.get())])
                    fetch = cur.fetchall()
                    if fetch:
                        result = []
                        for i in fetch:
                            lst = i
                        for j in lst:
                            result.append(j)
                        #result.append(ann.predict(np.array([float(result[1]), float(result[2]), int(result[3])]).reshape(1, -1)))
                        win2.destroy()
                        win3 = Tk()
                        win3.geometry("500x300")
                        win3.title("Info")
                        win3.resizable(False, False)
                        lbl1 = Label(win3, text = 'Your info:', font = ('Consolas', 20))
                        lbl1.pack()
                        lbl2 = Label(win3, text = f'Your ID: {result[0]}')
                        lbl2.pack()
                        lbl3 = Label(win3, text = f'Your weight: {result[1]}')
                        lbl3.pack()
                        lbl4 = Label(win3, text = f'Your height: {result[2]}')
                        lbl4.pack()
                        lbl5 = Label(win3, text = f'Your age: {result[3]}')
                        lbl5.pack()
                        if eval(result[4]) < 18.5:
                            lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Underweight')
                            lbl6.pack()
                        elif eval(result[4]) >= 18.5 and eval(result[4]) < 25:
                            lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Normal')
                            lbl6.pack()
                        elif eval(result[4]) >= 25 and eval(result[4]) < 30:
                            lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Overweight')
                            lbl6.pack()
                        elif eval(result[4]) >= 30:
                            lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Obese')
                            lbl6.pack()
                        lbl7 = Label(win3, text = f'Your fatness: {round(result[5], 3)}%')
                        lbl7.pack()
                        def excel():
                            lst = []
                            lst.append(result[0])
                            for i in result[1:6]:
                                lst.append(round(float(i), 2))
                            '''for j in result[-1]:
                                lst.append(round(j, 2))'''
                            file = asksaveasfilename(defaultextension = '.xlsx', filetypes = [('excel file', '.xlsx')], confirmoverwrite = True)
                            df = pd.DataFrame(lst, columns = ['info'], index = ['ID', 'Weight', 'Height', 'Age', 'BMI', 'Fatness'])
                            if file:
                                writer = pd.ExcelWriter(file, engine = 'xlsxwriter')
                                df.to_excel(writer, 'Sheet1')
                                writer.save()
                        def plot():
                            win3.geometry('600x700')
                            fig, ax = plt.subplots()
                            ax.scatter(X[:, 2], y, c = ['r'], edgecolor= ['k'], label = 'Samples')
                            ax.scatter(eval(result[3]), result[-1], c = ['orange'], edgecolor = ['k'], label = 'You')
                            ax.scatter(eval(result[3]), result[-1], facecolor = ['none'], edgecolor = ['k'], s = 200)
                            plt.vlines(x = eval(result[3]), ymin = -15, ymax = result[-1], lw = 0.9,
                                        linestyle = '--', color = 'grey')
                            plt.hlines(y = result[-1], xmin = 0, xmax = eval(result[3]), lw = 0.9,
                                        linestyle = '--', color = 'grey')
                            plt.annotate('', xy = (eval(result[3]), result[-1]), 
                                            xytext = (eval(result[3]), result[-1]-10), fontsize = 12,
                                            xycoords = 'data',
                                            arrowprops = {'connectionstyle' : 'arc3, rad = 0.5',
                                             'facecolor' : 'silver', 'width' : 4})
                            plt.xlim(0)
                            plt.ylim(-5, 60)
                            ax.set_title('Body Fat Prediction')
                            ax.set_xlabel('Age', loc = 'right')
                            ax.set_ylabel('Body fat')
                            ax.legend()
                            canvas = FigureCanvasTkAgg(fig, master = win3)
                            canvas.draw()
                            toolbar = NavigationToolbar2Tk(canvas, win3)
                            toolbar.update()

                            canvas.get_tk_widget().pack()


                        btn9 = Button(win3, text = 'Save your data as an excel file', cursor = 'hand2', font = ('Arial', 16), command = excel)
                        btn9.pack()
                        btn10 = Button(win3, text = 'Show chart', cursor = 'hand2', font = ('Arial', 16), command = plot)
                        btn10.pack()
                        win3.mainloop()
                    else:
                        mb.showerror("Error!", "ID not found!")
                btn4 = Button(win2, text = 'Login', cursor = 'hand2', font = ('Arial', 16), command = log)
                btn4.grid(row = 1, column = 1)
                win2.mainloop()

            

    btn3 = Button(win1, text = 'Register', cursor = 'hand2', font = ('Arial', 16), command = reg)
    btn3.grid(row = 5, column = 1, pady = 5)
    win1.mainloop()

def LOGIN():
    global X
    global y
    window.destroy()
    win6 = Tk()
    win6.title("Login")
    win6.geometry("250x100")
    win6.resizable(False, False)
    lbl = Label(win6, text = 'Your ID:', font = ('Helvetica', 15))
    lbl.grid(row = 0, column = 0)
    E = Entry(win6, width = 20, bd = 4)
    E.focus_set()
    E.grid(row = 0, column = 1)
    def LOG():
        cur.execute(('SELECT * FROM bodyfat WHERE id = ?'), [(E.get())])
        fetch = cur.fetchall()
        if fetch:
            result = []
            for i in fetch:
                lst = i
            for j in lst:
                result.append(j)
            #result.append(ann.predict(np.array([float(result[1]), float(result[2]), int(result[3])]).reshape(1, -1)))
            
            win6.destroy()
            win3 = Tk()
            win3.geometry("500x300")
            win3.title("Info")
            win3.resizable(False, False)
            lbl1 = Label(win3, text = 'Your info:', font = ('Consolas', 20))
            lbl1.pack()
            lbl2 = Label(win3, text = f'Your ID: {result[0]}')
            lbl2.pack()
            lbl3 = Label(win3, text = f'Your weight: {result[1]}')
            lbl3.pack()
            lbl4 = Label(win3, text = f'Your height: {result[2]}')
            lbl4.pack()
            lbl5 = Label(win3, text = f'Your age: {result[3]}')
            lbl5.pack()
            if eval(result[4]) < 18.5:
                lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Underweight')
                lbl6.pack()
            elif eval(result[4]) >= 18.5 and eval(result[4]) < 25:
                lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Normal')
                lbl6.pack()
            elif eval(result[4]) >= 25 and eval(result[4]) < 30:
                lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Overweight')
                lbl6.pack()
            elif eval(result[4]) >= 30:
                lbl6 = Label(win3, text = f'Your BMI: {round(eval(result[4]), 3)} - Status : Obese')
                lbl6.pack()
            lbl7 = Label(win3, text = f'Your fatness: {round(result[5], 3)}%')
            lbl7.pack()
            def excel():
                lst = []
                lst.append(result[0])
                for i in result[1:6]:
                    lst.append(round(float(i), 2))
                '''for j in result[-1]:
                    lst.append(round(j, 2))'''
                file = asksaveasfilename(defaultextension = '.xlsx', filetypes = [('excel file', '.xlsx')], confirmoverwrite = True)
                df = pd.DataFrame(lst, columns = ['info'], index = ['ID', 'Weight', 'Height', 'Age', 'BMI', 'Fatness'])
                if file:
                    writer = pd.ExcelWriter(file, engine = 'xlsxwriter')
                    df.to_excel(writer, 'Sheet1')
                    writer.close()
            def plot():
                win3.geometry('600x700')
                fig, ax = plt.subplots()
                ax.scatter(X[:, 2], y, c = ['r'], edgecolor= ['k'], label = 'samples')
                ax.scatter(eval(result[3]), result[-1], c = ['orange'], edgecolor = ['k'], label = 'You')
                ax.scatter(eval(result[3]), result[-1], facecolor = ['none'], edgecolor = ['k'], s = 200)
                plt.vlines(x = eval(result[3]), ymin = -50, ymax = result[-1], lw = 0.9,
                             linestyle = '--', color = 'grey')
                plt.hlines(y = result[-1], xmin = -50, xmax = eval(result[3]), lw = 0.9,
                            linestyle = '--', color = 'grey')
                plt.annotate('', xy = (eval(result[3]), result[-1]), 
                                xytext = (eval(result[3]), result[-1] + 10), fontsize = 12,
                                xycoords = 'data',
                                 arrowprops = {'connectionstyle' : 'arc3, rad = 0.5',
                                 'facecolor' : 'silver', 'width' : 4})
                plt.xlim(0)
                plt.ylim(-5, 60)
                ax.set_title('Body Fat Prediction')
                ax.set_xlabel('Age', loc = 'right')
                ax.set_ylabel('Body fat')
                ax.legend()
                canvas = FigureCanvasTkAgg(fig, master = win3)
                canvas.draw()
                toolbar = NavigationToolbar2Tk(canvas, win3)
                toolbar.update()

                canvas.get_tk_widget().pack()

            btn9 = Button(win3, text = 'Save your info as an excel file', cursor = 'hand2', font = ('Arial', 16), command = excel)
            btn9.pack()
            btn10 = Button(win3, text = 'Show chart', cursor = 'hand2', font = ('Arial', 16), command = plot)
            btn10.pack()
            win3.mainloop()
        else:
            mb.showerror("Error!", "ID not found!")
    button = Button(win6, text = 'Login', cursor = 'hand2', font = ('Arial', 16),  command = LOG)
    button.grid(row = 1, column = 1)
    win6.mainloop()

def on_close():
    con.close()
    window.destroy()

L1 = Label(window, text = 'Welcome!', justify=CENTER, font = ('helvetica', 30, 'bold'))
L1.pack()
btn1 = Button(window, text = 'Register', cursor = 'hand2', font = ('Arial', 15), command = Register)
btn1.pack(pady = 20, anchor=CENTER)
btn2 = Button(window, text = 'Login', cursor = 'hand2', font = ('Arial', 15), command = LOGIN)
btn2.pack()
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()