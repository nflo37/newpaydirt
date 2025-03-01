#!/usr/bin/env python3

import pygame
import yaml
import os



class Playsheet:
    
    def __init__(self, yaml_file_path):
    
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
        self.possesion = self.home_team
        self.down = 0 
        self.distance = 0
        self.quarter = 1
        self.seconds = 15*6  #Quarter is 15 min long. 10 second increments
        self.game_over = False

        #TODO game has a direction it is being played in
        self.direction = left   #Game starts moving right to left

    
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

        self.select_teams()

    def select_teams(self):
        """
        Team selection based on playbooks in /playsheets
        """
        playsheets = os.listdir("/home/nickflo/newpaydirt/playsheets")
        print(playsheets)



def main():
    #team = Team("atlanta_falcons")
    #teamsheet = Playsheet("/home/nickflo/newpaydirt/playsheets/atlanta_falcons.yaml") 
    #print(teamsheet.special_teams)

    game = Game()
    game.select_teams()


main()
