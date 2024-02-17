# Python Multi-line slot machine

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Project Notes](#project-notes)

## Description
This python slot machine allows logged in and authenticated users to manage their balance and place bets, based on an 8+ multi-line slot system. This version utilises a 3*3 slot grid, however the programme is flexible to allow the creator to adjust for matrix sizes.


**Tech-stack: python / SQLite / Bcrypt / smtplib / HTML5**

**Project Areas: User login + authentication with bcrypt and password hashing, email security updates with account blocking features, SQLite database management and integration, dynamic programming including varied payouts and bonus round megawins **

## Installation

1. Clone the repository:

   ```bash
   gh repo clone wells1989/Python_slot_machine_Project

2. Install dependencies:

   ```bash
   pip install -r requirements.txt 

## Usage
### Logging in / User authentication
- The app uses a SQLite built-in database to store users along with key information (hashed_passwords, balances, if they are blocked users etc)
- The app allows for a maximum of 3 failed password attempts before the user is blocked and unable to access the programme, in which case a warning email will be sent to the users' email, for them to change their password etc.

### Playing / Balance management etc
- The user can alter bet size according to their balance, and deposit / withdraw at any time.
- The symbols in the slot are randomly generated out of several options, each with it's own payout and probability of occurence. 
- The symbols in the slot are shown to the user via the spin() function and if there are winning symbols the user also sees them in the winning_symbols grid, in addition to key winnings and balance information.

#### Winning Lines
**Payouts: * (bonus round triggered) A * 8 B * 5 C * 3.5 D * 3 E * 2.5 F * 2**
![Screenshot (562)](https://github.com/wells1989/Full-stack-blog/assets/122035759/188dc7e3-4594-415c-88d9-812cca2c10f6)

### 

### Project Notes:
- This programme was designed to be user and admin friendly, allowing easy modification of e.g. the symbols or the slot column / row sizes to increase variability
- The SQLite database was used for the first version due to it being easily integrated within the python environment
- This project was inspired by an earlier practice project, and I wanted to implement a programme which could be incorporated into real world slot websites etc.

#### Future-development:
- For extra variance the lines could have been further adjusted to allow for partial-line payouts or users to manually adjust the individual lines they are betting on.
- To improve user engagement the User model could have been altered to include random user bonuses or them to sign up to certain campaigns to win free bets or random prizes.
- This project focused on back-end and database functionality, although adding a front end UI and API functionalities would not only provide a more visually pleasing appearance but would help with certain functionalities, for example resetting user passwords via forms.
