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

from qgis.core import (QgsPoint,
                       QgsProject,
                       QgsCoordinateTransform,
                       QgsCoordinateReferenceSystem
                       )

from .client import Client


class RequestBuilder():
    def __init__(self, url, map_extent, map_epsg):
        """
        Builds the request from map parameters and user input

        :param url: The URL of the endpoint.
        :type url: str

        :param map_extent: Raw map extent from mapCanvas().extent().toString()
        :type map_extent: str

        :param map_epsg: CRS ID in format of '<Provider>: <Code>'
        :type map_epsg: str
        """
        self.url = url
        self.map_extent_raw = map_extent
        self.map_epsg = map_epsg

    def build_request(self):
        """
        Builds the actual request.

        :returns response: API response GeoJSON object
        :rtype: dict
        """
        clnt = Client()
        params = dict()

        map_extent_string = self._stringify_extent()
        params['bbox'] = map_extent_string

        response = clnt.request(self.url, params)

        return response

    def _stringify_extent(self):
        """
        Transforms the raw map extent string to the bbox URL parameter.

        :returns: Comma separated list in format of minx,miy,maxx,maxy
        :rtype: list
        """
        # Get QgsPoints in map CRS
        extent_points_string = [point.strip() for point in self.map_extent_raw.split(':')]
        extent_points_string_list = [point.split(',') for point in extent_points_string]
        extent_points = [QgsPoint(*[float(coord) for coord in coords]) for coords in extent_points_string_list]

        crs_wgs = QgsCoordinateReferenceSystem(4326)
        crs_map = QgsCoordinateReferenceSystem(self.map_epsg)
        xform = QgsCoordinateTransform(crs_map, crs_wgs, QgsProject.instance())

        coords_list = []
        # Transforms point in place
        for point in extent_points:
            point.transform(xform)
            coords_list.extend([point.x(), point.y()])

        return ','.join([self._format_float(f) for f in coords_list])

    def _format_float(self, f):
        """
        Formats a float to 6 digits.

        :param f: float to be converted
        :type f: float

        :returns: formatted float
        :rtype: str
        """

        return ("{}".format(round(float(f), 6)).rstrip("0").rstrip("."))