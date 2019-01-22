import robocup
import standard_play
import behavior
import constants
import main
import skills.move
import skills.capture
import enum
import evaluation
import tactics.coordinated_pass
import tactics.defense
import play


class distraction1(standard_play.StandardPlay):
    setup = 1
    setuptwo = 2
    setupthree = 3
    passing = 4
    shoot = 5

    class State (enum.Enum):
        setup = 1
        setuptwo = 2
        setupthree = 3
        passing = 4
        cross = 5
        shoot = 6
    
    def __init__(self):
        super().__init__(continuous=False)  

        self.ball_is_far = False
        
        self.add_state(distraction1.State.setup,
                        behavior.Behavior.State.running)
        self.add_state(distraction1.State.setuptwo,
                        behavior.Behavior.State.running)
        self.add_state(distraction1.State.setupthree,
                        behavior.Behavior.State.running)
        self.add_state(distraction1.State.passing,
                        behavior.Behavior.State.running)
        self.add_state(distraction1.State.cross,
                        behavior.Behavior.State.running)
        self.add_state(distraction1.State.shoot,
                        behavior.Behavior.State.running)
        
        
        self.add_transition(behavior.Behavior.State.start,
                        distraction1.State.setup, lambda: True, 'immediately')

        self.add_transition(distraction1.State.setup,
                        distraction1.State.passing, lambda: not self.ball_is_far,'1-passing')

        #setuptwo can be skipped if ball is not far from goal
        self.add_transition(distraction1.State.setup,
                        distraction1.State.setuptwo, lambda: self.ball_is_far and
                        self.subbehavior_with_name('striker moves').is_done_running(),'1-2')

        self.add_transition(distraction1.State.setuptwo,
                        distraction1.State.setupthree, lambda: self.subbehavior_with_name('move half').is_done_running() and
                        self.subbehavior_with_name('move to distract').is_done_running() , '2-setupthree')

        self.add_transition(distraction1.State.setupthree,
                        distraction1.State.passing, lambda: self.subbehavior_with_name('center pass').is_done_running(), 'setupthree-passing')

        self.add_transition(distraction1.State.passing,
                        distraction1.State.cross, lambda: (self.has_subbehavior_with_name('distract pass') and self.subbehavior_with_name('distract pass').is_done_running() )
                        , 'passing-crossing')

        self.add_transition(distraction1.State.passing,
                        distraction1.State.shoot, lambda: (self.has_subbehavior_with_name('striker pass') and self.subbehavior_with_name('striker pass').is_done_running() ),'pass-shoot' )

        self.add_transition(distraction1.State.cross,
                        distraction1.State.shoot, lambda: self.subbehavior_with_name('pass to striker').is_done_running()
                        , 'pls shoot')

        self.add_transition(distraction1.State.shoot,
                        distraction1.State.setup, lambda: self.has_subbehavior_with_name('shooting') and self.subbehavior_with_name('shooting').is_done_running(), 'repeat')

        
        self.d1 = robocup.Point(0.40*constants.Field.Width, 0.95*constants.Field.Length) #the first distraction point
        self.d2 = robocup.Point(0.40*constants.Field.Width, 0.8*constants.Field.Length) #the second distraction point
        self.s1 = robocup.Point(-0.40*constants.Field.Width,0.9*constants.Field.Length) #striker's position
        self.center = robocup.Point(0,4.5) #center of field position, used if ball is far
        

    def on_enter_setup(self):
        print("entered setup")
        self.add_subbehavior(skills.capture.Capture(), 'capture1')
        self.add_subbehavior(skills.move.Move(self.s1), 'striker moves')
        self.add_subbehavior(skills.move.Move(self.d2), 'distract moves')
        
        self.ball_is_far = main.ball().pos.y < 4
        


    def on_exit_setup(self):
        print("exits setup")
        self.remove_all_subbehaviors()
        

    def on_enter_setuptwo(self):
        print("entered setup2")
        self.add_subbehavior(skills.capture.Capture(), 'capture 2')
        self.add_subbehavior(skills.move.Move(self.center), 'move half')
        self.add_subbehavior(skills.move.Move(self.s1), 'stay')
        

    def on_exit_setuptwo(self):
        print('exits setuptwo')
        self.remove_all_subbehaviors()

    def on_enter_setupthree(self):
        self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.center), 'center pass')
        self.add_subbehavior(skills.move.Move(self.d2), "move back to distract")


    def on_exit_setupthree(self):
        self.remove_all_subbehaviors()

    def on_enter_passing(self):
        print('entered passing')
        
        
        passchance1 = evaluation.passing.eval_pass( main.ball().pos, self.d2, main.our_robots() )
        passchance2 = evaluation.passing.eval_pass( main.ball().pos, self.s1, main.our_robots() )
        passchance3 = evaluation.passing.eval_pass( self.d2, self.s1, main.our_robots() )
        shotchance1 = evaluation.shooting.eval_shot( self.s1, main.our_robots() )

        if passchance1 >= passchance2*shotchance1:
                self.add_subbehavior(skills.move.Move(self.s1), 'stay2 ')
                
                self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.d2), 'distract pass')
                

        else:
                self.add_subbehavior(skills.move.Move(self.d1), 'stay2')
                
                self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.s1), 'striker pass')


    def on_exit_passing(self):
        print('exit passing')
        self.remove_all_subbehaviors()

    def on_enter_cross(self):
        print('enter cross')
        self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.s1),'pass to striker')
        self.add_subbehavior(skills.move.Move(self.d1), 'move distract')
        self.add_subbehavior(skills.move.Move(self.d2), 'shift right')
        

    def on_exit_cross(self):
        print('exit cross')
        self.remove_all_subbehaviors()

    def on_enter_shoot(self):
        print('enter shoot')
        passchance1 = evaluation.passing.eval_pass( main.ball().pos, self.d2, main.our_robots() )
        passchance2 = evaluation.passing.eval_pass( main.ball().pos, self.s1, main.our_robots() )
        passchance3 = evaluation.passing.eval_pass( self.d2, self.s1, main.our_robots() )
        passchance4 = evaluation.passing.eval_pass( self.s1, self.d2, main.our_robots() )
        shotchance1 = evaluation.shooting.eval_shot( self.s1, main.our_robots() )
        shotchance2 = evaluation.shooting.eval_shot( self.d2, main.our_robots() )

        if passchance4*shotchance2 > shotchance1:
                
                self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(self.d2), 'distract pass')
                self.add_subbehavior(skills.move.Move(self.s1), 'stay3')
                self.add_subbehavior(skills.pivot_kick.PivotKick(), 'shooting')
                

        else:
                self.add_subbehavior(skills.move.Move(self.d2), 'stay2')
                self.add_subbehavior(skills.move.Move(self.d1), 'stay3')
                self.add_subbehavior(skills.pivot_kick.PivotKick(), 'shooting')