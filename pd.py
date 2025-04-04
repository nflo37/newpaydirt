#!/usr/bin/env python3

import pygame
import yaml
import os
from termcolor import colored
import random
from gui import FootballField


class Playsheet:
    
    def __init__(self, yaml_file):

        #yaml_file_path = f"/home/nickflo/newpaydirt/playsheets/{yaml_file}"
        yaml_file_path = f"./playsheets/{yaml_file}"
    
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
        #self.possesion = False
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
    SP_OFFENSE_PLAYS = ["Field Goal", "Punt"]
    DEFENSE_PLAYS  = ["Standard", "Nickel", "Dime", "Prevent", "Blitz"]
    POST_TD_PLAYS = ["2pt Attempt", "XP"]

    def __init__(self):
        #Initial game state is for kickoff
        self.ball_position = 15              #Think 50yd line will map to 0. So for kickoff 35-> (15 or -15)
        self.down = 0 
        self.distance = 0
        self.quarter = 1
        self.seconds = 15*60  #Quarter is 15 min long. 10 second increments
        self.game_over = False
        self.user_team = False
        self.comp_team = False #TODO should i show these here even tho they get set later?
        self.play_state = False
        self.possession = False


        #TODO game has a direction it is being played in
        self.direction = "right"   #Game starts moving left to right

    
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
            Display the play outcome

        post_play_phase:
            Update game state based on play resolution

        """

        self.start_phase()

        while not self.game_over:
            self.pre_play_phase()
            result = self.evaluate_play_phase()  #Net yards from play
            self.post_play_phase(result)

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
        self.possession = self.user_team
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
        
        if self.direction == "right":
            self.ball_position = -15
        else:
            self.ball_position = 15

        self.down = 0
        self.distance = 0
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
            if self.possession == self.user_team:
                plays = Game.KICKOFF_RETURN_PLAYS
            elif self.possession == self.comp_team:
                plays = Game.KICKOFF_PLAYS

            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
            comp_play = "Kickoff Return"

        elif self.play_state == "offense":
            plays = Game.OFFENSE_PLAYS + Game.SP_OFFENSE_PLAYS
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
            comp_play = random.choice(Game.DEFENSE_PLAYS)

        elif self.play_state == "defense":
            plays = Game.DEFENSE_PLAYS
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
            comp_play = random.choice(Game.OFFENSE_PLAYS)

        elif self.play_state == "post_touchdown":
            if self.possession == self.user_team:
                plays = Game.POST_TD_PLAYS
                for index,play in enumerate(plays):
                    play_choices = play_choices + f"[{index}]: {play}\n"
                comp_play = "Field Goal"
            elif self.possession == self.comp_team:
                comp_play = random.choice(Game.POST_TD_PLAYS)
                if comp_play == "XP":
                    self.play_state = "XP"
                    self.user_team.selected_play = "Field Goal"
                    self.comp_team.selected_play = "Field Goal"
                    return
                elif comp_play == "2pt Attempt":
                    self.play_state = "2pt Attempt"
                    print(f"{self.possession.name} are going for 2")
                    plays =  Game.DEFENSE_PLAYS
                    for index,play in enumerate(plays):
                        play_choices = play_choices + f"[{index}]: {play}\n"
                    comp_play = random.choice(Game.OFFENSE_PLAYS)
                #We need to know if comp is going for 1 or 2 to be able to select a play
            
        user_play = self.user_play_selection(play_choices, plays)
        user_play, comp_play = self.check_post_td_play(play_choices, plays,  user_play, comp_play)
        user_play, comp_play = self.check_for_field_goal(user_play, comp_play)

        self.user_team.selected_play = user_play
        self.comp_team.selected_play = comp_play


    def check_for_field_goal(self, user_play, comp_play):
        if user_play == "Field Goal":
            comp_play = "Field Goal"
            self.play_state = "Field Goal"

        return user_play, comp_play

    def user_play_selection(self, play_choices, plays):

        num_plays = len(plays)
        while True:
            user_input = input(play_choices)
            try:
                num=int(user_input)
                if not 0 <= num < num_plays:
                    continue
                break
            except ValueError:
                print("Enter a valid number")

        selected_play = plays[num]

        return selected_play


    def check_post_td_play(self, play_choices, plays, user_play, comp_play=False):
        #We have to convert the play selection to actual playsheet play
        if user_play == "XP":
            user_play = "Field Goal"
            self.play_state = "XP"
        elif user_play == "2pt Attempt":
            #Allow user to select an offensive play if they go for 2
            self.play_state = "2pt Attempt"
            plays = Game.OFFENSE_PLAYS
            play_choices = ""
            for index,play in enumerate(plays):
                play_choices = play_choices + f"[{index}]: {play}\n"
            comp_play = random.choice(Game.DEFENSE_PLAYS)

            user_play = self.user_play_selection(play_choices, plays)
        
        return user_play, comp_play


    
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

        #TODO check for all non-yardage scenarios (need to add these to playsheet) 
        #Need to handle special roll for if user/comp is on defense
        if self.play_state == "offense" or self.play_state == "2pt Attempt":
            #Check for if computer is going for 2
            if self.possession == self.comp_team:
                user_roll = random.choice(list(user_play_outcomes[self.comp_team.selected_play].items()))
                comp_roll = random.choice(list(comp_play_outcomes.items()))
            else:
                user_roll = random.choice(list(user_play_outcomes.items()))  #[play, yardage]?
                comp_roll = random.choice(list(comp_play_outcomes[self.user_team.selected_play].items()))
        elif self.play_state == "defense":
            user_roll = random.choice(list(user_play_outcomes[self.comp_team.selected_play].items()))
            comp_roll = random.choice(list(comp_play_outcomes.items()))
        elif self.play_state == "Field Goal":
            if self.possession == self.user_team:
                user_roll = random.choice(list(user_play_outcomes.items()))  #[play, yardage]?
                comp_roll = [1, 0]
            else:
                comp_roll = random.choice(list(user_play_outcomes.items()))  #[play, yardage]?
                user_roll = [1, 0]
        elif self.play_state == "XP":
            if self.possession == self.user_team:
                user_roll = random.choice(list(user_play_outcomes.items()))
                comp_roll = [1, 30]     #XP = FG-30yds 
            else:
                comp_roll = random.choice(list(user_play_outcomes.items()))
                user_roll = [1, 30]     #XP = FG-30yds 
        else:
            user_roll = random.choice(list(user_play_outcomes.items()))
            comp_roll = random.choice(list(comp_play_outcomes.items()))

        user_roll_num = user_roll[0]
        comp_roll_num = comp_roll[0]
        user_result = user_roll[1]
        comp_result = comp_roll[1]

        result, result_string = self.get_play_result(user_result, comp_result)
        self.display_play_results(user_roll, comp_roll, result_string)

        return result


    def get_play_result(self, user_result, comp_result):
        
        #result = abs(user_result - comp_result)

        if self.play_state == "kickoff":
            if self.possession == self.user_team:
                result = comp_result - user_result
            else:
                result = user_result - comp_result
            result_string = f"Kickoff: Net {result} yards"
        elif self.play_state == "offense" or self.play_state == "defense" or self.play_state == "2pt Attempt":
            result = user_result + comp_result
            result_string = f"{self.possession.name} gained {result} yards"
        elif self.play_state == "XP":
            if self.possession == self.user_team:
                result = user_result - comp_result
            else:
                result = comp_result - user_result
            result_string = f"XP: Net {result} yards"
        elif self.play_state == "Field Goal":
            result = user_result - comp_result
            result_string = f"Field Goal: {result} yards"

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
        elif(player.selected_play in self.SP_OFFENSE_PLAYS):
                play_outcomes = player.teamsheet.special_teams[player.selected_play]


        return play_outcomes


    def post_play_phase(self, result):
        """
        Update game state 
            Ball position
            Check for touchdown
            Check for firstdown
            update down and distance accordingly
            Update clock (TODO allow for timeout first?)

        self.ball_position = 15              #Think 50yd line will map to 0. So for kickoff 35-> (15 or -15)
        self.down = 0 
        self.distance = 0
        self.quarter = 1
        self.seconds = 15*6  #Quarter is 15 min long. 10 second increments
        """
        #TODO what about Special teams plays?

        self.update_ball_position(result)

        if self.play_state == "Field Goal":
            #Check if field goal is good, update score
            self.handle_fieldgoal(result)
        elif self.play_state == "XP":
            self.check_XP(result)
            self.swap_possession()
            #self.update_game_direction()
            self.setup_kickoff()
        elif self.play_state == "2pt Attempt":
            self.check_attempt(result)
            self.swap_possession()
            self.update_game_direction()
            self.setup_kickoff()
        elif self.play_state == "kickoff":
            self.down = 1
            self.set_distance()
            self.update_game_clock(10)
            self.update_game_direction()
            self.transition_from_kickoff()
            if self.check_for_touchback():
                return
        elif self.check_for_touchdown():
            #Display TD, Update game clock only 10 seconds, Update score 
            self.display_touchdown()
            self.update_game_clock(10)
            self.update_game_score(6)
            if self.direction == "left":
                self.ball_position = -48
            else:
                self.ball_position = 48
            self.down = 0
            self.distance = 0
            self.play_state = "post_touchdown"
        elif self.check_for_firstdown(result):
            self.down = 1
            self.set_distance()
            self.update_game_clock(40)
        elif self.check_for_turnover_on_downs():
            self.down = 1
            self.set_distance()
            self.swap_possession()
            self.update_game_direction()
            self.update_game_clock(10)
        else:
            self.down = self.down + 1
            self.distance = self.distance - result
            self.update_game_clock(40)
        
        #TODO handle end of game/quarter

    def handle_fieldgoal(self, result):

        self.update_game_clock(10)
        
        if abs(self.ball_position) > 50:
            score_message = f'Field Goal is good {self.possession.name}!!!'
            self.update_game_score(3)
            self.swap_possession()
            self.setup_kickoff()
        else:
            score_message = f'Field Goal is NO good {self.possession.name}!!!'
            self.update_ball_position(result * -1) #We need to move the ball back to where the kick happened 
            self.down = 1
            self.set_distance()
            self.update_game_direction()
            self.swap_possession()

        print(colored(score_message, "cyan"))


    def set_distance(self):
        if self.first_and_goal():
            self.distance = 50 - abs(self.ball_position)
        else:
            self.distance = 10 


    def first_and_goal(self):
        if self.direction == "left" and self.ball_position <= -40:
            return True
        elif self.direction == "right" and self.ball_position >= 40:
            return True
        else:
            return False
    
    def check_attempt(self, result):
        if result >= 2:
            score_message = f'2pt attempt is good {self.possession.name}!!!!!'
            self.update_game_score(2)
        else:
            score_message = f'2pt attempt is no good {self.possession.name}!!!!!'
            
        print(colored(score_message, "cyan"))


    def check_XP(self, result):
        if result >= 0:
            score_message = f'XP is good {self.possession.name}!!!!!'
            self.update_game_score(1)
        else:
            score_message = f'XP is no good {self.possession.name}!!!!!'
            
        print(colored(score_message, "cyan"))




    def transition_from_kickoff(self):
        if self.play_state == "kickoff" and self.possession == self.user_team:
            self.play_state = "offense"
        elif self.play_state == "kickoff" and self.possession == self.comp_team:
            self.play_state = "defense"


    def update_game_direction(self):
        if self.direction == "right":
            self.direction = "left"
        else:
            self.direction = "right"

    def swap_possession(self):
        if self.possession == self.user_team:
            self.possession = self.comp_team
            self.play_state = "defense"
        else:
            self.possession = self.user_team
            self.play_state = "offense"
    
    def update_game_clock(self, time_elapsed):
        self.seconds = self.seconds - time_elapsed
    
    def update_game_score(self, points):
        self.possession.score = self.possession.score + points

    def update_ball_position(self, result):
        if self.direction == "right":
            self.ball_position = self.ball_position + result
        else:
            self.ball_position = self.ball_position - result

    def check_for_touchdown(self):
        if self.ball_position <= -50 or self.ball_position >= 50:
            return True
        else:
            return False

    def check_for_touchback(self):
        if self.ball_position <= -50 and self.direction == "left":
            return True
            self.ball_position = -25
        elif self.ball_position >= 50 and self.direction == "right":
            return True
            self.ball_position = 25
        else:
            return False

    def check_for_firstdown(self, result):
        if result >= self.distance:
            return True
        else:
            return False

    def check_for_turnover_on_downs(self):
        #We already know it wasnt a 1st down
        if self.down == 4:
            print(colored("Turnover on Downs", "yellow", attrs=["blink"]))
            return True
        else:
            return False
    
    def display_touchdown(self):
        touchdown_message = f'Touchdown {self.possession.name}!!!!!'
        print(colored(touchdown_message, "cyan"))

    def print_game_state(self):
        if self.possession == self.user_team:
            print(f'SCORE:    {colored(self.user_team.name, "red", attrs=["bold"])}: {self.user_team.score} - {self.comp_team.name}: {self.comp_team.score}')
        else:
            print(f'SCORE:    {self.user_team.name}: {self.user_team.score} - {colored(self.comp_team.name, "red", attrs=["bold"])}: {self.comp_team.score}')
        print(f"Timeouts  {colored(self.user_team.name, attrs=['bold'])}: {self.user_team.timeouts}   {self.comp_team.name}: {self.comp_team.timeouts}")
        print(f"Time Remaining: {self.seconds // 60}:{self.seconds % 60}")
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

    # Initialize pygame and create screen
    WIDTH  = 800
    HEIGHT = 600
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paydirt Football")
    
    # Create field visualization
    field = FootballField(screen, WIDTH, HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        game.pre_play_phase()
        result = game.evaluate_play_phase()
        game.post_play_phase(result)
        
        # Update the visual display
        field.draw(game)
        pygame.time.wait(100)  # Small delay to make the game playable

if __name__ == "__main__":
    main()
