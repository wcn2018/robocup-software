import robocup
import play
import behavior
import skills.move
import skills.capture
import tactics.coordinated_pass
import constants
import main
import enum

class firstPlay(play.Play):
    class State(enum.Enum):
        setup = 1
        passing = 2
        shooting = 3

    def __init__(self):
        super().__init__(continuous = True)
        self.add_state(firstPlay.State.setup.behavior.Behavior.state.running)
        self.add_state(firstPlay.State.passing.behavior.Behavior.state.running)
        self.add_state(firstPlay.State.shooting.behavior.Behavior.state.running)
        self.add_transition(behavior.Behavior.State.start,
                            TrianglePass.State.setup, lambda: True,'immediate')
        self.add_transition(behavior.Behavior.State.start,
                            TrianglePass.State.passing, lambda: self.all_subbehaviors_completed(),
                            '')
        self.add_transition(behavior.Behavior.State.start,
                            TrianglePass.State.shooting, lambda: self.all_subbehaviors_completed(),
                            '')
        self.pass_bhvr = tactics.coordinated_pass.CoordinatedPass()
        self.hold1 = robocup.Point(-1.5,6.5)
        self.hold2 = robocup.Point(1.5,6.5)
        self.kick = skills.pivot_kick.PivotKick()

    def on_enter_setup(self):
        # Add subbehaviors to place robots in a triangle
        #
        self.add_subbehavior(skills.move.Move(self.hold1), "point 1")
        self.add_subbehavior(skills.move.Move(self.hold2), "point 2")
        self.add_subbehavior(skills.capture.Capture(), "capturing")

        pass

    def on_exit_setup(self):
        # Remove all subbehaviors, so we can add new ones for passing
        self.shootProb = evaluation.shooting.eval_shot( main.ball().pos, main.our_robots() )
        self.passProb1 = evaluation.passing.eval_pass( main.ball().pos, self.hold1, main.our_robots() )
        self.passProb2 = evaluation.passing.eval_pass( main.ball().pos, self.hold2, main.our_robots() )
        #put these options in a dictionary and then sort it.
        self.dc = {"shoot": self.shootProb,"pass1": self.passProb1,"pass2": self.passProb2}
        self.dc.sort()
        self.remove_all_subbehaviors()

    def on_enter_passing(self):
        #finds the most probably action
        self.actionName = self.dc.keys().pop()
        self.action = self.dc.items().pop()
    
    def on_exit_passing(self):
        if not self.actionName == "shoot":  
            self.add_subbehavior(self.pass_bhvr, 'pass')
            self.pass_bhvr.receive_point = self.action
        self.remove_all_subbehaviors()

    def on_enter_shooting(self):
        
        self.add_subbehavior(self.kick, 'shoot')
        kick.target = (0,Field.Length)
        
        if not self.has_subbehaviors():
            pass

    def on_exit_passing(self):
        self.remove_all_subbehaviors()






