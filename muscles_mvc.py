import json
import sys
import numpy as np

# Load joint motions information
with open('joint_motions.json', 'r') as json_file:
    joint_motions = json.load(json_file)

# Load moment arms during isometric exercise
with open('moment_arms.json', 'r') as json_file:
    moment_arms = json.load(json_file)

# Functions
def begin(motion_name, max_joint_torq):
    ## Preguntas: cual es el torque de inverse dynamics
    ## Cual es la representación de brazo de palanca que calcula el model de Azhar

    ## Program asuming that the joint torque is the torque only from the muscles
    try:
        # get list of muscles participants
        muscles = joint_motions[motion_name]["muscles"]
        # get list of maximum force proportion
        proportions = joint_motions[motion_name]["proportion"]
    except KeyError:
        # explain error and return None
        print(f'＞ The provided motion name: "{motion_name}" does not exist in dictionary of motions')
        return None

    muscles_mvc = []
    try:
        # sum of proportion times muscle arm
        sum_prop_arm = 0
        for i, muscle in enumerate(muscles):
            sum_prop_arm = sum_prop_arm + proportions[i]*moment_arms[muscle]
    except KeyError:
        # explain error and return None
        print(f'＞ The provided muscle name: "{muscle}" does not exist in dictionary of moment arms')
        return None
    
    # solve the reference muscle's MVC (geometric proportion is 1)
    ref_muscle_mvc = max_joint_torq/sum_prop_arm

    # solve the rest of muscles_MVC
    for proportion in proportions:
        muscles_mvc.append(ref_muscle_mvc*proportion)
    return muscles_mvc

###################### START OF EXECUTION ######################

if __name__ == "__main__":
    # Variables
    motion_name = ''

    # Receive arguments from terminal
    if len(sys.argv) == 3:
        try:
            # read and convert numeric arguments
            max_joint_torq = float(sys.argv[2])
        except:
            print('Arguments expected to be numeric were of different type')
        motion_name = sys.argv[1]
    else:
        print('Usage:\nFor computing the distribution of MVC among muscles of a motion: python muscles_mvc.py motion_name max_joint_torque')

    # If argument activity name is provided
    if len(motion_name)>1:
        result = begin(motion_name, max_joint_torq)
        print(result)