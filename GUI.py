import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

# Genius API credentials
API_TOKEN = 'YOUR_GENIUS_API_TOKEN'
BASE_URL = 'https://api.genius.com'

def fetch_lyrics(title, artist):
    """Fetch lyrics from Genius API based on song title and artist."""
    search_url = f"{BASE_URL}/search"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    params = {'q': f'{title} {artist}'}
    
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    
    if not data['response']['hits']:
        return "No lyrics found."
    
    # Get the first hit's URL
    song_url = data['response']['hits'][0]['result']['url']
    
    # Fetch the lyrics page
    song_response = requests.get(song_url)
    soup = BeautifulSoup(song_response.text, 'html.parser')
    lyrics = soup.find('div', class_='lyrics').get_text()
    
    return lyrics

def on_search_button_click():
    """Handle the search button click event."""
    title = title_entry.get()
    artist = artist_entry.get()
    
    if not title or not artist:
        messagebox.showwarning("Input Error", "Please enter both song title and artist.")
        return
    
    lyrics = fetch_lyrics(title, artist)
    lyrics_text.delete(1.0, tk.END)
    lyrics_text.insert(tk.END, lyrics)

# Create the main application window
root = tk.Tk()
root.title("Lyrics Extractor")

# Create and place widgets
tk.Label(root, text="Song Title:").grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Artist:").grid(row=1, column=0, padx=10, pady=10)
artist_entry = tk.Entry(root, width=50)
artist_entry.grid(row=1, column=1, padx=10, pady=10)

search_button = tk.Button(root, text="Search Lyrics", command=on_search_button_click)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

lyrics_text = tk.Text(root, wrap=tk.WORD, width=60, height=20)
lyrics_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
