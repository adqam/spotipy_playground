import spotipy
import pprint as pp
import emoji

''' shows recommendations for the given artist
'''

from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

artist_list = ["Prince", "Childish Gambino", "Daft Punk", "Press Club"]

def artist_recommender(list_of_artists):

    output_list = []

    def exact_matcher(match_term, item_list):
        if len(item_list) > 0:
            for i in item_list:
                if i != match_term:
                    exact_match_flag = 0
                else:
                    exact_match_flag = 1
                    break
            if exact_match_flag == 1:
                return i
            else:
                return None
        else:
            return None

    def get_artist(name):
        results = sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        results_list = [nm['name'] for nm in items]
        print(results_list)
        exact_match = exact_matcher(match_term=name, item_list = results_list)
        if len(items) > 0:
            if exact_match:
                print("Exact match artist found!")
                exact_match_output = [nm for nm in items if nm['name'] == exact_match]
                return exact_match_output[0]
            else:
                print("No exact match found. Returning results for first close match: " + items[0]['name'])
                return items[0]
        else:
            print(name + " not found. " + emoji.emojize(':pensive:', use_aliases=True))
            return None

    def show_recommendations_for_artist(artist):
        results = sp.recommendations(seed_artists=[artist['id']])
        track_list = []
        for track in results['tracks']:
            print(track['name'], '-', track['artists'][0]['name'])
            track_list.append(track['name'] + '-' + track['artists'][0]['name'])
        return track_list


    for performer in artist_list:
        artist = get_artist(performer)
        if artist:
            recos = show_recommendations_for_artist(artist)
            output_list.append(recos)
        else:
            print("Can't find that artist.")
            continue

    output_list = [x for sublist in output_list for x in sublist]
    pp.pprint(output_list, indent=4)

artist_recommender(artist_list)