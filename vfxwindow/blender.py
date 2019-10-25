"""Window class for Blender."""

from __future__ import absolute_import

import sys

import bpy

from .utils import setCoordinatesToScreen
from .utils.Qt import QtWidgets
from .standalone import StandaloneWindow


BLENDER_VERSION = bpy.app.version_string


def getMainWindow():
    """Get an instance of the main window.
    TODO: Get HWND using pywin32.
    """
    return None


class BlenderWindow(StandaloneWindow):
    """Window to use for Blender.
    It has support for automatically saving the position when closed,
    and performs some necessary CSS edits to fix colours.
    """
    def __init__(self, parent=None, **kwargs):
        if parent is None:
            parent = getMainWindow()
        super(BlenderWindow, self).__init__(parent, **kwargs)
        self.blender = True
        self.standalone = False

    def saveWindowPosition(self):
        """Save the window location."""
        try:
            blenderSettings = self.windowSettings['blender']
        except KeyError:
            blenderSettings = self.windowSettings['blender'] = {}
        try:
            mainWindowSettings = blenderSettings['main']
        except KeyError:
            mainWindowSettings = blenderSettings['main'] = {}

        mainWindowSettings['width'] = self.width()
        mainWindowSettings['height'] = self.height()
        mainWindowSettings['x'] = self.x()
        mainWindowSettings['y'] = self.y()
        super(BlenderWindow, self).saveWindowPosition()

    def loadWindowPosition(self):
        """Set the position of the window when loaded."""
        try:
            x = self.windowSettings['blender']['main']['x']
            y = self.windowSettings['blender']['main']['y']
            width = self.windowSettings['blender']['main']['width']
            height = self.windowSettings['blender']['main']['height']
        except KeyError:
            super(BlenderWindow, self).loadWindowPosition()
        else:
            x, y = setCoordinatesToScreen(x, y, width, height, padding=5)
            self.resize(width, height)
            self.move(x, y)

    @classmethod
    def show(cls, **kwargs):
        return super(BlenderWindow, cls).show(instance=True, exec_=False)
