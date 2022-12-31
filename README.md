# Yahtzee #

## Overview ##
A basic executable Yahtzee game framework.

## Goals ##
The goals of this framework are to:  

    1. Create basic functionality for an interactive Yahtzee game.  
    2. Allow this to be the backbone for a Yahtzee game that plays itself.  
    
## Progress ##
The program currently has:

- [x] Basic functionality for an interactive Yahtzee game.

## Future Additions ##
In terms of future additions, we aim to :

- [ ] Implement the Yahtzee bonus functionality.
- [ ] Implement a sensible reward system including handling contribution to the bonus in the upper section and integrating chance.
- [ ] Implement functionality for determing the estimated best dice to hold on each roll of each turn for the highest reward selection.
- [ ] Allow the program to act on these predicted best moves to play the game itself without human intervention.
- [ ] Include the option to include bias to any/all dice.

## Running the Program ##
In order to run the program, open up an IDE (I used IDLE but it doesn't really matter), and run the file `yahtzee.py`. A window will open, where you can interact with the game, which looks as follows:  

![image](https://user-images.githubusercontent.com/62014208/210124046-1a8f8216-7315-42f5-ac04-3f317c220daf.png)

From here, you can roll the dice by pressing the 'Roll' button, and select which dice you would like to hold for the next roll by pressing the buttons directly underneath the respective die (you can release the die by selecting the same button again). You will get three rolls to maximise your score, where you can select at any point which subsection you would like to score your turn under. When you have selected the desired subsection, click the 'CONFIRM' button, and roll again for the next roll. This will continue until you have scored under each subsection, where the game will end. You can then press the 'Roll' button again to start the first roll of the first turn of the next game.
