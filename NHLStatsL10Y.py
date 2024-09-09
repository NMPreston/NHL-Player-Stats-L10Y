import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the data
url = 'https://www.quanthockey.com/nhl/seasons/last-10-nhl-seasons-players-stats.html'

# Sends a request to the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Finds the table containing the data
table = soup.find('table')

# Parses the table 
df = pd.read_html(str(table))[0]

# Make the multi-level columns into a single level 
df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Display available columns (statistics) for the user to choose from
def display_available_columns():
    print("\nAvailable columns (statistics):")
    for i, column in enumerate(df.columns):
        print(f"{i + 1}. {column}")

# Menu function to output for the user's input
def menu():
    print("\nWhat would you like to do?")
    print("1. Search by player name")
    print("2. Search by statistic")
    print("3. Show available columns (statistics)")
    print("4. Quit")
    return input("Enter your choice (1-4): ")

# Function to search player stats by name
def search_by_player(df):
    player_name = input("Enter the player's name: ")
    """
    This meant taking the name from the website and translating it for the code to execute correctly
    """
    if 'Unnamed: 2_level_0_Name' in df.columns:
        player_stats = df[df['Unnamed: 2_level_0_Name'].str.contains(player_name, case = False, na = False)]
        if not player_stats.empty:
            print(f"\nStats for {player_name}:")
            print(player_stats)
        else:
            print(f"No stats found for {player_name}.")
    else:
        print("'Name' column not found. Available columns are:")
        print(df.columns)

# Searches by a specific statistic
def search_by_stat(df):
    display_available_columns()  # Show columns before asking for statistic input
    stat = input("\nEnter the statistic (e.g., Overall_G, Assists_ESA, Points_ESP): ")
    
    if stat in df.columns:
        top_players = df[['Unnamed: 2_level_0_Name', stat]].sort_values(by=stat, ascending=False).head(10)
        print(f"\nTop 10 players by {stat}:")
        print(top_players)
    else:
        print(f"Statistic '{stat}' not found. Available statistics: {df.columns}")

# Loop for output 
while True:
    choice = menu()
    
    if choice == '1':
        search_by_player(df)
    elif choice == '2':
        search_by_stat(df)
    elif choice == '3':
        display_available_columns()  # Display the available columns
    elif choice == '4':
        print("Exiting program.")
        break
    else:
        print("Invalid choice, please try again.")
