import tkinter as tk

class InputLabel(tk.Label):
    def __init__(self, window):
        self.fontsize = 9
        self.enter = tk.StringVar(value='')
        super().__init__(window, textvariable=self.enter, relief='sunken', cursor='xterm', font=("Courier", self.fontsize+2), highlightthickness=1)
        
        self.bind('<Key>', func=self.process_entering)
        self.bind('<Button-1>', func=self.process_mouse)

        self.grid(column=0, row=0, sticky='news')
        
        
        self.pos = 0
        self.cursor = tk.Frame(self, height=20, width=2, background="grey")
        self.looping()
        
    def looping(self):
        self.master.after(500, self.looping)

    
    def cursor_pos(self, newpos):
        self.pos = newpos
        self.pos = max(self.pos, 0)
        self.pos = min(self.pos, len(self.enter.get()))
        self.cursor.place(x=self.pos*self.fontsize, y=1)
        
    def delete(self):
        left = self.enter.get()[:self.pos][:-1]
        right = self.enter.get()[self.pos:]
        self.enter.set(left + right)
        self.cursor_pos(self.pos-1)

    def add(self, char):
        left = self.enter.get()[:self.pos]
        right = self.enter.get()[self.pos:]
        self.enter.set(left + char + right)
        self.cursor_pos(self.pos+1)
    
    def add_symb(self, enter):
    	if enter.isprintable():
            self.add(enter)
    
    def process_entering(self, event):
        if event.keysym == 'BackSpace':
            self.delete()
        elif event.keysym == 'Left':
            self.cursor_pos(self.pos-1)
        elif event.keysym == 'Right':
            self.cursor_pos(self.pos+1)
        elif event.keysym == 'Home':
            self.cursor_pos(0)
        elif event.keysym == 'End':
            self.cursor_pos(len(self.string.get()))
        elif event.char:
            self.add_symb(event.char)
            
    
    def process_mouse(self, event):
        self.focus()
        self.cursor_pos(event.x // self.fontsize)
            
window = tk.Tk()
window.title("StringEditor")

quit_btn = tk.Button(window, text='Quit', command=lambda: window.destroy())
quit_btn.grid(row=1, sticky='news')
inputlabel = InputLabel(window)

window.mainloop()
