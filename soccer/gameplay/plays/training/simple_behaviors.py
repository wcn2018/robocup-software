import skills
import tactics
import play
import behavior
import skills.pivot_kick
import skills.move
import constants
import robocup


# This is a file where you can learn how skills work!
class SimpleBehaviors(play.Play):

    def __init__(self):
        super().__init__(continuous=True)

        # To make a robot move, use skills.move.Move(<point to move to>)
        # To create a point, we initialize a point using 
        # robocup.Point(<x coordinate>, <y coordinate>)
        
        # These lines moves a robot to the point (0, 0)
        #point1 = robocup.Point(3,0)
        #point2 = robocup.Point(3,9)
        #point3 = robocup.Point(-3,9)
        #point4 = robocup.Point(-3,0)
        #skill1 = skills.move.Move(point1)
        #skill2 = skills.move.Move(point2)
        #skill3 = skills.move.Move(point3)
        #skill4 = skills.move.Move(point4)
        #move_point = robocup.Point(2, constants.Field.Length/
        self.add_transition(behavior.Behavior.State.start,
                            behavior.Behavior.State.running, lambda: True,
                            'immediately')
        
        line_kick_skill = skills.line_kick.LineKick()
        line_kick_skill.target = constants.Field.OurGoalSegment
        self.add_subbehavior(line_kick_skill, "line_kick_skill")



        # Adds behavior to our behavior tree, we will explain this more later
    def execeute_line_kick_repeat(self):
            line_kick_skill = self.subbehavior_with_name(line_kick)
            if line_kick_skill.is_done_running():
                line_kick_skill.restart()





        #github.come/robocjacetks,==m====================