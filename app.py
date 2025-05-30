
from flask import Flask, render_template, request, jsonify
import random
import os
import threading
from playsound import playsound

app = Flask(__name__)

# Simple linked list node for playlist
class SongNode:
    def __init__(self, song):
        self.song = song
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None

    def add_song(self, song):
        new_node = SongNode(song)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def remove_song(self, song):
        temp = self.head
        prev = None
        while temp:
            if temp.song == song:
                if prev:
                    prev.next = temp.next
                else:
                    self.head = temp.next
                return True
            prev = temp
            temp = temp.next
        return False

    def get_all_songs(self):
        songs = []
        temp = self.head
        while temp:
            songs.append(temp.song)
            temp = temp.next
        return songs

    def shuffle(self):
        songs = self.get_all_songs()
        random.shuffle(songs)
        self.head = None
        for s in songs:
            self.add_song(s)

playlist = Playlist()

current_song_thread = None

def play_song(song_path):
    playsound(song_path)

@app.route('/')
def index():
    return render_template('index.html', songs=playlist.get_all_songs())

@app.route('/add_song', methods=['POST'])
def add_song():
    song = request.json.get('song')
    if song:
        playlist.add_song(song)
        return jsonify({'status': 'success', 'songs': playlist.get_all_songs()})
    return jsonify({'status': 'error', 'message': 'No song provided'})

@app.route('/remove_song', methods=['POST'])
def remove_song():
    song = request.json.get('song')
    if song and playlist.remove_song(song):
        return jsonify({'status': 'success', 'songs': playlist.get_all_songs()})
    return jsonify({'status': 'error', 'message': 'Song not found'})

@app.route('/shuffle', methods=['POST'])
def shuffle():
    playlist.shuffle()
    return jsonify({'status': 'success', 'songs': playlist.get_all_songs()})

@app.route('/play', methods=['POST'])
def play():
    global current_song_thread
    song = request.json.get('song')
    song_path = os.path.join('static', 'songs', song)
    if current_song_thread and current_song_thread.is_alive():
        # Ideally, you would stop the current song before playing another,
        # but playsound does not support stopping. This is a limitation.
        pass
    current_song_thread = threading.Thread(target=play_song, args=(song_path,))
    current_song_thread.start()
    return jsonify({'status': 'playing', 'song': song})

if __name__ == '__main__':
    # Preload some songs (you'll need to add real mp3s into static/songs)
    playlist.add_song('song1.mp3')
    playlist.add_song('song2.mp3')
    app.run(debug=True)
