# from .important import *
# import bpy
#
# class SNA_GROUP_sna_dgs_material_properties_group(bpy.types.PropertyGroup):
#     lq_hq: bpy.props.EnumProperty(name='LQ_HQ', description='', items=[('LQ Mode (Dithered Alpha)', 'LQ Mode (Dithered Alpha)', '', 0, 0), ('HQ Mode (Blended Alpha)', 'HQ Mode (Blended Alpha)', '', 0, 1)], update=sna_update_lq_hq_065F9)
#
#
# def sna_update_lq_hq_065F9(self, context):
#     sna_updated_prop = self.lq_hq
#     self.surface_render_method = ('BLENDED' if (sna_updated_prop == 'HQ Mode (Blended Alpha)') else 'DITHERED')
#     for i_DF01B in range(len(bpy.data.objects)):
#         if (property_exists("bpy.data.objects[i_DF01B].modifiers", globals(), locals()) and 'KIRI_3DGS_Sorter_GN' in bpy.data.objects[i_DF01B].modifiers):
#             for i_19853 in range(len(bpy.data.objects[i_DF01B].material_slots)):
#                 if (bpy.data.objects[i_DF01B].material_slots[i_19853].material == self):
#                     bpy.data.objects[i_DF01B].modifiers['KIRI_3DGS_Sorter_GN'].show_viewport = (sna_updated_prop == 'HQ Mode (Blended Alpha)')
#                     bpy.data.objects[i_DF01B].modifiers['KIRI_3DGS_Sorter_GN'].show_render = (sna_updated_prop == 'HQ Mode (Blended Alpha)')
#                     if (property_exists("bpy.context.scene.objects", globals(), locals()) and 'KIRI_HQ_Merged_Object' in bpy.context.scene.objects):
#                         if (sna_updated_prop == 'HQ Mode (Blended Alpha)'):
#                             bpy.data.objects[i_DF01B].hide_viewport = True
#                             bpy.data.objects[i_DF01B].hide_render = True
#                             bpy.data.objects['KIRI_HQ_Merged_Object'].hide_viewport = False
#                             bpy.data.objects['KIRI_HQ_Merged_Object'].hide_render = False
#                         else:
#                             bpy.data.objects['KIRI_HQ_Merged_Object'].hide_viewport = True
#                             bpy.data.objects['KIRI_HQ_Merged_Object'].hide_render = True
#                             bpy.data.objects[i_DF01B].hide_viewport = False
#                             bpy.data.objects[i_DF01B].hide_render = False
#
