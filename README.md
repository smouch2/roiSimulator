# roiSimulator
A return-on-investment simulator for 5-ball lottery games with visualization utility.

This program requires a prize CSV file and a winning number CSV file.  It uses these files to simulate wins as follows:
Match 0 numbers = $0.00
Match 1 number = $0.00
Match 2 numbers = $1.00
Match 3 numbers = $5.00
Match 4 numbers = Determine correct prize using the data in Cash5-Prizes.csv column ‘prize_4’
Match 5 numbers = Determine correct prize using the data in Cash5-Prizes.csv column ‘prize_5’

Rules for the Lotto Game:
- Each date is played only once, but every date is played
- Ball order does not matter, only matching
- Five winning numbers are selected every day
- It costs $1 to play per play
- All playable numbers are between 1 and 39, inclusively

Included is the capstone report, as well as the graphing code for general wins, 4 or 5 number matches, and given CSV files for the assignment.
