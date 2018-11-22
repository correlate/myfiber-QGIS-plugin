## Installation

### ZIP

Unzip entire `.zip` contents to QGIS pugin dir:

- Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
- Windows: `C:\Users\USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
- Mac OS: `Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`

Restart QGIS and activate plugin in Plugin Manager.

## Modifying GUI

Only modify the GUI over Qt Designer (part of QGIS distro):

1. Open `gui/OSMtoolsDialogUI.ui` in Qt Designer
2. Modify to your needs. Name the widgets accordingly.
3. Save file.
4. Check preview: `pyuic5 gui/myfiberDialogUI.ui -p`
4. Populate the `.py` file: `pyuic5 gui/myfiberDialogUI.ui > gui/myfiberDialogUI.py`

## Compile plugin

Only needs to be done, when `resources.qrc` changes, to e.g. include more images.

`pyrcc5 -o resources_rc.py resources.qrc`
