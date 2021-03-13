import tkinter
import tkinter.messagebox

class Main(tkinter.Frame):
    """Класс главного окна"""

    def __init__(self, root):
        """Конструктор главного окна

        Вызывает метод инициализации из родительского класса, передавая root.
        Вызвает методы построения условных блоков графики.

        """
        super().__init__(root)
        self.hand = tkinter.BooleanVar()
        self.alphabet = tkinter.StringVar()
        self.step = tkinter.StringVar()
        self.hand.set(1)
        self.alphabet.set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ,.:;!?0123456789")
        self.step.set("1")
        self.buttons = []
        self._create_settings_bar()
        self._create_work_place()
        self._create_bottom()

    def _create_settings_bar(self):
        settings_bar = tkinter.Frame(bg="#f2f2f2", bd=3)
        settings_bar.pack(side=tkinter.TOP, fill=tkinter.X)

        tkinter.Label(
            settings_bar, bg="#f2f2f2", bd=3,
            text="Алфавит:", relief="flat").pack(side=tkinter.LEFT)

        self.alphabet_entry = tkinter.Entry(
            settings_bar, width=64,
            textvariable=self.alphabet, bg="#f2f2f2", bd=3)
        self.alphabet_entry.pack(side=tkinter.LEFT, anchor=tkinter.NW)

        tkinter.Label(
            settings_bar, width=3, bg="#f2f2f2").pack(side=tkinter.LEFT)
        tkinter.Label(
            settings_bar, bg="#f2f2f2", bd=3,
            text="Смещение:", relief="flat").pack(side=tkinter.LEFT)

        tkinter.Radiobutton(
            settings_bar, text="Влево", indicatoron=True,
            value=0, bg="#f2f2f2", highlightthickness=0,
            variable=self.hand).pack(side=tkinter.LEFT)
        tkinter.Radiobutton(
            settings_bar, text="Вправо", indicatoron=True,
            value=1, bg="#f2f2f2", highlightthickness=0,
            variable=self.hand).pack(side=tkinter.LEFT)

        tkinter.Label(
            settings_bar, width=3, bg="#f2f2f2").pack(side=tkinter.LEFT)
        tkinter.Label(
            settings_bar, bg="#f2f2f2", bd=3,
            text="Шаг смещения:", relief="flat").pack(side=tkinter.LEFT)

        self.step_entry = tkinter.Entry(
            settings_bar, width=3,
            textvariable=self.step, bg="#f2f2f2", bd=3)
        self.step_entry.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        self.step_entry.bind("<Key>", self._check_keys)

    def _create_work_place(self):
        work_place = tkinter.Frame(bg="#f2f2f2", bd=3)
        work_place.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

        self.text_field_1 = tkinter.Text(
            work_place, bg="#ffffff",
            highlightthickness=0, wrap="word")
        self.text_field_1.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        arrows = tkinter.Frame(work_place, bg="#f2f2f2", bd=3)
        arrows.pack(side=tkinter.LEFT)

        self.icon = tkinter.PhotoImage(file="icons/arrow_r.png")
        tool_button = tkinter.Button(
            arrows, bg="#f2f2f2", bd=0,
            compound=tkinter.TOP, image=self.icon,
            highlightthickness=0)
        tool_button.pack(side=tkinter.TOP)
        tool_button.bind('<Button-1>', self._cypher)
        self.buttons.append(tool_button)

        self.icon_2 = tkinter.PhotoImage(file="icons/arrow_l.png")
        tool_button = tkinter.Button(
            arrows, bg="#f2f2f2", bd=0,
            compound=tkinter.TOP, image=self.icon_2,
            highlightthickness=0)
        tool_button.pack(side=tkinter.TOP)
        tool_button.bind('<Button-1>', self._cypher)
        self.buttons.append(tool_button)

        self.text_field_2 = tkinter.Text(
            work_place, bg="#ffffff",
            highlightthickness=0, wrap="word")
        self.text_field_2.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def _create_bottom(self):
        bottom = tkinter.Frame(bg="#f2f2f2", bd=3)
        bottom.pack(side=tkinter.TOP, fill=tkinter.X)

        tkinter.Label(
            bottom, bg="#f2f2f2", bd=0,
            text="© 2021 Copyright Poleno", relief="flat").pack(side=tkinter.TOP)

    def _check_keys(self, event):
        if (event.char not in "0123456789" and
                event.keysym != "BackSpace"):
            return "break"
        if len(self.step.get()) == 0 and event.char == '0':
            return "break"

    def _get_string(self, widget):
        string = widget.get(1.0, tkinter.END)
        string = string.strip('\n')
        string = string.strip()
        string = string.replace("\n", " ")
        string = string.replace("  ", " ")
        return string

    def _check(self, widget):
        if len(self.alphabet.get()) == 0:
            tkinter.messagebox.showerror("Ошибка", "Алфавит пуст.")
            return False
        elif len(self.step.get()) == 0:
            tkinter.messagebox.showerror("Ошибка", "Шаг смещения пуст.")
            return False
        elif widget == self.buttons[0]:
            string = self._get_string(self.text_field_1)
            for char in string:
                if char not in self.alphabet.get():
                    tkinter.messagebox.showerror("Ошибка", "Используется внеалфавитный символ: "+char)
                    return False
        elif widget == self.buttons[1]:
            string = self._get_string(self.text_field_2)
            for char in string:
                if char not in self.alphabet.get():
                    tkinter.messagebox.showerror("Ошибка", "Используется внеалфавитный символ: "+char)
                    return False
        return True

    def _set_text(self, text, widget):
        if self.buttons[0] == widget:
            widget = self.text_field_2
        elif self.buttons[1] == widget:
            widget = self.text_field_1

        widget.delete("%d.%d" % (1,0), tkinter.END)
        widget.insert("%d.%d" % (1,0), text)

    def _cypher(self, event):
        if self._check(event.widget):
            i1 = 0
            i2 = 0
            encode = ""
            dict = {self.buttons[0]: self.text_field_1, self.buttons[1]: self.text_field_2}
            if (event.widget == self.buttons[0] and not self.hand.get()) or (event.widget == self.buttons[1] and self.hand.get()):
                for index, char in enumerate(self._get_string(dict[event.widget])):
                    alph = self.alphabet.get()
                    index: int = (alph.find(char) + int(self.step.get())*i1) % len(alph)
                    i1+=1
                    encode += alph[index]
            if (event.widget == self.buttons[0] and self.hand.get()) or (event.widget == self.buttons[1] and not self.hand.get()):
                for index, char in enumerate(self._get_string(dict[event.widget])):
                    alph = self.alphabet.get()
                    index: int = (alph.find(char) - int(self.step.get())*i2) % len(alph)
                    i2+=1
                    encode += alph[index]
            self._set_text(encode, event.widget)

if __name__ == "__main__":
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app = Main(root)
    app.pack()

    root.title("Шифр Тритемия")
    root.geometry(str(screen_width) + "x" + str(screen_height))
    root.minsize(screen_width//2, screen_height//2)

    root.mainloop()
