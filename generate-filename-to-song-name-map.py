# Get the first line of every file in directory and subdirectories, print filename comma first line
# Usage: python get-first-line.py <directory>

import os
import sys
import re

def get_first_line(filename):
  # Open file
  f = open(filename, 'r')

  # Get first line
  first_line = f.readline()

  # Close file
  f.close()

  return first_line

# Call get_first_line for every file in a directory and its subdirectories
def get_first_line_for_all_files(directory):
  lines = []
  for root, dirs, files in os.walk(directory):
    for filename in files:
      # Get full path of file
      full_path = os.path.join(root, filename)

      # Get first line of file
      first_line = get_first_line(full_path)

      # Print filename and first line
      #print(f"{filename}|{first_line}")
      lines.append(f"{filename}|{first_line}")
  return lines

def extract_song_titles(lines):
    """
    Extract song titles from provided metadata.

    Args:
    - lines (list): List of strings in the format "filename|metadata".

    Returns:
    - List of strings in the format "filename|answer".
    """
    answers = []
    for line in lines:
      answers.append(extract_answer_from_line(line))

    return answers

def refined_extract_answer_from_line(line):
    filename, metadata = line.split('|')

    # Extract the first 5 characters (or fewer, if a non-alphabetical character is encountered) from the filename
    try:
      keyword = re.match(r'[a-zA-Z0-9]{1,5}', filename).group()
    except:
      if filename.startswith('___Ready'):
        keyword = "...Re"
    original_keyword = keyword

    # Convert capitalization changes to spaces
    keyword = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', keyword)
    # Convert capital I followed by another capital to include a space between
    keyword = re.sub(r'(?<=I)(?=[A-Z])', ' ', keyword)

    if keyword.startswith("Dont"):
        keyword = "Don’t"
    elif keyword.startswith("Im "):
        keyword = "I’m "
    elif keyword.startswith("Its "):
        keyword = "It’s "


    # Function to insert a character at a specific index in a string
    def insert_char(string, index, char):
        return string[:index] + char + string[index:]

    matches = re.findall(rf"({keyword}(?!.*{keyword}).*) Lyrics", metadata, flags=re.IGNORECASE)

    # If no match found with the initial keyword, try inserting spaces or apostrophes
    if not matches:
        for i in range(len(original_keyword)):
            for char in [' ', '’']:
                modified_keyword = insert_char(original_keyword, i, char)
                
                matches = re.findall(rf"({modified_keyword}(?!.*{modified_keyword}).*?) Lyrics", metadata, flags=re.IGNORECASE)
                if matches:
                    answer = matches[-1]
                    answer = answer.replace("Lyrics", "").replace("[Verse 1]", "").strip()
                    return f"{filename}|{answer}"

    # If matches are found with the original or modified keyword, extract the first match as the answer
    elif matches:
        answer = matches[-1]
        answer = answer.replace("Lyrics", "").replace("[Verse 1]", "").strip()
        return f"{filename}|{answer}"

    print(f'Error: No metadata matches for original-keyword="{original_keyword}" keyword="{keyword}": {filename}|{metadata}')
    return f"{filename}|Not Found"

if __name__ == "__main__":
  if len(sys.argv) < 2:
    target_dir = "data/original-albums/"
  else:
    target_dir = sys.argv[1]
  
  ## Test Lines
  # lines = [
  #    "'57 ContributorsTranslationsFrançaisСрпскиEnglishPortuguêsTaylor Swift - Babe (Taylor’s Version) [From the Vault] (ترجمه\u200cی فارسی)Babe (Taylor’s Version) [From the Vault] Lyrics[Intro]\n'"
  # ]

  ## All Lines
  lines = get_first_line_for_all_files(target_dir)

  for line in lines:
    # refined_extract_answer_from_line(line)
    print(refined_extract_answer_from_line(line))
    # print(line)
