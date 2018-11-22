# -*- coding: utf-8 -*-
"""
/***************************************************************************
 noegig
                                 A QGIS plugin
Downloads GeoJSONs from the APIs at https://api.noegig.at/v1.2/doc#/.
                              -------------------
        begin                : 2018-11-22
        copyright            : (C) 2018 by corRelate GmbH
        email                : hello@correlate.at
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path

from PyQt5.QtWidgets import (QAction,
                             QDialog,
                             )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from myfiber import ICON_DIR
from myfiber.gui import myfiberDialogUI
from myfiber.core import configmanager

class noegigDialogMain(QDialog):
    """Defines all mandatory QGIS things about dialog."""

    def __init__(self, iface, parent=None):
        """

        :param iface: the current QGIS interface
        :type iface: Qgis.Interface
        """
        QDialog.__init__(self, parent)

        # Set up UI
        self.ui = myfiberDialogUI.Ui_Dialog()
        self.ui.setupUi(self)

        self._iface = iface

        # Programmtically invoke logo
        logo = QPixmap(os.path.join(ICON_DIR, "logo-correlate.svg"))
        pixmap = logo.scaled(200, 50,
                             aspectRatioMode=Qt.KeepAspectRatio,
                             transformMode=Qt.SmoothTransformation
                                   )
        self.ui.header_pic.setPixmap(pixmap)
        self.ui.header_pic.setAlignment(Qt.AlignCenter)


        # Read config file
        self.CONFIG = configmanager.read()

        # Set API key field
        self.ui.key_text.setText(self.CONFIG['api_key'])

        #### Set up signals/slots ####

        # API key text line
        self.ui.key_text.textChanged.connect(self._keywriter)

    def initGui(self):
        """Gets called when QGIS UI starts up"""
        self.action = QAction(QIcon(os.path.join(ICON_DIR, 'icon_plugin.svg')),
                              'noegig',  # tr text
                              self._iface.mainWindow()  # parent
                              )

        self._iface.addPluginToMenu('&noegig',
                                    self.action)
        self._iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)

    def unload(self):
        """Gets called when QGIS is closing"""
        self._iface.removePluginMenu('&noegig', self.action)
        self._iface.removeToolBarIcon(self.action)

    def run(self):
        """When you click the plugin icon"""
        self.show()
        result = self.exec_()
        if result:
            self.close()

    def _keywriter(self):
        """
        Writes key to text file when api key text field changes.
        """
        configmanager.write('api_key',
                            self.ui.key_text.text())
