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
import yaml

from myfiber import BASE_DIR, CONFIG


def read():
    with open(os.path.join(BASE_DIR, CONFIG)) as f:
        doc = yaml.safe_load(f)

    return doc


def write(key, value):

    doc = read()
    doc[key] = value
    with open(os.path.join(BASE_DIR, CONFIG), 'w') as f:
        yaml.safe_dump(doc, f)