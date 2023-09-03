import os
import re
import json

def load_pipe_separated_csv_to_map(filename):
    with open(filename, 'r') as f:
        content = f.readlines()
        return {line.split('|')[0].strip(): line.split('|')[1].strip() for line in content}

filename_to_song_name_map = load_pipe_separated_csv_to_map("./filename-to-song-name-map.txt")

def process_lyric_file_v12(lyrics, filename):
    """
    Process the lyric file to extract title (without replacing underscores), metadata line, and cleaned lyrics.
    Additionally, remove lines ending with "(digits)Embed" metadata.
    """
    # Extract the metadata line, removing everything before the match \u200b (zero-width space); also remove the Lyrics[.*] prefix
    metadata_line = lyrics[0].strip()

    # title = lyrics[0].split("\u200b")[-1].strip().split("Lyrics[")[0].strip()
    title = filename_to_song_name_map[filename]
    
    cleaned_lyrics = []
    # Filter out contextual references, empty lines, metadata; 
    for line in lyrics[1:]:
      if not (line.startswith('[') or line.strip() == ''):
        cleaned_lyrics.append(re.sub(r'\d+[Ee]mbed', '', line.strip()))
    return title, metadata_line, cleaned_lyrics


def recursively_load_and_process(base_path):
    """
    Recursively load and process lyric files from directories.
    """
    data = {}
    for root, dirs, files in os.walk(base_path):
        album = os.path.basename(root)
        songs = []
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as lyric_file:
                    lyrics = lyric_file.readlines()
                title, metadata_line, cleaned_lyrics = process_lyric_file_v12(lyrics, file)
                song_data = {
                    "album": album,
                    "title": title,
                    "metadata_line": metadata_line,
                    "lyrics": cleaned_lyrics
                }
                songs.append(song_data)
        if songs:
            data[album] = songs
    return data

def generate_acronym_map_whole_song_v2(album_song_data):
    """
    Updated function to generate the acronym map/dict for the provided songs considering entire song lyrics.
    This version ensures all lyrics are saved in lowercase and no duplicates appear.
    """
    acronym_map = {}
    
    for album, songs in album_song_data.items():
        for song in songs:
            title = song["title"]
            # Join the entire lyrics of the song into a single string
            whole_lyrics = " ".join(song["lyrics"]).lower()  # Convert lyrics to lowercase
            words = whole_lyrics.split()
            
            # Generate consecutive lyric initials ranging from 4 to 20 words
            for length in range(4, min(21, len(words) + 1)):
                for i in range(len(words) - length + 1):
                    acronym = "".join([word[0].upper() for word in words[i:i+length]])
                    sequence = " ".join(words[i:i+length])
                    if acronym:
                        if acronym not in acronym_map:
                            acronym_map[acronym] = []
                        # Check for duplicates and only add unique sequences
                        if (title, sequence) not in acronym_map[acronym]:
                            acronym_map[acronym].append((title, sequence))
    
    return acronym_map


data = recursively_load_and_process("data/original-albums")
#print(data)
acronym_map_updated = generate_acronym_map_whole_song_v2(data)
print(f"IKYWTWYWI: {acronym_map_updated['IKYWTWYWI']}")

# Create the acronyms directory to store the JSON files
acronyms_directory = "acronyms"
os.makedirs(acronyms_directory, exist_ok=True)

# Group the acronym map by acronym length
grouped_acronym_map = {}
for acronym, entries in acronym_map_updated.items():
    length = len(acronym)
    if length not in grouped_acronym_map:
        grouped_acronym_map[length] = {}
    grouped_acronym_map[length][acronym] = entries

# Save the grouped acronym map to JSON files sharded by acronym length again
saved_files = []
for length, data in grouped_acronym_map.items():
    filename = f"{acronyms_directory}/acronym_{length}.json"
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
    saved_files.append(filename)



#### Testing
#data = recursively_load_and_process("test")
#print(data)
#data2 = generate_acronym_map_whole_song_v2(data)
#print(data2)
#print(f"YMRIYW: {data2['YMRIYP']}")
