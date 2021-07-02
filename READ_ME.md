# Développez un programme logiciel en Python

## Description
This programm has been redacted in order to organize chess tournaments and to store informations about past ones.
The organizer will be able at any moment to:
  -Start a new tournament
  -Enter a new player in the database
  -Generate a round for an onging tournament
  -Enter results for a finished round
  -Consult reports about past or ongoing tournaments
  -Consult informations about a player in the database
  -Change the elo rank of a player
  -Look at the final/provisional  ranking for a finished/ongoing tournament.
 
 
## Execution
### How to implement the virtual environment:
The first step is to create a virtual environment in order to install the required libraries.

1- create your environment with the command "py -m venv env"

2- activate it with the command "env\script\activate"

3- install the needed libraries with the command "pip install -r requirements.txt"

### Script execution
Get into the correct folder using terminal command. Then run the following command.

```sh
python main.py 
```
The user will have the main menue displayed in the terminal.
To begin an action, the user has to enter an integer corresponding to the action.

To shut the programm down, the user just has to press "Ctrl + c" in the terminal.

### Generate a flake8-html report.
This action shall be executed either on a separated terminal or with the programm not running.
Get into the correct folder using terminal command. Then run the following command.

```sh
flake8 --format=html --htmldir=flake-report
```
--htmldir=flake-report will create a new folder with all html files. The user can give it the name he wants by changing "flake-report" designation.

## Dependencies


## Licences
the MIT license (MIT)
