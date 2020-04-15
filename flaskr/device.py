import functools
import soco
import urllib

from soco.discovery import by_name
from collections import defaultdict
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)


bp = Blueprint('device', __name__, url_prefix='/devices')


@bp.route('/list', methods=['GET'])
def listAvailableDevices():
    d = {}
    for zone in soco.discover():
        d[zone.player_name]={}
        device = by_name(zone.player_name)
        #devices.append(zone.player_name)
        d[zone.player_name]['zone.player_name'] = zone.player_name
        d[zone.player_name]['zone.uid'] = zone.uid
        d[zone.player_name]['zone.volume'] = zone.volume
        d[zone.player_name]['zone.is_coordinator'] = zone.is_coordinator
        d[zone.player_name]['transport.state'] = device.get_current_transport_info()['current_transport_state']

        #print("Found " + zone.uid + " named " + zone.player_name + " at volume " +
        #     str(zone.volume) + " which is coordinator? " + str(zone.is_coordinator))
    print(d)
    return jsonify({'devices': d}), 200


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