
# Music Playlist Manager

A simple Flask web application to manage a music playlist using linked lists.

## Features
- Add songs by filename
- Remove songs
- Shuffle playlist
- Play songs (requires `.mp3` files in `static/songs/`)

## Setup

1. Install dependencies:
```
pip install flask playsound
```

2. Add your `.mp3` files inside `static/songs/`

3. Run the app:
```
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser

## Notes
- `playsound` may have limitations on stopping audio playback.
- You must have `.mp3` files present to play them.
