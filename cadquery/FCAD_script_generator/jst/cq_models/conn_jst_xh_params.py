# -*- coding: utf8 -*-
#!/usr/bin/python
#
# CadQuery script returning JST XH Connectors

## requirements
## freecad (v1.5 and v1.6 have been tested)
## cadquery FreeCAD plugin (v0.3.0 and v0.2.0 have been tested)
##   https://github.com/jmwright/cadquery-freecad-module

## This script can be run from within the cadquery module of freecad.
## To generate VRML/ STEP files for, use export_conn_jst_xh
## script of the parrent directory.

#* This is a cadquery script for the generation of MCAD Models.             *
#*                                                                          *
#*   Copyright (c) 2016                                                     *
#* Rene Poeschl https://github.com/poeschlr                                 *
#* All trademarks within this guide belong to their legitimate owners.      *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU General Public License (GPL)             *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc.,                                                      *
#*   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA           *
#*                                                                          *
#* The models generated with this script add the following exception:       *
#*   As a special exception, if you create a design which uses this symbol, *
#*   and embed this symbol or unaltered portions of this symbol into the    *
#*   design, this symbol does not by itself cause the resulting design to   *
#*   be covered by the GNU General Public License. This exception does not  *
#*   however invalidate any other reasons why the design itself might be    *
#*   covered by the GNU General Public License. If you modify this symbol,  *
#*   you may extend this exception to your version of the symbol, but you   *
#*   are not obligated to do so. If you do not wish to do so, delete this   *
#*   exception statement from your version.                                 *
#****************************************************************************

__title__ = "model description for JST-XH Connectors"
__author__ = "poeschlr"
__Comment__ = 'model description for JST-XH Connectors using cadquery'

___ver___ = "1.1 10/04/2016"

from collections import namedtuple
from math import sqrt


#global parameter
pin_width = 0.64
pin_depth = 3.4
pin_inner_lenght = 6.5
pin_lock_h1 = 1.9
pin_lock_h2 = 2.5
pin_lock_d = 0.3
pin_fillet = 0.2
pin_bend_radius = 0.05
pin_pitch = 2.5
body_corner_x = -2.45
body_corner_y = -2.35


def v_add(p1, p2):
    return (p1[0]+p2[0],p1[1]+p2[1])

def v_sub(p1, p2):
    return (p1[0]-p2[0],p1[1]-p2[1])
#v_add(pcs2, (-body_cutout_radius*(1-1/sqrt(2)), -1/sqrt(2)*body_cutout_radius))
def get_third_arc_point(starting_point, end_point):
    px = v_sub(end_point, starting_point)
    #FreeCAD.Console.PrintMessage("("+str(px[0])+","+str(px[1])+")")
    return v_add((px[0]*(1-1/sqrt(2)),px[1]*(1/sqrt(2))),starting_point)

def add_p_to_chain(chain, rel_point):
    chain.append(v_add(chain[len(chain)-1], rel_point))

def mirror(chain):
    result = []
    for point in chain:
        result.append((point[0]*-1,point[1]))
    return result

def poline(points, plane):
    sp = points.pop()
    plane=plane.moveTo(sp[0],sp[1])
    plane=plane.polyline(points)
    return plane

Params = namedtuple("Params",[
    'file_name',
    'angled',
    'num_pins',
    'model_name',
    'pin_angle_distance',
    'pin_angle_length',
    'body_width',
    'body_height',
    'body_length',
    'zdistance'
])

def make_params_angled(num_pins, name):
    return Params(
        angled=True,
        num_pins=num_pins,
        model_name=name,
        pin_angle_distance=9.2-7,
        pin_angle_length=9.2,
        body_width=5.75,
        body_height=7.0,
        body_length=2*2.45+(num_pins-1)*pin_pitch,
        zdistance=6.1-5.75,
        file_name="JST_XH_S{num_pins:02d}B-XH-A_{num_pins:02d}x{pin_pitch:.2f}mm_Angled".format(num_pins=num_pins, pin_pitch=pin_pitch)
    )
def make_params_angled_short(num_pins, name):
    return Params(
        angled=True,
        num_pins=num_pins,
        model_name=name,
        pin_angle_distance=7.6-7,
        pin_angle_length=7.6,
        body_width=5.75,
        body_height=7.0,
        body_length=2*2.45+(num_pins-1)*pin_pitch,
        zdistance=6.1-5.75,
        file_name="JST_XH_S{num_pins:02d}B-XH-A-1_{num_pins:02d}x{pin_pitch:.2f}mm_Angled_compact".format(num_pins=num_pins, pin_pitch=pin_pitch)
    )
