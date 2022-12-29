import rospy
import actionlib
from std_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

counter1 =0

flag1=0

def take_the_wheel():

    pub3 = rospy.Publisher("/cmd_vel", Twist, queue=1000)
    robot_speed = Twist()

    global flag1
    global counter1

    vel_linear=0.0
    vel_angular=0.0

    counter2 = 10

    input = 'e'

    while input != 'f':
        # Command list
        if counter2 % 10 == 0:
            print("\n Commands: \n"
                "w - Go on\n"
                "s - Go back\n"
                "q - Curve left\n"
                "e - Curve right\n"
                "a - Turn left\n"
                "d - Turn right\n"
                "-----------------------------\n"
                "r - Increase linear velocity\n"
                "t - Decrease linear velocity\n"
                "y - Increase angular velocity\n"
                "u - Decrease angular velocity\n"
                "-----------------------------\n"
                "i - Emergency stop\n"
                "p - Quit")
            
        if flag3 == 0:
            print("h - Enable driving assistance")
        elif flag3 == 1:
            print("h - Disable driving assistance")
        
        # Take user input
        input = input("\nCommand: ")
        
        rospy.set_param('/print_flag', 0)

        match input:
            case 'w':
                robot_speed.linear.x = vel_linear
                robot_speed.angular.z = 0
                
            case 'q':
                robot_speed.linear.x = vel_linear
                robot_speed.angular.z = vel_angular
                
        
            case 's':  
                robot_speed.linear.x = -vel_linear
                robot_speed.angular.z = 0; 
                
        
            case 'e':  
                robot_speed.linear.x = vel_linear
                robot_speed.angular.z = -vel_angular
                
        
            case 'a':  
                robot_speed.linear.x = 0
                robot_speed.angular.z = vel_angular
                
        
            case 'd':  
                robot_speed.linear.x = 0
                robot_speed.angular.z = -vel_angular
                
        
            case 'r':  
                vel_linear += 0.1
                break
                
            case 't':  
                vel_linear -= 0.1
                break
            case 'y':  
                vel_angular += 0.1
                break
            case 'u':  
                vel_angular -= 0.1
                break
            case 'i':  
                robot_speed.linear.x = 0
                robot_speed.angular.z = 0; 
                break
            case 'o':  
                if flag3 == 0:
                    rospy.set_param('/flag1', 1)
                    flag3 = 1
                elif flag3 == 1:
                    rospy.set_param('/flag1', 0)
                    flag3 = 0
                break
            case 'p':
                robot_speed.linear.x = 0
                robot_speed.angular.z = 0
                pub3.publish(robot_speed)
                counter1 = 10
                break

        print("Linear velocity: %f\n" "Angular velocity: %f\n", vel_linear, vel_angular)
        pub3.publish(robot_speed)
        counter2 += 1

def ui():
    global flag3
    global counter1

    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    client.wait_for_server()
    res = '5'

    flag5 =0
    rospy.setparam('/flag5', flag5)

    while (res != '0'):
                
        if counter1 % 10 == 0:
            print("\nChoose an action:\n"
            "0 - Exit\n"
            "1 - Insert new coordinates to reach\n"
            "2 - Cancel the initial goal\n"
            "3 - Manual driving\n")
            
        if flag3 == 0:
            print("4 - Enable assistance\n")
        elif flag3 == 1:
            print("4 - Disable assistance\n")
        
        
        res = input("Please Enter your choice of Action: ")

        if res != '0' and res != '1' and res != '2' and res != '3' and res != '4':
            print("\nERROR: type '0', '1', '2', '3' or '4'.\n")

        counter1 += 1

        flag5 = rospy.get_param("flag5",)
        
        if res == '0':
            flag2 = 0
            rospy.set_param('/goal_flag', 0)
            client.cancel_goal()
            
        elif res == '1':
            
            print("\nInsert coordinates to reach:\n")
            x = input("x: ")
            y = input("y: ")

            goal_pos =MoveBaseGoal()
            goal_pos.goal.target_pose.header.frame_id = "map"
            goal_pos.goal.target_pose.pose.orientation.w = 1
            
            goal_pos.goal.target_pose.pose.position.x = float(x)
            goal_pos.goal.target_pose.pose.position.y = float(y)
            
            client.send_goal(goal_pos)
            rospy.set_param('/goal_flag',1)
            print("The goal has been sent \n")
            
        
        
        elif res == '2':
            if flag5 ==1:
                rospy.set_param('/flag5',0)
                client.canc_goal()
                flag5 = 0
                print("goal got cancelled \n")
        
        elif res == '3':
            if flag5 ==1:
                rospy.set_param('/flag5',0)
                client.cancel_goal()
            take_the_wheel()

        
        elif res == '4':
            if flag3 == 0:
                rospy.set_param('/flag1',1)
                flag3 = 1
                print("\n assistance enabled.\n")
                
            elif flag3 == 1:
                rospy.set_param('/flag1',0)
                flag3 = 0
                print("\n assistance disabled.\n")

def main():
    print( "*****USER INTERFACE***** \n"
        " TWO WAYS TO CONTROL THE ROBOT \n"
        "1.MANUAL DRIVING  2. AUTOMATIC DRIVING")
    
    rospy.init_node("rt2_robot_interface")
    ui()
    print("\n THE END \n")

if __name__ == "__main__":
    main()
