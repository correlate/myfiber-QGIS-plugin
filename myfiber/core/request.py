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
                       QgsCoordinateReferenceSystem,
                       QgsMessageLog
                       )

from .client import Client
import urllib.parse as urlparse


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

        # separate parameters from url
        url_parts = list(urlparse.urlparse(url))
        # store parameters
        self.params = dict(urlparse.parse_qsl(url_parts[4]))
        # store url w/o parameters
        url_parts[4] = None
        self.url = urlparse.urlunparse(url_parts)

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
        self.params.update(params)

        # QgsMessageLog.logMessage('url: {}'.format(self.url), 'myfiber')
        # QgsMessageLog.logMessage('query: {}'.format(self.params), 'myfiber')
        response = clnt.request(self.url, self.params)

        return response

    def _adjust_extent(self, bbox):
        """
        Adjust extent (bounding box) if bounding box is too big or unset.

        Bugfix if myfiber is called on QGIS startup.
        Note: On QGIS startup the extent looks like: -1.5e-05,-9e-06,1.5e-05,9e-06

        Since we're only interested in Austria, we use the extent of EPSG 31287 (https://epsg.io/31287),
        which is 9.53,46.4,17.17,49.02.

        :returns: Comma separated list in format minx,miny,maxx,maxy
        """
        extent = (9.53,46.4,17.17,49.02)
        # not the best check, but ok for the moment !
        if abs(bbox[0]) == abs(bbox[2]) or abs(bbox[1]) == abs(bbox[3]):
            return extent

        bbox[0] = extent[0] if bbox[0] < extent[0] or bbox[0] > extent[2] else bbox[0]
        bbox[1] = extent[1] if bbox[1] < extent[1] or bbox[1] > extent[3] else bbox[1]
        bbox[2] = extent[2] if bbox[2] > extent[2] or bbox[2] < extent[0] else bbox[2]
        bbox[3] = extent[3] if bbox[3] > extent[3] or bbox[3] < extent[1] else bbox[3]
        return bbox

    def _stringify_extent(self):
        """
        Transforms the raw map extent string to the bbox URL parameter.

        :returns: Comma separated list in format of minx,miny,maxx,maxy
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

        # Limit box to given extent
        coords_list = self._adjust_extent(bbox=coords_list)

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