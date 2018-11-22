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

import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta
import time
import random

from myfiber import __version__
from . import configmanager, exceptions

_USER_AGENT = "QGISClientv{}".format(__version__)
_RETRIABLE_STATUSES = [503]


class Client(object):
    """Performs requests to the ORS API services."""

    def __init__(self,
                 retry_timeout=60):
        """
        :param iface: A QGIS interface instance.
        :type iface: QgisInterface

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int
        """

        base_params = configmanager.read()

        self.key = base_params['api_key']
        self.base_url = base_params['base_url']

        self.session = requests.Session()

        self.retry_timeout = timedelta(seconds=retry_timeout)
        self.requests_kwargs = dict()
        self.requests_kwargs.update({
            "headers": {"User-Agent": _USER_AGENT,
                        'Accept': 'application/geo+json',
                        'X-API-KEY': self.key}
        })

    def request(self,
                url,
                params=None,
                first_request_time=None,
                retry_counter=0):
        """Performs HTTP GET/POST with credentials, returning the body asdlg
        JSON.

        :param url: URL extension for request. Should begin with a slash.
        :type url: string

        :param params: HTTP GET parameters.
        :type params: dict or list of key/value tuples

        :param first_request_time: The time of the first request (None if no
            retries have occurred).
        :type first_request_time: datetime.datetime

        :param retry_counter: The number of this retry, or zero for first attempt.
        :type retry_counter: int

        :raises ApiError: when the API returns an error.
        :raises Timeout: if the request timed out.

        :rtype: dict from JSON response.
        """

        if not first_request_time:
            first_request_time = datetime.now()

        elapsed = datetime.now() - first_request_time
        if elapsed > self.retry_timeout:
            raise exceptions.Timeout()

        if retry_counter > 0:
            # 0.5 * (1.5 ^ i) is an increased sleep time of 1.5x per iteration,
            # starting at 0.5s when retry_counter=1. The first retry will occur
            # at 1, so subtract that first.
            delay_seconds = 1.5 ** (retry_counter - 1)

            # Jitter this value by 50% and pause.
            time.sleep(delay_seconds * (random.random() + 0.5))

        authed_url = self._generate_auth_url(url,
                                             params,
                                             )

        final_requests_kwargs = dict(self.requests_kwargs)

        requests_method = self.session.get

        print("url:\n{}\nParameters:\n{}".format(self.base_url + authed_url,
                                                 final_requests_kwargs))

        try:
            response = requests_method(self.base_url + authed_url,
                                       **final_requests_kwargs)
        except requests.exceptions.Timeout:
            raise exceptions.Timeout()
        except Exception:
            raise

        if response.status_code in _RETRIABLE_STATUSES:
            # Retry request.
            print('Server down.\nRetrying for the {}th time.'.format(retry_counter + 1))

            return self.request(url, params, first_request_time,
                                retry_counter + 1)

        try:
            result = self._get_body(response)
            return result
        except exceptions.RetriableRequest as e:
            return self.request(url, params, first_request_time,
                                retry_counter + 1)
        except Exception:
            raise

    @staticmethod
    def _get_body(response):
        """
        Casts JSON response to dict

        :param response: The HTTP response of the request.
        :type response: JSON object

        :rtype: dict from JSON
        """
        body = response.json()
        status_code = response.status_code

        if status_code != 200:
            raise exceptions.ApiError(status_code,
                                      body['msg'])

        return body

    def _generate_auth_url(self, path, params):
        """Returns the path and query string portion of the request URL, first
        adding any necessary parameters.

        :param path: The path portion of the URL.
        :type path: string

        :param params: URL parameters.
        :type params: dict or list of key/value tuples

        :rtype: string

        """

        if type(params) is dict and params:
            params = sorted(dict(**params).items())

            return path + "?" + _urlencode_params(params)
        else:
            return path


def _urlencode_params(params):
    """URL encodes the parameters.

    :param params: The parameters
    :type params: list of key/value tuples.

    :rtype: string
    """
    # urlencode does not handle unicode strings in Python 2.
    # Firstly, normalize the values so they get encoded correctly.
    params = [(key, _normalize_for_urlencode(val)) for key, val in params]
    # Secondly, unquote unreserved chars which are incorrectly quoted
    # by urllib.urlencode, causing invalid auth signatures. See GH #72
    # for more info.
    return requests.utils.unquote_unreserved(urlencode(params))


try:
    unicode


    # NOTE(cbro): `unicode` was removed in Python 3. In Python 3, NameError is
    # raised here, and caught below.

    def _normalize_for_urlencode(value):
        """(Python 2) Converts the value to a `str` (raw bytes)."""
        if isinstance(value, unicode):
            return value.encode('utf8')

        if isinstance(value, str):
            return value

        return _normalize_for_urlencode(str(value))

except NameError:
    def _normalize_for_urlencode(value):
        """(Python 3) No-op."""
        # urlencode in Python 3 handles all the types we are passing it.
        return value
