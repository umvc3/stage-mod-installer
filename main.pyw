import tkinter as tk
from tkinter import filedialog
from threading import Thread
from Installer import Installer
from b64_icon import icon

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('UMvC3 Stage Installer')
        self.resizable(False, False)
        self.widgets = {}
        self.add_UMvC3_dir()
        self.add_progress_box()
        self.add_install_button()

        img = tk.PhotoImage(data=icon)
        self.tk.call('wm', 'iconphoto', self._w, img)

    def add_UMvC3_dir(self):
        self.widgets['umvc3_dir_label'] = tk.Label(self, text='Select your UMvC3 folder')
        self.widgets['umvc3_dir_label'].grid(column=0, row=0)

        self.widgets['umvc3_dir_textbox'] = tk.Text(self, height=1, width=35, wrap='none')
        self.widgets['umvc3_dir_textbox'].grid(column=0, row=1)

        self.widgets['umvc3_dir_button'] = tk.Button(self, text='Open', command=lambda:self._setUMvC3Dir(self.widgets['umvc3_dir_textbox']))
        self.widgets['umvc3_dir_button'].grid(column=1, row=1)

    def add_progress_box(self):
        self.progress_box = tk.Text(width=35, height=10, bg='#e3e3e3', wrap='none')
        self.progress_box.bind("<Key>", lambda a: "break")
        self.progress_box.grid(column=0, row=2, stick='nesw', columnspan=2, pady=5)
        self.reset_progress_box_text()

    def reset_progress_box_text(self):
        self.progress_box.delete(1.0, tk.END)
        self.progress_box.insert(tk.END, 'Install Progress:\n')
     
    def add_install_button(self):
        self.widgets['install_button'] = tk.Button(self, text="Install Stage", command=self._install, bg="#6fed53")
        self.widgets['install_button'].grid(column=0, row=3, sticky='nesw', columnspan=2, pady=5)

    def disable_widgets(self):
        for widget in self.widgets:
            self.widgets[widget]['state'] = 'disabled'

    def enable_widgets(self):
        for widget in self.widgets:
            self.widgets[widget]['state'] = 'normal'

    def _setUMvC3Dir(self, textbox):
        default_umvc3_dir = r'C:\Program Files (x86)\Steam\steamapps\common\ULTIMATE MARVEL VS. CAPCOM 3'
        umvc3_path = filedialog.askdirectory(initialdir=default_umvc3_dir, title='Select ULTIMATE MARVEL VS. CAPCOM 3 Folder')
        if umvc3_path:
            textbox.delete(1.0,tk.END)
            textbox.insert(1.0, umvc3_path)
            textbox.see(tk.END)

    def write(self, *msg):
        text = ''
        for item in msg:
            text += '{}'.format(item)
            text += ' '
        text += '\n'
        self.progress_box.insert(tk.END, text)
        self.progress_box.see(tk.END)

    def _install(self):
        self.disable_widgets()

        def t(self):
            self.reset_progress_box_text()
            umvc3dir = self.widgets['umvc3_dir_textbox'].get("1.0",tk.END)
            if len(umvc3dir) > 1:
                installer = Installer(umvc3dir)
                installer.run(printfn=self.write)
            self.enable_widgets()
            return

        thread = Thread(target=t, args=(self,))
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    root = GUI()
    root.mainloop()