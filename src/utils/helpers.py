import json
import matplotlib.pyplot as plt
from collections import Counter

def plot_title_frequencies(json_file):
    # Load JSON data from a file
    with open(json_file, 'r') as file:
        data = json.load(file)

    for item in data['results']:
        print(type(item))
        print(type(item['properties']))
        print(type(item['properties']['Name']))
        
        # Check if 'Name' and 'title' keys exist and 'title' is a list
        if 'Name' in item['properties'] and 'title' in item['properties']['Name'] and isinstance(item['properties']['Name']['title'], list):
            if item['properties']['Name']['title']:  # Check if the list is not empty
                title = item['properties']['Name']['title'][0]
                if 'plain_text' in title:  # Check if 'plain_text' key exists
                    print(title['plain_text'])  # Print the plain_text for debugging
                else:
                    print("No plain_text key found in title")
            else:
                print("Title list is empty")
        else:
            print("Name or title key not found, or title is not a list")
        
        try:
            titles = [item['properties']['Name']['title'][0]['plain_text'] for item in data['results'] if 'Name' in item['properties'] and 'title' in item['properties']['Name'] and isinstance(item['properties']['Name']['title'], list) and item['properties']['Name']['title']]
            print(titles)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Count the frequency of each title
    title_counts = Counter(titles)

    # Prepare data for plotting
    labels, values = zip(*title_counts.items())

    # Create bar chart
    plt.figure(figsize=(10, 8))
    plt.bar(labels, values, color='blue')
    plt.xlabel('Titles')
    plt.ylabel('Frequency')
    plt.title('Frequency of Titles in JSON Data')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show the plot
    plt.show()