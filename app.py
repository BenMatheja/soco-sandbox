import soco
from soco.discovery import by_name
from soco.music_services import MusicService
# for zone in soco.discover():
#     print(zone.player_name)
# device = soco.discovery.any_soco()
# print(device)
#device.play()
device = by_name("Wohnzimmer")
print(device.get_current_transport_info()['current_transport_state'])

#queue = device.clear_queue()
queue = device.get_queue()
#print(queue)
#print(device.music_library.list_library_shares())
print('My current track is')
print(device.get_current_track_info())
print('switching to')
#device.next()
print(device.get_current_track_info())
print ('Device Volume ' + str(device.volume))
device.volume +=3
print ('Device Volume is now at ' + str(device.volume + 3 ))
#device.get_accounts()
#print(MusicService.get_subscribed_services_names())
#spotify = MusicService('Spotify')

