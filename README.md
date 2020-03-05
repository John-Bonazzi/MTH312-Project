# MTH312-Project
The project consist in a game with the player against the computer.

After selecting the set of **rules**, the player will have to create a password. The length and what symbols can be put in the password are defined in the rules.

The computer will try to break the code and obtain the password.

## Game Mechanichs
The computer will receive **hints** every *x* amount of seconds. The hint is a random letter from the password (the position of the letter in the password will be given as well).

## Game Over
conditions for the game over are basically two: the computer takes too much time, or it finds the password. The time limit can either be defined as a time on the clock, or by the amount of hints received.

## Rules
Rules will change what the player can put in a password, for example just using letters, or allowing numbers and symbols as well. Basically, the rules will mirror some of the password requirement that are usually found on the web.

**Note:** rules will either be a preset of game modes, or a more comprehensive selection of options where the player can choose the values manually.

## Options
Through the interface, the player will be able to set their own preferences for the game, like how many hints to give the computer, the time limit, and the time that has to pass between hints.

**Note:** in the future the Rules and Options might be part of the same preferences' tab in the interface.

## Additions
If I can figure out a good randomizer, we might make use of multi-threading to have the computer execute more operations at a time (from 1 to 8 for example), and can be toggled in the options.

That will be a thing only if I can find a way to avoid having threads running the same random values and repeating the same work.

## Checklist of features
- [ ] basic game with mechanics
- [ ] Rules added
- [ ] Game Over conditions based on rules added
- [ ] Options & preferences added
- [ ] Multi-threading support