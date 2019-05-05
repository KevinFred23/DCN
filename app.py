from tkinter import *
import tkinter as tk
import tkinter.messagebox

class fletcher_csum(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (f1,f2,f3):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("f1")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class f1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text='Fletcher Checksum', fg="white", bg="black", font=("Times New Roman", 40), relief=RAISED, height=5, width=10).pack(side="top", fill=X, pady=10)
        tk.Button(self, text="Sender",command=lambda: controller.show_frame("f2")).pack(side="right")
        tk.Button(self, text="Receiver", command=lambda: controller.show_frame("f3")).pack(side="left")

class f2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text='Message :').grid(row=0, column=0, padx=5, pady=5, sticky=W)


        global message
        message = tk.Text(self, wrap=WORD, width=60, height=10, state=NORMAL, relief=RAISED, insertofftime=0)
        message.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text='Generate', command=lambda: self.fletcher_checksum(message)).grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)
        tk.Button(self, text='Back', command=lambda: controller.show_frame("f1")).grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

    def fletcher_checksum(self,msg):
        msg = msg.get('1.0', 'end-1c')
        w = list(map(hex,list(map(ord,list(msg)))))
        dw = ""
        c1 = c2 = 0
        for i in w:
            dw += i[2:]
            c1 += int(i[2:],16)
            c2 += c1
        c1 %= 255
        c2 %= 255
        tk.Label(self, text='Checksum :').grid(row=3, column=0, padx=5, pady=5, sticky=W)
        tk.Label(self, text='CodeWord :').grid(row=5, column=0, padx=5, pady=5, sticky=W)
        global fbtext
        fbtext = StringVar()
        fbtext.set(hex(c1)[2:]+hex(c2)[2:])
        tk.Entry(self, textvariable=fbtext, width=30, insertofftime=0).grid(row=3, column=1, padx=5, pady=5, sticky=W)
        global cbxt
        cbxt = StringVar()
        cbxt.set(dw+hex(c1)[2:]+hex(c2)[2:])
        tk.Entry(self, textvariable=cbxt, width=100, insertofftime=0).grid(row=5, column=1, padx=5, pady=5, sticky=W)

class f3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text='Received Codeword :').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        global code
        code = StringVar()
        tk.Entry(self, textvariable=code, width=30, insertofftime=0).grid(row=0, column=1, padx=5, pady=5, sticky=W)
        tk.Button(self, text='Decode', command=lambda: self.check(code)).grid(row=4, column=0, padx=5,pady=5, sticky=N + S + E + W)
        tk.Button(self, text='Back', command=lambda: controller.show_frame("f1")).grid(row=4, column=2, padx=5, pady=5, sticky=N + S + E + W)
    def check(self,word):
        word = word.get()
        s1 = s2 = 0
        l = []
        for i in range(0,len(word)-4,2):
            x = int(word[i:i+2],16)
            s1 += x
            s2 += s1
            l.append(x)
        if (s1%255) == int(word[-4:-2],16) and (s2%255) == int(word[-2:],16):
            tkinter.messagebox.showinfo("Check Complete", "Correct Message received")
            tk.Label(self, text='status : CORRECT MESSAGE RECEIVED',fg = "green").grid(row=1, column=0, padx=5, pady=5, sticky=W)
            self.gen_mes(l)
        else:
            tkinter.messagebox.showerror("Check Complete","Wrong Message received")
            tk.Label(self, text="STATUS: WRONG MESSAGE RECEIVED",fg = "red").grid(row=1, column=0, padx=5, pady=5, sticky=W)
            label.destroy()

    def gen_mes(self,l):
        s = ""
        s = "".join([chr(c) for c in l])
        tk.Label(self, text='Decoded Message :').grid(row=2, column=0, padx=5, pady=5, sticky=W)
        var = StringVar()
        global label
        label = Message(self, textvariable=var, relief=RAISED, bg = "black",fg = "white")
        var.set(s)
        label.grid(row=2, column=1, padx=5, pady=5,sticky=W)

if __name__ == "__main__":
    app = fletcher_csum()
    app.mainloop()