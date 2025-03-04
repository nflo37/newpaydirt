#!/usr/bin/env python3

import pygame
import yaml
import os
from termcolor import colored
import random



class Playsheet:
    
    def __init__(self, yaml_file):

        yaml_file_path = f"/home/nickflo/newpaydirt/playsheets/{yaml_file}"
    
        with open(yaml_file_path, 'r') as f:
            self.yaml_data = yaml.safe_load(f)

        self.team_info = self.yaml_data['team_info']
        self.offense = self.yaml_data['offense']
        self.defense = self.yaml_data['defense']
        self.special_teams = self.yaml_data['special_teams']



class Team:
    """
    Player class

    Attributes:
        name:       Team Name
        teamsheet:  Teams Playsheet
        score:      Team score
        timeouts:   Timeouts remaining 
    """
    def __init__(self, team_name):
        self.name = team_name
        self.teamsheet = Playsheet(f"{self.name}.yaml")
        self.score = 0
        self.timeouts = 3
        self.possesion = False
        self.selected_play = ""

class Game:
    """
    Game class keeps track of game metadata

    Attributes:
        home_team:  Team instance for home player
        away_team:  Team instance for away player
        ball_position: Position of ball
    """
    
    KICKOFF_PLAYS  = ["Kickoff", "Onside Kick"]
    KICKOFF_RETURN_PLAYS = ["Kickoff Return"]
    OFFENSE_PLAYS = ["Line Plunge", "Off Tackle", "End Run", "Draw", "Screen",
                      "Short Pass", "Medium Pass", "Long", "Sideline"]
    DEFENSE_PLAYS  = ["Standard", "Nickel", "Dime", "Prevent", "Blitz"]

    def __init__(self):
        #Initial game state is for kickoff
        self.ball_position = 15              #Think 50yd line will map to 0. So for kickoff 35-> (15 or -15)
        self.down = 0 
        self.distance = 0
        self.quarter = 1
        self.seconds = 15*6  #Quarter is 15 min long. 10 second increments
        self.game_over = False
        self.user_team = False
        self.comp_team = False #TODO should i show these here even tho they get set later?
        self.play_phase = False

        #TODO game has a direction it is being played in
        self.direction = "left"   #Game starts moving right to left

    
    def run_game(self):
        """
        Phase based game approach

        start_phase:
            Player selects team
            Sets up game state for a kickoff

        pre_play_phase:
            Display game state
            Allow user to select and display play

        evaluate_play_phase:
            Determine result of both team play selections

        post_play_phase:
            Update game state based on play resolution

        """

        self.start_phase()

        while not self.game_over:
            self.pre_play_phase()
            self.evaluate_play_phase()
            self.post_play_phase() #TODO pickup here, update game state

    def start_phase(self, user_team=False, comp_team=False):
        """
        User selects a team and selects computer team
        Setup for kickoff
        """

        if not user_team and comp_team:
            user_team, comp_team = self.select_teams()
        self.user_team = Team(user_team)
        self.comp_team = Team(comp_team)
        
        #User team will just start with ball for now
        #TODO Coin toss
        #TODO Game options like quarter length?
        self.user_team.possesion = True
        self.setup_kickoff()

    def select_teams(self):
        """
        Team selection based on playbooks in /playsheets
        """

        playsheets = [x.split(".yaml")[0] for x in os.listdir("/home/nickflo/newpaydirt/playsheets") if x.endswith("yaml")]
        
        print("Select a user team")
        user_team = self.select_team(playsheets)
        print(f"User team is {user_team}\n")

        print("Select a computer team")
        comp_team = self.select_team(playsheets)
        print(f"Computer team is {comp_team}")

        return user_team, comp_team

        
    def select_team(self, playsheets):
        for index, playsheet in enumerate(playsheets):
            print(f"[{index}]: {playsheet}")

        while True:
            user_input = input("Choice: ")
            try:
                num=int(user_input)
                if not 0 <= num < len(playsheets):
                    continue
                break
            except ValueError:
                print("Enter a valid number")

        return playsheets[num]

    def setup_kickoff(self):
        """
        kickoff placement depends on direction of game. 
        Assuming always going left to right

        Whoever does not have possesion kicks off
        Ball starts on -15 yard line (35 yd line left to right)
        Down is 0 

        Should we indicate that the game is in a special teams state??
        How to indicate that special teams playsheet sections will need to be used
        """
        
        self.ball_position = -15
        self.down = 0
        self.yards = 0
        self.play_state = "kickoff"


    def pre_play_phase(self):
        """
        Display the game state
            Score, Down+Distance, Timouts Left, game board
            Not printing any game board info for now

            Allow user player to select a play, pick random computer play
                Should user have option to call timeout before?

            Display play selection
        """

        self.print_game_state()
        self.select_plays()
        self.print_play_selection()

    def print_play_selection(self):
        user_string = f"{self.user_team.name} selected {self.user_team.selected_play}"
        print(f'{colored(user_string, "red", "on_white", attrs=["bold"])}')
        comp_string = f"{self.comp_team.name} selected {self.comp_team.selected_play}"
        print(f'{colored(comp_string, "blue", "on_white", attrs=["bold"])}')


    def select_plays(self):
        """
        User selects play based on play_state
            TODO handle punts/field goals
        Select a random play for a computer
        
        Returns user_play and comp_play
        """

        play_choices = ""
        num_plays = 0

        if self.play_state == "kickoff":
            plays = Game.KICKOFF_PLAYS
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
                num_plays = len(plays)
                comp_play = "Kickoff Return"

        elif self.play_state == "offense":
            plays = GAME.OFFENSE_PLAYS
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
                num_plays = len(plays)
                comp_play = random.choice(Game.DEFENSE_PLAYS)

        elif self.play_state == "defense":
            plays = GAME.DEFENSE_PLAYS
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
                num_plays = len(plays)
                comp_play = random.choice(Game.OFFENSE_PLAYS)
            
        while True:
            user_input = input(play_choices)
            try:
                num=int(user_input)
                if not 0 <= num < num_plays:
                    continue
                break
            except ValueError:
                print("Enter a valid number")

        user_play = plays[num]

        #return user_play, comp_play
        self.user_team.selected_play = user_play
        self.comp_team.selected_play = comp_play

    
    def evaluate_play_phase(self):
        """
        Determine and display results based on selected play. 
        This is the core of the game logic and rules.
        
        For now, just have yardage results
        TODO (Incomplete, fumble, penalites, Breakaway, all special teams)

        Update game state
        """

        user_play_outcomes = self.get_play_outcomes(self.user_team)
        comp_play_outcomes = self.get_play_outcomes(self.comp_team)

        #TODO check for all non-yardage scenarios 

        #print(self.user_team.teamsheet.defense)
        user_roll = random.choice(list(user_play_outcomes.items())) 
        comp_roll = random.choice(list(comp_play_outcomes.items()))
        
        result, result_string = self.get_play_result(user_roll[1], comp_roll[1])

        self.display_play_results(user_roll, comp_roll, result_string)

    def get_play_result(self, user_result, comp_result):
        if self.play_state == "kickoff":
            result = abs(user_result - comp_result)
            result_string = f"Kickoff: Net {result} yards"

        return result, result_string

    def display_play_results(self, user_roll, comp_roll, result_string):
        """
        _roll is a tuple of (roll, result)
        """
        user_dice = user_roll[0]
        comp_dice = comp_roll[0]
        user_result = user_roll[1]
        comp_result = comp_roll[1]

        user_string = f"{self.user_team.name} rolled a {user_dice} for {user_result} yards"
        comp_string = f"{self.comp_team.name} rolled a {comp_dice} for {comp_result} yards"
        if int(user_result) > 0 :
            user_string = colored(user_string, "green")
        else:
            user_string = colored(user_string, "red")
        if int(comp_result) > 0 :
            comp_string = colored(comp_string, "green")
        else:
            comp_string = colored(comp_string, "red")
    
        print(user_string)
        print(comp_string)
        print(colored(result_string, "yellow", attrs=["blink"]))


    def get_play_outcomes(self, player):
        
        play_outcomes = ""

        if(player.selected_play in self.KICKOFF_PLAYS):
            play_outcomes = player.teamsheet.special_teams[player.selected_play]
        elif(player.selected_play in self.KICKOFF_RETURN_PLAYS):
            play_outcomes = player.teamsheet.special_teams[player.selected_play]
        elif(player.selected_play in self.OFFENSE_PLAYS):
            play_outcomes = player.teamsheet.offense[player.selected_play]
        elif(player.selected_play in self.DEFENSE_PLAYS):
            play_outcomes = player.teamsheet.defense[player.selected_play]

        return play_outcomes

        
    def print_game_state(self):
        print(f'SCORE:    {colored(self.user_team.name, "red", attrs=["bold"])}: {self.user_team.score} - {self.comp_team.name}: {self.comp_team.score}')
        print(f"Timeouts  {colored(self.user_team.name, attrs=['bold'])}: {self.user_team.timeouts}   {self.comp_team.name}: {self.comp_team.timeouts}")
        print(f"{self.down} and {self.distance} on the {self.convert_yardage()} ")

    def convert_yardage(self):
        if self.ball_position <= 0:
            return self.ball_position + 50
        else:
            return 50 - self.ball_position






def main():
    #team = Team("atlanta_falcons")
    #teamsheet = Playsheet("/home/nickflo/newpaydirt/playsheets/atlanta_falcons.yaml") 
    #print(teamsheet.special_teams)

    game = Game()
    game.start_phase("atlanta_falcons", "dallas_cowboys")
    game.pre_play_phase()
    game.evaluate_play_phase()


main()
