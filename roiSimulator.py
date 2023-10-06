# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:41:52 2023

@author: Stephen Mouch
"""

import pandas as pd
import random
from datetime import datetime

df_numbers = pd.read_csv('Cash5-WinningNumbers.csv')
df_prizes = pd.read_csv('Cash5-Prizes.csv')

# Convert dates to datetime
df_numbers['Date'] = pd.to_datetime(df_numbers['Date'])
df_prizes['date'] = pd.to_datetime(df_prizes['date'])

# Define the rules of the game
cost_per_play = 1
prizes = [0, 0, 1, 5]  # prizes for 0, 1, 2, 3 matches

def simulate_game(start_date, end_date, numbers, reselect=False):
    total_spent = 0
    total_won = 0
    match_4_or_5 = 0

    for date in pd.date_range(start=start_date, end=end_date):
        total_spent += cost_per_play

        # Reselect numbers if required
        if reselect:
            numbers = random.sample(range(1, 40), 5)

        # Get winning numbers for the day
        winning_numbers = df_numbers[df_numbers['Date'] == date].iloc[0, 1:].values.tolist()

        # Calculate matches and prize won
        matches = len(set(numbers) & set(winning_numbers))
        if matches < 4:
            total_won += prizes[matches]
        else:
            prize_column = 'prize_5' if matches == 5 else 'prize_4'
            total_won += df_prizes[df_prizes['date'] == date][prize_column].values[0]
            match_4_or_5 += 1
    
    # Compute ROI
    roi = (total_won - total_spent) / total_spent * 100

    return total_spent, total_won, roi, match_4_or_5

def main():
    
    isRandom = False
    # Dates for the simulation
    start_date = '2006-10-27'
    end_date = '2014-05-14'
    
    
    # Prompt user to enter their own numbers or select randomly
    choice = input("Enter '1' to select your own numbers or '2' to have numbers selected randomly: ")

    # If user chooses to select their own numbers
    if choice == '1':
        numbers = input("Enter 5 unique numbers between 1 and 39, separated by spaces: ")
        numbers = list(map(int, numbers.split()))
        if len(numbers) != 5 or len(numbers) != len(set(numbers)) or not all(1 <= num <= 39 for num in numbers):
            print("Invalid input. Please enter 5 unique numbers between 1 and 39.")
            return
    elif choice == '2':
        numbers = random.sample(range(1, 40), 5)
        isRandom = True
    else:
        print("Invalid choice. Please enter either '1' or '2'.")
        return


   # Scenario 1: User-selected or randomly selected numbers
    total_spent_fixed, total_won_fixed, roi_fixed, fixed_match4or5 = simulate_game(start_date, end_date, numbers)
    if isRandom:
        print(f"Scenario 1 - Fixed numbers (randomly generated): {numbers}")
    else:
        print(f"Scenario 1 - Fixed numbers (user-selected): {numbers}")
    print(f"Total money spent: ${total_spent_fixed}")
    print(f"Total money won: ${total_won_fixed}")
    print(f"Return on investment: {roi_fixed:.2f}%\n")
    print(f"Four or Five number matches: {fixed_match4or5}\n")

    # Scenario 2: Reselecting numbers every day
    if choice == '2':
        total_spent_reselected, total_won_reselected, roi_reselected, reselected_match4or5  = simulate_game(start_date, end_date, numbers, reselect=True)
        print("Scenario 2 - Reselecting numbers every day")
        print(f"Total money spent: ${total_spent_reselected}")
        print(f"Total money won: ${total_won_reselected}")
        print(f"Return on investment: {roi_reselected:.2f}%")
        print(f"Four or Five number matches: {reselected_match4or5}\n")

if __name__ == "__main__":
    main()