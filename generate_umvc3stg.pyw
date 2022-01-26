import tkinter as tk
from tkinter import filedialog
from threading import Thread
from b64_icon import icon
from umvc3stg import UMvC3Stg
from arc import Arc
import arc_file_paths
import os

def generate_UMvC3Stg(arc, outdir='.'):
    """generates .umvc3stg file with 
    
    :param arc: path to stage arc file
    :type arc: str
    """
    arc = arc.replace('/', '\\').strip()
    stage_id = os.path.basename(arc.split('\\0000.arc')[0])
    outfile = os.path.join(outdir, stage_id+'.umvc3stg')

    new_arc_path = lambda p: os.path.abspath(os.path.join(arc, p))
    sound_arc = Arc(new_arc_path('..\\..\\..\\sound\\chs.arc'))
    arcade_arc = Arc(new_arc_path('..\\..\\..\\ui\\res\\arc\\stg\\'+stage_id.zfill(4)+'.arc'))
    chs_arc = Arc(new_arc_path('..\\..\\..\\ui\\mnchsstg.arc'))

    announcer_path = arc_file_paths.get_announcer(stage_id)
    stg_text_path = arc_file_paths.get_stage_text(stage_id)
    stg_preview_path = arc_file_paths.get_stage_preview(stage_id)
    sm_stg_preview_path = arc_file_paths.get_small_stage_preview(stage_id)
    arcade_path = arc_file_paths.get_stage_arcade_text(stage_id)

    def open_and_write(umvc3stg, arc, filename):
        binary = b''
        for i in range(len(arc.path_list)):
            if arc.path_list[i] == filename:
                binary = arc.binaries[i]
                break
        umvc3stg.write(binary)
        umvc3stg.close()

    umvc3stg = UMvC3Stg(outfile, 'w')
    # put 0000.arc in archive
    with umvc3stg.open(umvc3stg.ARC, 'w') as umvc3stg_arc, open(arc, 'rb') as stg_arc:
        umvc3stg_arc.write(stg_arc.read())
    # put announcer.xsew in archive
    open_and_write(umvc3stg.open(umvc3stg.ANNOUNCER, 'w'), sound_arc, announcer_path)
    # put stage_select_text.tex in archive
    open_and_write(umvc3stg.open(umvc3stg.STG_TEXT, 'w'), chs_arc, stg_text_path)
    # put stage_preview.tex in archive
    open_and_write(umvc3stg.open(umvc3stg.STG_PREVIEW, 'w'), chs_arc, stg_preview_path)
    # put small_stage_preview.tex in archive
    open_and_write(umvc3stg.open(umvc3stg.STG_PREVIEW_SM, 'w'), chs_arc, sm_stg_preview_path)
    # put arcade_text.tex in archive
    open_and_write(umvc3stg.open(umvc3stg.STG_TEXT_ARCADE, 'w'), arcade_arc, arcade_path)

    umvc3stg.close()

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Generate UMvC3 Stage Installer File')
        self.resizable(False, False)
        self.widgets = {}
        self.add_UMvC3_dir()
        self.add_install_button()

        img = tk.PhotoImage(data=icon)
        self.tk.call('wm', 'iconphoto', self._w, img)

    def add_UMvC3_dir(self):
        self.widgets['stage_arc_label'] = tk.Label(self, text='Select stage arc file')
        self.widgets['stage_arc_label'].grid(column=0, row=0)

        self.widgets['stage_arc_textbox'] = tk.Text(self, height=1, width=35, wrap='none')
        self.widgets['stage_arc_textbox'].grid(column=0, row=1)

        self.widgets['stage_arc_button'] = tk.Button(self, text='Open', command=lambda:self._setUMvC3Dir(self.widgets['stage_arc_textbox']))
        self.widgets['stage_arc_button'].grid(column=1, row=1)

    def add_install_button(self):
        self.widgets['install_button'] = tk.Button(self, text="Generate .umvc3stg", command=self._install, bg="#6fed53")
        self.widgets['install_button'].grid(column=0, row=3, sticky='nesw', columnspan=2, pady=5)

    def disable_widgets(self):
        for widget in self.widgets:
            self.widgets[widget]['state'] = 'disabled'

    def enable_widgets(self):
        for widget in self.widgets:
            self.widgets[widget]['state'] = 'normal'

    def _setUMvC3Dir(self, textbox):
        default_umvc3_dir = r'C:\Program Files (x86)\Steam\steamapps\common\ULTIMATE MARVEL VS. CAPCOM 3'
        stage_path = filedialog.askopenfilename(initialdir=default_umvc3_dir, title='Select Your Stage\'s .arc File (nativePCx64\\stg\\<stage_id>\\0000.arc)', filetypes=(('MT Framework Archive', '*.arc'),)).replace('/', '\\')
        if stage_path:
            textbox.delete(1.0,tk.END)
            textbox.insert(1.0, stage_path)
            textbox.see(tk.END)

    def _install(self):
        self.disable_widgets()

        def t(self):
            stage_arc = self.widgets['stage_arc_textbox'].get("1.0",tk.END)
            if len(stage_arc) > 1:
                generate_UMvC3Stg(stage_arc)
                pass
            self.enable_widgets()
            return

        thread = Thread(target=t, args=(self,))
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    root = GUI()
    root.mainloop()