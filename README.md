# VXFWindow
Qt Window class for designing tools to be compatible between multiple VFX programs.

The main purpose of the class is to integrate into the program UI, but it also contains helpful features such as safely dealing with callbacks and automatically saving the window position.

The intended usage is to make your window class inherit `VFXWindow` - which is an instance of `QMainWindow`. By calling `cls.show()`, it will launch the correct window type based on what program is loaded, and what settings were previously saved.

This is perfectly stable, but there is still plenty that needs improvement. Eventually I plan to add support for Unreal, Fusion, Blender, etc.

### Basic Example:
```python
class MyWindow(VFXWindow):
    WindowID = 'unique_window_id'
    WindowName = 'My Window'

    def __init__(self, parent=None, **kwargs):
        super(MyWindow, self).__init__(parent, **kwargs)
        # Setup window here

        # Setup callbacks, but wait until the program is ready
        self.deferred(self.newScene)

    def newScene(self, *args):
        """Example: Delete and reapply callbacks after loading a new scene."""
        self.removeCallbacks('sceneNewCallbacks')
        if self.maya:
            self.addCallbackScene('kAfterNew', self.newScene, group='sceneNewCallbacks')
        elif self.nuke:
            self.addCallbackOnCreate(self.newScene, nodeClass='Root', group='sceneNewCallbacks')

if __name__ == '__main__':
    MyWindow.show()
```

### Compatibility
 - Maya (2011-2016, tested lightly on 2016) - standard, docked (`pymel.core.dockControl`)
 - Maya (2017+, tested on 2017-2019) - standard, docked (`pymel.core.workspaceControl`), dialog (`pymel.core.layoutDialog`)
 - Nuke (tested on 9 and 10) - standard, docked (`nukescripts.panels`)
 - Houdini (tested on 16) - standard
 - Standalone (Qt4, Qt5) - standard

### Generic Features
 - Automatically save/restore window position
 - Move window to screen if out of bounds (windows only)
 - Keep track of callbacks to remove groups if required, and clean up on window close
 - Keep track of signals to remove groups if required
 - Display a popup message that forces control
 - Set palette to that of another program
 - Auto close if opening a duplicate window
 - Close down all windows at once

### Maya Features
 - Dock window using workspaceControl
 - Dialog window using layoutDialog
 - Save/restore position of workspaceControl window (floating+docked)
 - Easy access to callbacks

### Nuke Features
 - Dock window as a panel
 - Save/restore location of panel (docked only)

### Special Thanks
 - [Blue Zoo](https://www.blue-zoo.co.uk/) - I've been building this up while working there
 - [Lior Ben Horin](https://gist.github.com/liorbenhorin): [Simple_MayaDockingClass.py](https://gist.github.com/liorbenhorin/69da10ec6f22c6d7b92deefdb4a4f475) - used for main Maya docking code
 - [Fredrik Averpil](https://github.com/fredrikaverpil): [pyvfx-boilerplate](https://github.com/fredrikaverpil/pyvfx-boilerplate) - helped with palettes, Nuke, and pre-2017 Maya
