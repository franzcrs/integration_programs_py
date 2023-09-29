import json
import sys
import numpy as np

# Load joint motions information
with open('joint_motions.json', 'r') as json_file:
    joint_motions = json.load(json_file)

# Functions
def begin(motion_name, torque_at_met, area_curve_torque_met):
    # parameters for Newton Method
    init_value = 0.1
    delta = 0.000000001
    max_its = 100
    
    try:
        # get fatigue ratio from dictionary
        λ_F = joint_motions[motion_name]["f_ratio"]
    except KeyError:
        # explain error and return None
        print(f'＞ The provided motion name: "{motion_name}" does not exist in dictionary of motions')
        return None
    
    # Newton method for finding roots
    max_torq_prev = 0
    max_torq = init_value
    for i in np.arange(0, max_its):
        max_torq_prev = max_torq
        # X update: x = x - (f(x)/f'(x))
        max_torq = max_torq - (np.log(torque_at_met/max_torq) + (λ_F*area_curve_torque_met/max_torq))/((-1)*( 1/max_torq + λ_F*area_curve_torque_met/(max_torq*max_torq)))
        # Convergence method: |x - x_prev|/|x_prev| < delta
        if (abs(max_torq - max_torq_prev) / abs(max_torq_prev)) < delta:
            print("＞ Root value converged!")
            print(f"＞ τ_max = {round(max_torq,2)}\n")
            return max_torq
    if (i == max_its):
        print("＞ Root value could not converge in the defined number of iterations\n")
        return None

###################### START OF EXECUTION ######################

if __name__ == "__main__":
    # Variables
    motion_name = ''

    # Receive arguments from terminal
    if len(sys.argv) == 4:
        try:
            # read and convert numeric arguments
            torque_at_met = float(sys.argv[2])
            area_curve_torque_met = float(sys.argv[3])
        except:
            print('Arguments expected to be numeric were of different type')
        motion_name = sys.argv[1]
    else:
        print('Usage:\nFor computing the maximum torque per joint: python max_joint_torque.py joint_name torque_at_met area_curve_torque_met')

    # If argument activity name is provided
    if len(motion_name)>1:
        result = begin(motion_name, torque_at_met, area_curve_torque_met)
        print(result)