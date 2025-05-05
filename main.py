import streamlit as st
import pandas as pd
from collections import deque

# Path to the CSV file (Make sure this file is included in your deployed folder)
CSV_FILE_PATH = "word_list.csv"  # Change this to the actual file name

# Load word list from CSV (using st.cache_data)
@st.cache_data  # Cache the data to avoid reloading each time
def load_word_list():
    # Read the CSV file
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Assuming words are in a column named 'word'
    # You can adjust this column name based on your CSV structure
    word_list = set(df['word'].str.lower())  # Convert all words to lowercase for consistency
    
    return word_list

# Function to get neighbors
def get_neighbors(word, word_list):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i+1:]
            if new_word != word and new_word in word_list:
                neighbors.append(new_word)
    return neighbors

# Function to find the shortest path using BFS
def bfs(start, end, word_list):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        current_word, path = queue.popleft()

        if current_word == end:
            return path

        for neighbor in get_neighbors(current_word, word_list):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

# Streamlit UI
st.title("Word Ladder Game")

# Load word list from the local CSV file
word_list = load_word_list()

# User inputs
word_length = st.number_input("Enter desired word length:", min_value=3, max_value=10, value=5)
start_word = st.text_input(f"Enter start word ({word_length} letters):").lower()
end_word = st.text_input(f"Enter end word ({word_length} letters):").lower()

# Check inputs
if start_word and end_word:
    if len(start_word) != word_length or len(end_word) != word_length:
        st.error(f"Both words must be exactly {word_length} letters long.")
    elif start_word not in word_list or end_word not in word_list:
        st.error("One or both words are not valid in the dictionary.")
    else:
        # Run BFS and show results
        path = bfs(start_word, end_word, word_list)
        if path:
            st.success(f"Shortest transformation: {' -> '.join(path)}")
        else:
            st.warning("No valid transformation path found.")
