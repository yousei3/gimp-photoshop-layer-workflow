#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject, GLib
import sys
import time

class MultiMerge(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["python-multimerge-layers"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Merge Selected Layers")
        procedure.add_menu_path('<Image>/Layer/')
        procedure.add_menu_path('<Layers>/Layers Menu') # LayerMenu
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        selected = image.get_selected_layers()
        if not selected or len(selected) < 2:
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        selected.sort(key=lambda l: image.get_item_position(l))
        
        top_layer = selected[0]
        parent = top_layer.get_parent()
        position = image.get_item_position(top_layer)

        image.undo_group_start()
        
        try:
            # 1. 成功実績のあるグループ作成
            unique_name = f"MGD_GRP_{int(time.time())}"
            group = Gimp.GroupLayer.new(image)
            group.set_name(unique_name)
            image.insert_layer(group, parent, position)
            
            # 2. 成功実績のあるレイヤー移動
            for layer in reversed(selected):
                if layer.is_valid() and layer != group:
                    image.reorder_item(layer, group, 0)
            
            # 3. 【特定したプロシージャを実行】
            # 直接 pdb.run_procedure を呼ばず、一度プロシージャオブジェクトを取り出す
            pdb = Gimp.get_pdb()
            merge_proc = pdb.lookup_procedure('gimp-group-layer-merge')
            
            if merge_proc:
                # 設定オブジェクト（config）を作成して引数をセット
                merge_config = merge_proc.create_config()
                # 引数名は 'group-layer' であることを Procedure Browser で確認済み
                merge_config.set_property('group-layer', group)
                
                # run ではなく、config を使って実行
                res = merge_proc.run(merge_config)
                
                if res.index(0) == Gimp.PDBStatusType.SUCCESS:
                    merged_layer = res.index(1)
                    image.set_selected_layers([merged_layer])
            else:
                Gimp.message("Error: gimp-group-layer-merge not found.")

        except Exception as e:
            Gimp.message(f"Final Merge Error: {str(e)}")
        finally:
            image.undo_group_end()
            Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == '__main__':
    Gimp.main(MultiMerge.__gtype__, sys.argv)