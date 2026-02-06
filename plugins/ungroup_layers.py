#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject, GLib
import sys

class MultiUngroup(Gimp.PlugIn):
    def do_query_procedures(self):
        # プロシージャ名を登録
        return ["python-multiungroup-layers"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Ungroup Selected Layers")
        procedure.add_menu_path('<Image>/Layer/')
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        selected = image.get_selected_layers()
        if not selected:
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        image.undo_group_start()
        
        try:
            for item in selected:
                # 選択されたものが「レイヤーグループ（フォルダ）」か判定
                # Gimp 3.0では isinstance を使うのが確実です
                if isinstance(item, Gimp.GroupLayer):
                    parent = item.get_parent()
                    position = image.get_item_position(item)
                    children = item.get_children()
                    
                    if children:
                        # 重なり順を維持するため、逆順（下のレイヤーから順）で移動
                        for child in reversed(children):
                            image.reorder_item(child, parent, position)
                    
                    # 空になったグループを削除
                    image.remove_layer(item)

        except Exception as e:
            Gimp.message(f"Ungroup Error: {str(e)}")
        finally:
            image.undo_group_end()
            Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == '__main__':
    Gimp.main(MultiUngroup.__gtype__, sys.argv)