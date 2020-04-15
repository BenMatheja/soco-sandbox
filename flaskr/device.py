import functools
import soco
import urllib

from soco.discovery import by_name
from collections import defaultdict
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_api import status


bp = Blueprint('device', __name__, url_prefix='/devices')


@bp.route('/v1/', methods=['GET'])
def listAvailableDevices():
    d = {}
    if(soco.discover()):
        for zone in soco.discover():
            d[zone.player_name] = {}
            device = by_name(zone.player_name)

            d[zone.player_name]['zone.player_name'] = zone.player_name
            d[zone.player_name]['zone.uid'] = zone.uid
            d[zone.player_name]['zone.volume'] = zone.volume
            d[zone.player_name]['zone.is_coordinator'] = zone.is_coordinator
            d[zone.player_name]['transport.state'] = device.get_current_transport_info()[
                'current_transport_state']
        response = jsonify({'devices': d}), status.HTTP_200_OK
    else:
        response = jsonify({'status': 'no devices found'}
                           ), status.HTTP_504_GATEWAY_TIMEOUT
    return response


@bp.route('/v1/<name>', methods=['GET'])
def getDeviceByName(name=str):
    if not (by_name(name) == None):
        device = by_name(name)
        current_transport_info = device.get_current_transport_info()
        current_track_info = device.get_current_track_info()
        response = jsonify(current_transport_info,
                           current_track_info), status.HTTP_200_OK
    else:
        response = jsonify({'status': 'device ' + name +
                            ' not found'}), status.HTTP_504_GATEWAY_TIMEOUT
    return response


@bp.route('/v1/<name>/volume/<volume>', methods=['PUT'])
def updateDeviceVolume(name=str, volume=int):
    try:
        device = by_name(name)
        previous_volume = str(device.volume)
        device.volume = volume
    except:
        response = jsonify({'status': 'device not found'}
                           ), status.HTTP_504_GATEWAY_TIMEOUT
    else:
        response = jsonify({'status': 'okay',
                            'previous_volume': previous_volume,
                            'current_volume': volume}), status.HTTP_202_ACCEPTED
    return response
