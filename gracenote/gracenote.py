import pygn

clientID='# insert your client ID here #'
userID='# insert your user ID here #'

print('UserID', userID)

artist = 'Led Zeppelin'
song   = 'Stairway to Heaven'
artist = 'against me'
# song = 'a joy in all i can see'
song = 'a joy'

artist = '10,000 Maniacs'
song = 'What''s The Matter Here'

artist = 'Metallica'
song = 'Nothing else matters'

artist = 'Leonard Cohen'
song='Hallelujah'

metadata = pygn.search(clientID=clientID, userID=userID, artist=artist, track=song)
print(metadata)

# print metadata

print('album_artist_name: ', metadata['album_artist_name'])
print('track_title:       ', metadata['track_title'])

print('album_title:       ', metadata['album_title'])
print('album_year:        ', metadata['album_year'])
origin = metadata['artist_origin']
print('artist_origin:     ', origin['1']['TEXT'], '-', origin['2']['TEXT'], '-',
                             origin['3']['TEXT'])
genre = metadata['genre']
print('genre:             ', genre['1']['TEXT'], '-', genre['2']['TEXT'], '-',
                             genre['3']['TEXT'])
artist_type = metadata['artist_type']
print('artist_type:       ', artist_type['1']['TEXT'], '-', artist_type['2']['TEXT'])

era = metadata['artist_era']
if '2' not in era:
	era['2'] = {'TEXT': ''}

print('era:               ', era['1']['TEXT'], '-', era['2']['TEXT'])

