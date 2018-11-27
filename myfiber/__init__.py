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

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OSMtools class from file.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .myfiberPlugin import myfiber
    return myfiber(iface)


__version__ = '0.4'
__author__ = 'Nils Nolde'
__date__ = '2018-11-27'
__copyright__ = '(C) 2018 by corRelate GmbH'

# Define plugin wide constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'static', 'img')
CONFIG = os.path.join(BASE_DIR, 'config.yml')
