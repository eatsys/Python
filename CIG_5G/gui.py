#!/user/bin/env python
# encoding: utf-8
# @time      : 2020/2/11 14:05

__author__ = 'Ethan'

import PySimpleGUI as gui

layout = [[gui.Text('hello')],
          [gui.Input()],
          [gui.OK()]]

event, (number,) = gui.Window('hello').Layout(layout).Read()

gui.Popup(event, number)
