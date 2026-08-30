import os as _kiri_os
__file__ = _kiri_os.path.join(_kiri_os.path.dirname(_kiri_os.path.dirname(__file__)), '__init__.py')
del _kiri_os

from .important import *

__package__ = __package__.rsplit('.', 1)[0]


def sna_about_kiri_links_docs_3dgs_D02EC(layout_function, ):
    box_12166 = layout_function.box()
    col_CB7BF = box_12166.column(heading='', align=True)
    box_D36BE = col_CB7BF.box()
    box_D36BE.alignment = 'Center'.upper()
    box_D36BE.label(text='About KIRI Engine', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'pointer-right-fill.svg')))
    box_D36BE.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Addon speel 2.png')), scale=10.0)
    op = box_D36BE.operator('sna.dgs_render_launch_site_bf973', text='Learn More', icon_value=0, emboss=True, depress=False)
    op.sna_site_address = 'https://www.kiriengine.app/'
    box_28D7F = col_CB7BF.box()
    box_28D7F.scale_y = 1.2000000476837158
    split_06A78 = box_28D7F.split(factor=0.5, align=False)
    split_06A78.label(text='Documentation', icon_value=0)
    row_273F5 = split_06A78.row(heading='', align=False)
    row_273F5.alignment = 'Right'.upper()
    op = row_273F5.operator('sna.dgs_render_launch_site_bf973', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'documentation.svg')), emboss=True, depress=False)
    op.sna_site_address = 'https://www.kiriengine.app/blender-addon/3dgs-render'
    op = row_273F5.operator('sna.dgs_render_launch_site_bf973', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'video.svg')), emboss=True, depress=False)
    op.sna_site_address = 'https://www.youtube.com/@BlenderAddon-fromKIRI'
    box_DE3AB = col_CB7BF.box()
    row_7D004 = box_DE3AB.row(heading='', align=False)
    row_7D004.scale_y = 1.2000000476837158
    row_7D004.label(text='Get More Addons', icon_value=0)
    split_649B4 = row_7D004.split(factor=0.5, align=False)
    op = split_649B4.operator('sna.dgs_render_launch_site_bf973', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'SuperHive Logo White.png')), emboss=True, depress=False)
    op.sna_site_address = 'https://blendermarket.com/creators/blender-addon-from-kiri-engine'
    op = split_649B4.operator('sna.dgs_render_launch_site_bf973', text='', icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'kiriengine blender addon icon color.svg')), emboss=True, depress=False)
    op.sna_site_address = 'https://www.kiriengine.app/blender-addon'
