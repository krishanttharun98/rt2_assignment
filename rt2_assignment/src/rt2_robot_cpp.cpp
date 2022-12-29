#include <iostream>
#include <string>
#include <chrono>
#include <ctime>
#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/LaserScan.h"
#include "actionlib_msgs/GoalID.h"
#include "move_base_msgs/MoveBaseActionGoal.h"
#include "move_base_msgs/MoveBaseActionFeedback.h"

ros::Publisher pub2;
ros::Publisher pub3;
float x_co_ord; 
float y_co_ord;

std::string id = ""; 
std::chrono::high_resolution_clock::time_point t_start;  
std::chrono::high_resolution_clock::time_point t_end;

#define DIST 0.30 
#define POS_ERROR 0.5 
#define MAX_TIME 100000000

void assistance(const sensor_msgs::LaserScan::ConstPtr& msg)
{
    
    geometry_msgs::Twist robot_speed;
    float left = 35.0;
    float center = 35.0;
    float right = 35.0;
    int i;
    int flag1;
    int flag4;
    int flag5;
    int flag6;

    /*std::time_t t = std::time(0); 
    #std::tm* time_info = std::localtime(&t);*/

    if (ros::param::has("/flag6")) {
        ros::param::get("/flag6", flag6);
    }
    if (ros::param::has("/flag1")) {
        ros::param::get("/flag1", flag1);
    }
    if (ros::param::has("/flag5")) {
        ros::param::get("/flag5", flag5);
    }
    if (ros::param::has("/flag4")) {
        ros::param::get("/flag4", flag4);
    }

    for (i = 0; i < 360; i++)
    { 
        if (msg->ranges[i] < right)
            right = msg->ranges[i];
    }
    for (i = 300; i < 420; i++)
    { 
        if (msg->ranges[i] < center)
            center = msg->ranges[i];
    }
    for (i = 360; i < 720; i++)
    { 
        if (msg->ranges[i] < left)
            left = msg->ranges[i];
    }
    
    if (flag1== 1 & ((center < DIST && input == 'w') || (left < DIST && input == 'q') || (right < DIST && input == 'e'))) {
        if (flag4 == 0)
        {
            printf("\nALERT! - Wall approached\n");
            ros::param::set("/flag4",1);
        }
        robot_speed.linear.x = 0;
        robot_speed.angular.z = 0;
        pub3.publish(robot_speed);
    }
    if (flag2 == 1)
    {
        t_end = std::chrono::high_resolution_clock::now();
        auto time = std::chrono::duration_cast<std::chrono::microseconds>(t_end - t_start).count();
        if (time > MAX_TIME)
        {
            actionlib_msgs::GoalID canc_goal;
            printf("\nCannot reach goal!\n");
            canc_goal.id = id;
            pub2.publish(canc_goal);
            printf("Goal cancelled.\n");
            ros::param::set("/flag5",0);
        }
        else if (flag5 == 0)
        {
            actionlib_msgs::GoalID canc_goal;
            canc_goal.id = id;
            pub_canc.publish(canc_goal);
        }   
    }
}

void initial_position(const move_base_msgs::MoveBaseActionFeedback::ConstPtr& msg)
{
    int flag5;
    float diff_x;
    float diff_y;
    float initial_x = msg->feedback.base_position.pose.position.x;
    float initial_y = msg->feedback.base_position.pose.position.y;

    if (ros::param::has("/flag5"))
    {
        ros::param::get("/flag5", flag5);
    }
    if (initial_x >= x_co_ord)
        diff_x = initial_x - x_co_ord;
    else 
        diff_x = x_co_ord - initial_x;
    if (initial_y >= y_co_ord)
        diff_y = initial_y - y_co_ord;
    else 
        diff_y = y_co_ord - initial_y;

    if (diff_x <= POS_ERROR && diff_y <= POS_ERROR)
    {
        if(flag5 == 1)
        {
            printf("Goal has been reached \n");
        }
        ros::param:set("/flag5", 0);
    }

    if (id != msg->status.goal_id.id)
    {
        printf("New goal is registered \n");
        ros::param:set("/flag5", 1);
        id = msg->status.goal_id.id;
        t_start = std::chrono::high_resolution_clock::now();
    }
}

void initial_goal(const move_base_msgs::MoveBaseActionGoal::ConstPtr& msg)
{
    x_co_ord = msg->goal.target_pose.pose.position.x;
    y_co_ord = msg->goal.target_pose.pose.position.y;
}

int main(int argc, char **argv)
{
    
    ros::init(argc, argv, "rt2_robot");
    ros::NodeHandle nh;
    
    t_start = std::chrono::high_resolution_clock::now();

    pub2 = nh.advertise<actionlib_msgs::GoalID>("move_base/cancel", 1000);
    pub3 = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 1000);
    
    
    ros::Subscriber sub_pos = nh.subscribe("/move_base/feedback", 1000, initial_position); 
    ros::Subscriber sub_goal = nh.subscribe("/move_base/goal", 1000, initial_goal); 
    ros::Subscriber sub_laser = nh.subscribe("/scan", 1000, assistance); 

    
    ros::AsyncSpinner spinner(3);
    spinner.start();
    char quit;
    printf("To quit press any key\n");
    std::cin>>quit;
    printf("***THANK YOU SEE YOU***");
    spinner.stop();
    ros::shutdown();
    ros::waitForShutdown();

    return 0;
}


