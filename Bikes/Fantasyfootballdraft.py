import pandas as pd
from tabulate import tabulate
from colorama import Fore, Style

# Load the CSV file
file_path = 'EFL (1).csv'
df = pd.read_csv(file_path)

# Clean the dataframe by removing any unnecessary columns (like 'Unnamed: 0')
df = df.drop(columns=['Unnamed: 0'])

# Lists to keep track of picks
your_picks = []
other_teams_picks = []

# Function to color-code based on position
def colorize_position(pos):
    if pos == 'QB':
        return Fore.RED + pos + Style.RESET_ALL
    elif pos == 'RB':
        return Fore.GREEN + pos + Style.RESET_ALL
    elif pos == 'WR':
        return Fore.BLUE + pos + Style.RESET_ALL
    elif pos == 'TE':
        return Fore.MAGENTA + pos + Style.RESET_ALL
    elif pos == 'K':
        return Fore.YELLOW + pos + Style.RESET_ALL
    elif pos == 'DEF':
        return Fore.CYAN + pos + Style.RESET_ALL
    else:
        return pos

# Function to display the best available players
def display_best_available(df):
    # Sort by Rank
    available_players = df.sort_values('Rank').reset_index(drop=True)
    available_players['Pos'] = available_players['Pos'].apply(colorize_position)
    print(tabulate(available_players[['Rank', 'Player', 'Pos', 'Team', 'Bye', 'Consensus', 'FP', 'Ceiling', 'MVP']].head(24), headers='keys', tablefmt='fancy_grid'))

# Function to remove a player from the list once they are picked
def pick_player(df, player_rank):
    df = df[df['Rank'] != player_rank]
    return df

# Function to display your current team
def display_your_team(your_picks_df):
    if not your_picks_df.empty:
        your_picks_df['Pos'] = your_picks_df['Pos'].apply(colorize_position)
        print("\nYour current team:")
        print(tabulate(your_picks_df[['Rank', 'Player', 'Pos', 'Team', 'Bye', 'Consensus', 'FP', 'Ceiling', 'MVP']], headers='keys', tablefmt='fancy_grid'))
    else:
        print("\nYour team is currently empty.")

# Initial display of the best available players
print("Best available players:")
display_best_available(df)

# Draft simulation loop
while True:
    pick = input("\nEnter the rank of the player picked (or type 'done' to finish): ").strip()

    if pick.lower() == 'done':
        print("Draft complete. Here are your picks:")
        display_your_team(pd.DataFrame(your_picks))
        break

    try:
        rank = int(pick)
    except ValueError:
        print("Invalid rank. Please enter a valid rank number.")
        continue

    team = input("Is this your pick? (yes/no): ").strip().lower()

    if team == 'yes':
        player_info = df[df['Rank'] == rank]
        if not player_info.empty:
            your_picks.append(player_info.iloc[0])
            display_your_team(pd.DataFrame(your_picks))
        else:
            print("Player with the given rank not found.")
    else:
        other_teams_picks.append(rank)

    # Remove the picked player from the dataframe
    df = pick_player(df, rank)

    # Display the updated list of best available players
    print("\nBest available players:")
    display_best_available(df)


