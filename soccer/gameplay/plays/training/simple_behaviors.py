import robocup
import constants
import play
import skills
import tactics

# This is a file where you can learn how skills work!
class SimpleBehaviors(play.Play):

    def __init__(self):
        super().__init__(continuous=True)

        # To make a robot move, use skills.move.Move(<point to move to>)
        # To create a point, we initialize a point using 
        # robocup.Point(<x coordinate>, <y coordinate>)
        
        # These lines moves a robot to the point (0, 0)
        point1 = robocup.Point(3,0)
        point2 = robocup.Point(3,9)
        point3 = robocup.Point(-3,9)
        point4 = robocup.Point(-3,0)
        skill1 = skills.move.Move(point1)
        skill2 = skills.move.Move(point2)
        skill3 = skills.move.Move(point3)
        skill4 = skills.move.Move(point3)


        # Adds behavior to our behavior tree, we will explain this more later
        self.add_subbehavior(skill1, "skill")
        self.add_subbehavior(skill2, "skill")
        self.add_subbehavior(skill3, "skill")
        self.add_subbehavior(skill4, "skill")




        #github.come/robocjacetks,==m====================