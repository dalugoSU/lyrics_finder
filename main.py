import tkinter as tk
from tkinter import StringVar
import requests

root = tk.Tk()
root.minsize(600,600)
root.maxsize(600,600)
root.title("Lyrics Finder")


class song_lyrics:

    def find_song(self, song_title, song_artist):
        '''
            get the closest matching song to title and artist using the track.search api call
            return the first track
        '''
        # API key and URL from my musixmatch account (Trial)
        key = "YOUR API KEY" # musixmatch API
        url = "https://api.musixmatch.com/ws/1.1/track.search"

        # API Key is part of your params (Thank you angela for the clarification on this)
        parameters = {'apikey': key, 'q_track': song_title, 'q_artist': song_artist}
        response = requests.get(url, params=parameters)

        # turn response into python object
        tracks = response.json()
        song_id = tracks['message']['body']['track_list'][0]['track']['track_id']  # Index song ID from object

        return song_id

    def get_lyrics(self, track_id):
        '''
            get the closest matching song to title and artist using the track.lyrics.get api call
            return the lyrics as text string
        '''
        # API Key gotten from mismusix account $ Request URL from musixmach for track.lyrics.get
        API_key = 'YOUR API KEY' # musixmatch API
        url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get"

        # parameters for my search (taken from the musixmatch website)
        parameters = {'track_id': track_id, 'apikey': API_key}
        response = requests.get(url, params=parameters)

        # Turn response into a python object
        lyrics = response.json()
        lyrics = lyrics['message']['body']['lyrics']['lyrics_body']

        # return lyrics
        return lyrics

    def sentiment(self, text):
        '''
            returns the sentiment of the given text. up to you as to whether it returns just 'pos', 'neg', 'neutral' or more information
        '''
        # API Key and Endpoint from Azure's resource. Url using endpoint and sentiment analytics API URL.
        API_key = "YOUR API KEY"
        endpoint = "YOUR ENDPOINT"
        url = f'{endpoint}text/analytics/v3.0/sentiment'

        # Header with API Key, Documents with text parameter to analyze.
        header = {'Ocp-Apim-Subscription-Key': API_key}
        documents = {'documents': [{'id': '1', 'text': text}]}

        # Request using requests with url, header key and documents to analyze
        response = requests.post(url, headers=header, json=documents)
        entity = response.json()

        # Return the sentiment only (Pos, Neg, Neutral, Mixed)
        return entity['documents'][0]['sentiment']


lyrics = song_lyrics()

song_name = StringVar()
song_artist = StringVar()

def restart():
    bottom_frame_text.delete('1.0', tk.END) # removes text from bottom text box everytime you run it

def post_lyrics():
    song = song_name.get()
    artist = song_artist.get()

    try:
        song_id = lyrics.find_song(song, artist)
        get_lyrics = lyrics.get_lyrics(song_id)

        try:
            get_lyrics = list(get_lyrics.split('\n'))  # Turn lyrics into a list split by new lines
            if ('******* This Lyrics is NOT for Commercial use *******') in get_lyrics:
                get_lyrics.remove(
                    '******* This Lyrics is NOT for Commercial use *******')  # Remove this mark from all lyrics
                get_lyrics.pop(-1)  # Remove the number code after the 'not for commercial use' disclaimer
                lyricsToString = ' '.join([str(elem) for elem in get_lyrics])
            else:
                lyricsToString = ' '.join([str(elem) for elem in get_lyrics])  # Turn lyrics back into a string
        except TypeError:
            bottom_frame_text.insert(tk.END,
                                     "Top Song option does not contain any lyrics! ")  # In case query doesn't return any lyrics

        bottom_frame_text.insert(tk.END, f"               ***** Lyrics *****")

        for word in lyricsToString.split('\n'):
            bottom_frame_text.insert(tk.END, f"\n\n{word}")

        sentiment = lyrics.sentiment(lyricsToString)
        bottom_frame_text.insert(tk.END, f"\n\n\nSong Lyric Sentiment: {sentiment}")

    except TypeError:
        bottom_frame_text.insert(tk.END, f"\n\n\n\n\n\n\n\nMISING EITHER SONG TITLE OR ARTIST\n OR LYRICS NOT FOUND")
    except IndexError:
        bottom_frame_text.insert(tk.END, f"\n\n\n\n\n\n\n\n               MISSPELLINGS FOUND")


main_frame = tk.Frame(root, bg='dark grey')
main_frame.pack(fill='both', expand=True)

top_frame_song_entry = tk.Entry(main_frame, textvariable=song_name)
top_frame_song_entry.place(relx=0.2, rely=0.15)

top_frame_artist_entry = tk.Entry(main_frame, textvariable=song_artist)
top_frame_artist_entry.place(relx=0.5, rely=0.15)

artist_label = tk.Label(main_frame, text='Artist Name', bg='dark grey')
artist_label.place(relx=0.57, rely=0.1)

artist_label = tk.Label(main_frame, text='Song Name', bg='dark grey')
artist_label.place(relx=0.27, rely=0.1)

submit_button = tk.Button(main_frame, text='Submit', command=lambda: [restart(), post_lyrics()])
submit_button.place(relx=0.44, rely=0.22)

bottom_frame = tk.Frame(main_frame, bg='light yellow')
bottom_frame.place(relheight=0.7, relwidth=1, rely=0.3)

bottom_frame_text = tk.Text(bottom_frame, bg='light yellow')
bottom_frame_text.place(relheight=0.8, relwidth=0.8, relx=0.1, rely=0.12)


root.mainloop()
