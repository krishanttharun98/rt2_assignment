---
# Research Track 2 - Jupyter Notebook Assignment 

-  This Assignment is to based on a control of a robot using Jupyter Notebook
-  This assignment is referenced from the previous Research track 1 third assignment [rt 1 third assignment](https://github.com/krishanttharun98/Research-track--1-thrid-assignment.git)
---
## How does it work
-  Few files are already from the RT-1 3rd assignment and by separating the modalities from a single code to three different separate codes, we have  
    
1. rt2_assignment2.py
2. rt2_robot_cpp.cpp
3. rt2_jupyter_interface.ipynb


The rt2_Assignment2.py, in this code we have the modalities in which the robot can be operated as per the request of the user from two modalities like manually driving ( take_the_wheel() function ), and another one is like automatic driving such as inserting a goal coordinates for the robot to move ( ui() function ).

The rt2_robot_cpp.cpp code it simulated only the generic logic of how the robot should move to a given goal or location. Three publishers and subscribers are used to for updating the goal position, its coordinates through a laser scanner data which helps the robot to stop if there is a wall in its path. 

The rt2_jupyter_interface.ipynb, for this code we use the jupyter notebook to plot the functionalities and position of the robot, laser scanner data and visualize the data. 

---
## How to run the code 

Step 1 : Open the terminal and go to src of your ROS workspace and run -

<pre><code>git clone https://github.com/krishanttharun98/rt2_assignment.git</code></pre>

Step 2 : Now to build your clonned code run the command -

<pre><code>catkin_make</code></pre>

step 3 : Open a each new terminal for the following commands seperately -
 
Terminal-1. 

<pre><code>roslaunch rt2_assignment simulation_gmapping.launch</code></pre>

Terminal-2.

<pre><code>roslaunch rt2_assignment move_base.launch</code></pre>

Terminal-3.

<pre><code>rosrun rt2_assignment rt2_robot</code></pre>

Terminal-4.

<pre><code>rosrun rt2_assignment rt2_assignment2.py</code></pre>

To start the jupyter run this in a seperate terminal 

<pre><code>jupyter notebook --allow-root --ip 0.0.0.0</code></pre>

After running this in terminal we can able to access the rt2_jupyter_interface.ipynb file which consists of plotting modalities. 


