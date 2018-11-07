import robocup
import play
import behavior
import skills.move
import skills.capture
import tactics.coordinated_pass
import constants
import main
import enum

# Goals
# 1. Move robots into the shape of a triangle
# 2. Pass around the triangle

## A demo play written during a teaching session to demonstrate play-writing
# Three robots form a triangle on the field and pass the ball A->B->C->A and so on.
class TrianglePass(play.Play):
    class State(enum.Enum):
        ## 2 robots get on the corners of a triangle,
        # while a third fetches the ball
        setup = 1

        ## The robots continually pass to each other
        passing = 2

    def __init__(self):
        super().__init__(continuous=True)

        # register states - they're both substates of "running"
        # Feel free to modify these transitions if you would like to use the state
        # machine system to your advantage!
        self.add_state(TrianglePass.State.setup,
                       behavior.Behavior.State.running)
        self.add_state(TrianglePass.State.passing,
                       behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
                            TrianglePass.State.setup, lambda: True,
                            'immediately')
        self.add_transition(TrianglePass.State.setup,
                            TrianglePass.State.passing,
                            lambda: self.all_subbehaviors_completed(),
                            'all subbehaviors completed')

    pass_bhvr = tactics.coordinated_pass.CoordinatedPass()

        # This play runs forever, so it dosen't need a transition out of 'passing'

        # Define any member variables you need here:
        # Eg:
    r1 = robocup.Point(0,4.5)
    r2 = robocup.Point(-1,3.5)
    r3 = robocup.Point(1,3.5)
    i = 0
        # self.triangle_points = [<point 1>, <point 2>, <point 3>]

    def on_enter_setup(self):
        # Add subbehaviors to place robots in a triangle
        #
        self.add_subbehavior(skills.move.Move(self.r), "point 1")
        self.add_subbehavior(skills.move.Move(self.r3), "point 2")
        self.add_subbehavior(skills.capture.Capture(), "capturing")

        # Send two robots to corners of triangle, and one to 'capture' the ball
        # self.add_subbehavior(skills.move.Move(<POINT>), 'move1')
        # self.add_subbehavior(skills.move.Move(<POINT>), 'move2')
        # self.add_subbehavior(skills.capture.Capture(), 'capture')
        pass

    def on_exit_setup(self):
        # Remove all subbehaviors, so we can add new ones for passing
        self.remove_all_subbehaviors()
    def on_enter_passing(self):
    	self.add_subbehavior(self.pass_bhvr, 'pass')
    	self.pass_bhvr.receive_point = self.r1
    	self.i += 1

    def execute_passing(self):
        # Remember this function is getting called continuously, so we don't want to add subbehaviors
        # if they are already present
        positions = [self.r1, self.r2, self.r3]
        if self.pass_bhvr.State == behavior.Behavior.State.completed:
            print("hi")
            self.remove_all_subbehaviors()
            self.add_subbehavior(self.pass_bhvr, 'pass')
            self.pass_bhvr.receive_point = robocup.Point(positions[i])
            self.i += 1
            if self.i == 3:
            	self.i = 0

        # <Check to see if subbehaviors are done, if they are, remove them, so we can kick again>

        # Don't add subbehaviors if we have added them in the previous loop
        if not self.has_subbehaviors():
            # Add a subbehavior to pass the ball to another robot!
            # self.add_subbehavior(tactics.coordinated_pass.CoordinatedPass(<KICK_TARGET_POINT>), 'pass')
            pass

    def on_exit_passing(self):
        # clean up!
        self.remove_all_subbehaviors()
