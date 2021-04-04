import tkinter as tk
import re


class App(tk.Frame):
    def __init__(self, master=None, title="oval", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.master)
        self.frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.text = tk.Text(self.frame)
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row=0, column=1, sticky=tk.NSEW)

        self.text.bind("<KeyRelease>", self.text_click)
        self.text.tag_config("error", background="red", selectbackground="#ff0077")
        self.canvas.bind("<Button-1>", self.painting_oval)
        self.canvas.bind("<Double-Button-1>", self.painting_oval)
        self.canvas.bind("<Motion>", self.canvas_move)
        self.canvas.bind("<ButtonRelease-1>", self.draw)
        self.creating_flag = False
        self.moving_flag = False
        self.coord_x, self.coord_y = 0, 0
        self.oval = None
        self.reg = r"#[0123456789a-fA-F]{6}"

    def check_correction_line(self, text):
        line = text.replace("<", "")
        line = line.replace(">", "")
        match_line = line.split()
        if match_line:
            if match_line[0] == "oval":
                return None
            if (
                len(match_line) == 8
                and len(match_line[-1]) == 7
                and len(match_line[-2]) == 7
                and (
                    not re.match(self.reg, match_line[-1])
                    or not re.match(self.reg, match_line[-2])
                )
            ):
                return None
            [int(elem) for elem in match_line[1:6]]
        return match_line

    def painting_oval(self, event):
        self.coord_x, self.coord_y = event.x, event.y
        ovals = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if ovals:
            self.oval = ovals[-1]
            self.canvas.tag_raise(self.oval)
            self.moving_flag = True
        else:
            self.oval = self.canvas.create_oval(
                event.x,
                event.y,
                event.x,
                event.y,
                fill="#DC143C",
                outline="#FFA07A",
                width=1,
            )
            self.creating_flag = True

    def draw(self, _):
        self.creating_flag = False
        self.moving_flag = False
        self.update_text()

    def create(self, event):
        x0, y0, x1, y1 = self.coord_x, self.coord_y, event.x, event.y
        self.canvas.coords(self.oval, x0, y0, x1, y1)

    def move(self, event):
        self.canvas.move(self.oval, event.x - self.coord_x, event.y - self.coord_y)
        self.coord_x, self.coord_y = event.x, event.y

    def canvas_move(self, event):
        if self.creating_flag:
            self.create(event)
        elif self.moving_flag:
            self.move(event)

    def text_click(self, event):
        self.canvas.delete("all")
        self.text.tag_remove("error", "0.0", tk.END)
        input_description = self.text.get("1.0", "end-1c").splitlines()
        for i, line in enumerate(input_description):
            match_line = self.check_correction_line(line)
            if match_line:
                fig_type, x0, y0, x1, y1, width, fill, outline = match_line
                self.canvas.create_oval(
                    x0, y0, x1, y1, fill=fill, outline=outline, width=width
                )
            else:
                self.text.tag_add("error", f"{i + 1}.0", f"{i + 1}.end")

    def made_text(self, oval, x0, y0, x1, y1):
        return (
            f"oval <{x0} {y0} {x1} {y1}> "
            + f"{self.canvas.itemcget(oval, 'width')[:-2]} {self.canvas.itemcget(oval, 'outline')} "
            + f"{self.canvas.itemcget(oval, 'fill')}\n"
        )

    def update_text(self):
        self.text.delete("0.0", tk.END)
        for oval in self.canvas.find_all():
            x0, y0, x1, y1 = [int(x) for x in self.canvas.coords(oval)[:4]]
            text = self.made_text(oval, x0, y0, x1, y1)
            self.text.insert("end", text)


if __name__ == "__main__":
    app = App(title="oval")
    app.mainloop()
