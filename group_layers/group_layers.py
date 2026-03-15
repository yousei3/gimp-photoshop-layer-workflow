#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject, GLib
import sys
import time

class MultiGroup(Gimp.PlugIn):
    def do_query_procedures(self):
        # マージ用とは別のIDを設定
        return ["python-multigroup-layers"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Group Selected Layers")
        procedure.add_menu_path('<Image>/Layer/')
        procedure.add_menu_path('<Layers>/Layers Menu') # LayerMenu
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # 1. 選択レイヤーを取得
        selected = image.get_selected_layers()
        if not selected or len(selected) < 1:
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

        # 2. 上から順にソート
        selected.sort(key=lambda l: image.get_item_position(l))
        
        # 3. 挿入位置の基準を確保
        top_layer = selected[0]
        parent = top_layer.get_parent()
        position = image.get_item_position(top_layer)

        # 確実にUndoグループを開始
        image.undo_group_start()
        
        try:
            # 4. GIMP 3.0で動作確認済みのグループ作成方法
            group = Gimp.GroupLayer.new(image)
            group.set_name(f"Group_{int(time.time())}")
            
            # 5. 画像に挿入
            image.insert_layer(group, parent, position)
            
            # 6. 選択レイヤーをグループ内へ移動
            # 逆順で処理することでグループ内での上下関係を維持
            for layer in reversed(selected):
                if layer.is_valid() and layer != group:
                    image.reorder_item(layer, group, 0)
            
            # 7. 作成したグループを選択状態にする
            image.set_selected_layers([group])

        except Exception as e:
            Gimp.message(f"Grouping Error: {str(e)}")
        finally:
            # 警告を避けるため確実にUndoグループを閉じる
            image.undo_group_end()
            Gimp.displays_flush()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == '__main__':
    Gimp.main(MultiGroup.__gtype__, sys.argv)