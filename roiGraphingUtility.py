# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:41:52 2023

@author: Stephen Mouch
"""

import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

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
    # Dates for the simulation
    start_date = '2006-10-27'
    end_date = '2014-05-14'
    
    # Prompt user to enter their own numbers or select randomly
    choice = input("Enter '1' to select your own numbers or '2' to have numbers selected randomly: ")
    if choice == '1':
        user_numbers = input("Enter 5 unique numbers between 1 and 39, separated by spaces: ")
        user_numbers = list(map(int, user_numbers.split()))
        if len(user_numbers) != 5 or len(user_numbers) != len(set(user_numbers)) or not all(1 <= num <= 39 for num in user_numbers):
            print("Invalid input. Please enter 5 unique numbers between 1 and 39.")
            return
    elif choice == '2':
        user_numbers = random.sample(range(1, 40), 5)
        numbers = random.sample(range(1, 40), 5)
        
    # Simulation controls
    num_simulations = 50  # Number of simulations to run
    roi_user_cumulative = np.zeros(num_simulations)  # Store cumulative ROI for user-selected scenario
    roi_random_cumulative = np.zeros(num_simulations)  # Store cumulative ROI for randomly-selected scenario
    roi_reselected_cumulative = np.zeros(num_simulations)  # Store cumulative ROI for reselected every day scenario

    for i in range(num_simulations):
        # User-selected scenario
        
        _, _, roi_user, _ = simulate_game(start_date, end_date, user_numbers)
        roi_user_cumulative[i] = roi_user_cumulative[i-1] + roi_user if i > 0 else roi_user

        # Randomly-selected scenario
        numbers = random.sample(range(1, 40), 5)
        _, _, roi_random, _ = simulate_game(start_date, end_date, numbers)
        roi_random_cumulative[i] = roi_random_cumulative[i-1] + roi_random if i > 0 else roi_random

        # Reselected every day scenario
        _, _, roi_reselected, _ = simulate_game(start_date, end_date, numbers, reselect=True)
        roi_reselected_cumulative[i] = roi_reselected_cumulative[i-1] + roi_reselected if i > 0 else roi_reselected

    # Plot the results
    plt.plot(roi_user_cumulative, label='User-selected numbers')
    plt.plot(roi_random_cumulative, label='Randomly-selected numbers')
    plt.plot(roi_reselected_cumulative, label='Reselected numbers every day')
    plt.legend(loc='upper right')
    plt.xlabel('Simulation Run')
    plt.ylabel('Cumulative ROI')
    plt.title('Cumulative ROI for Different Scenarios over Multiple Simulations')

    plt.xticks(range(num_simulations), range(1, num_simulations+1))  # Set the simulation run numbers as x-axis tick labels

    
    plt.show()

if __name__ == "__main__":
    main()