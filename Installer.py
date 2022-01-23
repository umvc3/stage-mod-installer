from arc import Arc
from datetime import datetime
from glob import glob
from shutil import copy
from umvc3stg import InvalidUMvC3Stg, UMvC3Stg
import os
import arc_file_paths

class Installer(object):
    def __init__(self, umvc3_dir):
        self.umvc3_dir = umvc3_dir.strip()

        self._nativePCx64_stg = 'nativePCx64\\stg'
        self._nativePCx64_arcade = 'nativePCx64\\ui\\res\\arc\\stg'
        self._nativePCx64_sound = 'nativePCx64\\sound'
        self._nativePCx64_ui = 'nativePCx64\\ui'

        self.stage_path = os.path.join(self.umvc3_dir, self._nativePCx64_stg)
        self.arcade_path = os.path.join(self.umvc3_dir, self._nativePCx64_arcade)
        self.sound_path = os.path.join(self.umvc3_dir, os.path.join(self._nativePCx64_sound, 'chs.arc'))

        self.mnchsstg_paths = [os.path.abspath(p) for p in glob(os.path.join(self.umvc3_dir, self._nativePCx64_ui, 'mnchsstg*arc'))]

    def _copy(self, src, dst):
        try:
            copy(src, dst)
        except:
            pass

    def generate_backups(self, stage_id, umvc3stg, printfn=print):
        backups_dir = os.path.abspath('./backups')
        if not os.path.exists(backups_dir):
            os.makedirs(backups_dir)

        backup_dir = 'backup'+str(len(os.listdir('.\\backups'))).zfill(3) + datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        backup_dir = os.path.join(backups_dir, backup_dir)
        os.makedirs(backup_dir)

        stage_dir = os.path.join(self.stage_path, stage_id.zfill(3))
        stg_backup_dir = os.path.join(backup_dir, self._nativePCx64_stg, stage_id.zfill(3))
        stg_arc = os.path.join(stage_dir, '0000.arc')
        os.makedirs(stg_backup_dir)
        self._copy(stg_arc, stg_backup_dir)
        printfn('Generated a backup of', stg_arc.replace('/', '\\'))

        if umvc3stg.announcer:
            sound_backup_dir = os.path.join(backup_dir, self._nativePCx64_sound)
            os.makedirs(sound_backup_dir)
            self._copy(self.sound_path, sound_backup_dir)
            printfn('Generated a backup of', self.sound_path.replace('/', '\\'))
        if umvc3stg.stage_select_text or umvc3stg.stage_preview or umvc3stg.small_stage_preview:
            ui_backup_dir = os.path.join(backup_dir, self._nativePCx64_ui)
            os.makedirs(ui_backup_dir)
            for mnchsstg in self.mnchsstg_paths:
                self._copy(mnchsstg, ui_backup_dir)
                printfn('Generated a backup of', mnchsstg.replace('/', '\\'))
        if umvc3stg.arcade_text or umvc3stg.stage_preview:
            arcade_backup_dir = os.path.join(backup_dir, self._nativePCx64_arcade)
            stg_arcade_arc = os.path.join(self.arcade_path, stage_id.zfill(4)+'.arc')
            os.makedirs(arcade_backup_dir)
            self._copy(stg_arcade_arc, arcade_backup_dir)
            printfn('Generated a backup of', stg_arcade_arc.replace('/', '\\'))

    def run(self, printfn=print):
        stages = glob('./*.umvc3stg')

        for stage in stages:
            stage_id = os.path.basename(stage).split('.')[0].lstrip('0')
            printfn('Installing "'+os.path.abspath(stage).replace('/', '\\')+'" ...')
            try:
                with UMvC3Stg(stage, 'r') as umvc3stg:
                    self.generate_backups(stage_id, umvc3stg, printfn=printfn)

                    # inject the stage preview/text in stage select
                    for mnchsstg in self.mnchsstg_paths:
                        lang = mnchsstg[-7:-4] if mnchsstg[-7] == '_' else ''
                        arc = Arc(mnchsstg)
                        if umvc3stg.stage_preview:
                            arc.replace(arc_file_paths.get_stage_preview(stage_id), umvc3stg.stage_preview)
                            printfn('Injected stage previews for stage', stage_id+lang, '...')
                        if umvc3stg.small_stage_preview:
                            arc.replace(arc_file_paths.get_small_stage_preview(stage_id), umvc3stg.small_stage_preview)
                        if umvc3stg.stage_select_text:
                            arc.replace(arc_file_paths.get_stage_text(stage_id), umvc3stg.stage_select_text)
                            printfn('Injected text for stage', stage_id+lang, '...')
                        arc.save(mnchsstg)

                    arcade_arc_path = stage_id.zfill(4) + '.arc'
                    arcade_arc_path = os.path.join(self.arcade_path, arcade_arc_path)
                    arcade_arc = Arc(arcade_arc_path)
                    if umvc3stg.stage_preview:
                        arcade_arc.replace(arc_file_paths.get_stage_preview(stage_id), umvc3stg.stage_preview)
                    if umvc3stg.arcade_text:
                        arcade_arc.replace(arc_file_paths.get_stage_arcade_text(stage_id), umvc3stg.arcade_text)
                        printfn('Injected text (arcade mode) for stage', stage_id, '...')
                    arcade_arc.save(arcade_arc_path)

                    sound_arc = Arc(self.sound_path)
                    if umvc3stg.announcer:
                        sound_arc.replace(arc_file_paths.get_announcer(stage_id), umvc3stg.announcer)
                        printfn('Injected announcer sfx for stage', stage_id, '...')
                    sound_arc.save(self.sound_path)

                    arc_path = os.path.join(self.umvc3_dir, self._nativePCx64_stg, stage_id.zfill(3), '0000.arc')
                    with open(arc_path, 'wb') as f:
                        f.write(umvc3stg.stage_arc)
                    printfn('Stage', stage_id, 'has finished installing.')

            except InvalidUMvC3Stg:
                printfn('ERROR: '+os.path.abspath(stage)+ ' is an invalid ".umvc3stg" file')
                printfn('='*30)
            except Exception as ex:
                printfn(ex)