def make_params_straight(num_pins, name):
    return Params(
        angled=False,
        num_pins=num_pins,
        model_name=name,
        pin_angle_distance=0,
        pin_angle_length=0,
        body_width=5.75,
        body_height=7.0,
        body_length=2*2.45+(num_pins-1)*pin_pitch,
        zdistance=6.1-5.75,
        file_name="JST_XH_B{num_pins:02d}B-XH-A_{num_pins:02d}x{pin_pitch:.2f}mm_Straight".format(num_pins=num_pins, pin_pitch=pin_pitch)
    )

params_straight = {
    "B02B_XH_A" : make_params_straight( 2, 'B02B_XH_A'),
    "B03B_XH_A" : make_params_straight( 3, 'B03B_XH_A'),
    "B04B_XH_A" : make_params_straight( 4, 'B04B_XH_A'),
    "B05B_XH_A" : make_params_straight( 5, 'B05B_XH_A'),
    "B06B_XH_A" : make_params_straight( 6, 'B06B_XH_A'),
    "B07B_XH_A" : make_params_straight( 7, 'B07B_XH_A'),
    "B08B_XH_A" : make_params_straight( 8, 'B08B_XH_A'),
    "B09B_XH_A" : make_params_straight( 9, 'B09B_XH_A'),
    "B10B_XH_A" : make_params_straight(10, 'B10B_XH_A'),
    "B11B_XH_A" : make_params_straight(11, 'B11B_XH_A'),
    "B12B_XH_A" : make_params_straight(12, 'B12B_XH_A'),
    "B13B_XH_A" : make_params_straight(13, 'B13B_XH_A'),
    "B14B_XH_A" : make_params_straight(14, 'B14B_XH_A'),
    "B15B_XH_A" : make_params_straight(15, 'B15B_XH_A'),
    "B16B_XH_A" : make_params_straight(16, 'B16B_XH_A'),
    "B20B_XH_A" : make_params_straight(20, 'B20B_XH_A')
}

params_angled = {
    "S02B_XH_A" : make_params_angled( 2, 'S02B_XH_A'),
    "S03B_XH_A" : make_params_angled( 3, 'S03B_XH_A'),
    "S04B_XH_A" : make_params_angled( 4, 'S04B_XH_A'),
    "S05B_XH_A" : make_params_angled( 5, 'S05B_XH_A'),
    "S06B_XH_A" : make_params_angled( 6, 'S06B_XH_A'),
    "S07B_XH_A" : make_params_angled( 7, 'S07B_XH_A'),
    "S08B_XH_A" : make_params_angled( 8, 'S08B_XH_A'),
    "S09B_XH_A" : make_params_angled( 9, 'S09B_XH_A'),
    "S10B_XH_A" : make_params_angled(10, 'S10B_XH_A'),
    "S11B_XH_A" : make_params_angled(11, 'S11B_XH_A'),
    "S12B_XH_A" : make_params_angled(12, 'S12B_XH_A'),
    "S13B_XH_A" : make_params_angled(13, 'S13B_XH_A'),
    "S14B_XH_A" : make_params_angled(14, 'S14B_XH_A'),
    "S15B_XH_A" : make_params_angled(15, 'S15B_XH_A'),
    "S16B_XH_A" : make_params_angled(16, 'S16B_XH_A')
}

params_angled_compact = {
    "S03B_XH_A_1" : make_params_angled_short( 3, 'S03B_XH_A_1'),
    "S04B_XH_A_1" : make_params_angled_short( 4, 'S04B_XH_A_1'),
    "S05B_XH_A_1" : make_params_angled_short( 5, 'S05B_XH_A_1'),
    "S06B_XH_A_1" : make_params_angled_short( 6, 'S06B_XH_A_1'),
    "S07B_XH_A_1" : make_params_angled_short( 7, 'S07B_XH_A_1'),
    "S08B_XH_A_1" : make_params_angled_short( 8, 'S08B_XH_A_1'),
    "S09B_XH_A_1" : make_params_angled_short( 9, 'S09B_XH_A_1'),
    "S10B_XH_A_1" : make_params_angled_short(10, 'S10B_XH_A_1'),
    "S11B_XH_A_1" : make_params_angled_short(11, 'S11B_XH_A_1'),
    "S12B_XH_A_1" : make_params_angled_short(12, 'S12B_XH_A_1'),
    "S13B_XH_A_1" : make_params_angled_short(13, 'S13B_XH_A_1'),
    "S14B_XH_A_1" : make_params_angled_short(14, 'S14B_XH_A_1'),
    "S15B_XH_A_1" : make_params_angled_short(15, 'S15B_XH_A_1')
}
