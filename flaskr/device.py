import functools
import soco
import urllib

from soco.discovery import by_name
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)


bp = Blueprint('device', __name__, url_prefix='/devices')


@bp.route('/list', methods=['GET'])
def listAvailableDevices():
    devices = []
    for zone in soco.discover():
        devices.append(zone.player_name)
        print("Found " + zone.uid + " named " + zone.player_name + " at volume " +
              str(zone.volume) + " which is coordinator? " + str(zone.is_coordinator))
    return jsonify({'devices': devices}), 200


@bp.route('/inspect/<name>')
def inspectDevice(name=str):
    print(str(name))
    device = by_name(name)
    return jsonify(device.get_current_transport_info(), device.get_current_track_info()), 200

@bp.route('/volume/<name>/<volume>', methods=['PUT'])
def setVolume(name=str, volume=int ):
    device = by_name(name)
    previous_volume =  str(device.volume)
    device.volume = volume
    return jsonify({'status':'okay',
                    'previous_volume':previous_volume,
                    'current_volume':volume})