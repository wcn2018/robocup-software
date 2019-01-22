import main
import robocup
import behavior
import constants
import enum

import standard_play
import evaluation.ball
import evaluation
import evaluation.passing_positioning
import tactics.coordinated_pass
import tactics.defensive_forward
import tactics.simple_zone_midfielder
import skills.move
import skills.capture

class basic_distract(standard_play.StandardPlay):

    # how far the 2 support robots should stay away from the striker


    class State(enum.Enum):
        # Collect the ball / Full cou rt defense
        setup1 = 1
        # Dribble for a second and prepare to pass / shoot / clear
        setup2 = 2
        # Pass when someone is open
        passing = 3
        # Shoot when chances are high
        shooting = 4

    def __init__(self):
        super().__init__(continuous=False) 
        self.passsetup1 = robocup.Point(2.5,4.5)
        self.passsetup2 = robocup.Point(2.1, 5.0)
        self.passsetup3 = robocup.Point(2.5, 5.5)
        self.passsetup4 = robocup.Point(2.2, 6.0)
        self.distract1 = robocup.Point(2.8, 6.5)
        self.distract2ball = robocup.Point(2.6, 8)
        self.striker = robocup.Point(-2.5, 7.5)
        self.ball_is_far = False

        self.add_state(basic_distract.State.setup1, behavior.Behavior.State.running)
        self.add_state(basic_distract.State.setup2, behavior.Behavior.State.running)
        self.add_state(basic_distract.State.passing, behavior.Behavior.State.running)
        self.add_state(basic_distract.State.shooting, behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
                            basic_distract.State.setup1, lambda: True,'immediate')
        self.add_transition(basic_distract.State.setup1,
                            basic_distract.State.setup2, lambda: self.ball_is_far,
                            'if ball is far from goal')
        self.add_transition(basic_distract.State.setup1,
                            basic_distract.State.passing, lambda: self.all_subbehaviors_completed(),
                            '')
        self.add_transition(basic_distract.State.setup2,
                            basic_distract.State.passing, lambda: self.all_subbehaviors_completed(),
                            '')
        self.add_transition(basic_distract.State.passing,
                            basic_distract.State.shooting, lambda: self.all_subbehaviors_completed(),
                            '')

    def on_enter_setup1(self):
        self.add_subbehavior(skills.capture.Capture(), 'initial_capture')
        self.add_subbehavior(skills.move.Move(self.striker), 'shooter_position')
        self.add_subbehavior(skills.move.Move(robocup.Point(1,4.5)), 'intermediate_move') # moves a third robot to an intermediate point, ready to capture in setup2 or move to distract1
        
    def execute_setup1(self):
        print(self.subbehavior_with_name('shooter_position').is_done_running())
        print(self.subbehavior_with_name('initial_capture').is_done_running())
        if self.subbehavior_with_name('shooter_position').is_done_running() and self.subbehavior_with_name('initial_capture').is_done_running():
            print("big check \n")
            self.ball_is_far = (main.ball().pos.y < 4.5)

    def on_exit_setup1(self):
        self.remove_all_subbehaviors()



    def on_enter_setup2(self): #
        print("BIG GAY 2 \n \n")
        self.add_subbehavior(skills.move.Move(robocup.Point(0,4.5)), 'move to center')# move the one to center
    def execute_setup2(self):
        if self.subbehavior_with_name('move to center').is_done_running():
            self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(robocup.Point(0,4.5)), 'pass to center bot') # this move will keep on running like an idiot.
            # because it's in execute. Add a skill or a new state to put it in enter.
            if self.subbehavior_with_name('pass to center bot').is_done_running(): # skills are just plays that run on one robot. make it and put it in the skills folder.
            # 
                self.add_subbehavior(skills.capture.Capture(), 'grab ball') 
    
    def on_exit_setup2(self):
        self.remove_all_subbehaviors()



    def on_enter_passing(self):
        self.add_subbehavior(skills.move.Move(self.distract1), 'a')
        self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.distract1), 'b')
        self.add_subbehavior(skills.capture.Capture(), 'c')
        self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.striker), 'd')
        self.add_subbehavior(skills.capture.Capture(), 'e')
    
    def on_exit_passing(self):
        self.remove_all_subbehaviors()



    def on_enter_shooting(self):
        self.kick = skills.pivot_kick.PivotKick()
        self.kick.target = robocup.Point(0,9)


    def on_exit_passing(self):
        self.remove_all_subbehaviors()