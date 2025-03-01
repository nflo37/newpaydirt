#!/usr/bin/env python3

import pygame
import yaml
import os



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

class Game:
    """
    Game class keeps track of game metadata

    Attributes:
        home_team:  Team instance for home player
        away_team:  Team instance for away player
        ball_position: Position of ball
    """
    def __init__(self):
        #Initial game state is for kickoff
        self.ball_position = 15              #Think 50yd line will map to 0. So for kickoff 35-> (15 or -15)
        self.down = 0 
        self.distance = 0
        self.quarter = 1
        self.seconds = 15*6  #Quarter is 15 min long. 10 second increments
        self.game_over = False

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

        play_selection_phase:
            Allow user to select a play

        play_resolution_phase:
            Determine result of both team play selections

        post_play_phase:
            Update game state based on play resolution

        """

        self.start_phase()

        #while not self.game_over:

    def start_phase(self):
        """
        User selects a team and selects computer team
        Setup for kickoff
        """

        user_team, comp_team = self.select_teams()
        self.user_team = Team(user_team)
        self.comp_team = Team(comp_team)
        
        #User team will just start with ball for now
        #TODO Coin toss
        #TODO Game options?
        self.user_team.possesion = True

    def setup_kickoff():
        """
        kickoff placement depends on direction of game. 
        Assuming always going left to right

        Whoever does not have possesion kicks off
        Ball starts on -15 yard line (35 yd line left to right)
        Down is 0 

        Should we indicate that the game is in a special teams state??
        How to indicate that special teams playsheet sections will need to be used

        """

    


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



def main():
    #team = Team("atlanta_falcons")
    #teamsheet = Playsheet("/home/nickflo/newpaydirt/playsheets/atlanta_falcons.yaml") 
    #print(teamsheet.special_teams)

    game = Game()
    game.start_phase()


main()
