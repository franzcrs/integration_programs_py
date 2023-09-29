import json
import max_joint_torque
import muscles_mvc
import muscles_f_ratio

# Variables
motion_name = "elbow_flexion" # Motion performed isometrically for calibration. Add any new motion_name to the joint_motions.json file
torque_at_met = 20 # Replace with true value of joint torque at Maximum Endurance Time(MET) obtained from inverse dynamics
area_curve_torque_met = 700 # Replace with true area under the curve of the joint torque from t=0 until MET obtained from inverse dynamics
forces_at_met_dict = { # Replace with true capture of all muscles forces at MET obtained from model simulations
                "BICLong": 200,
                "BICShort": 100,
                "BRA": 400,
                "BRD": 100,
                "TRILong": 0,
                "TRILat": 0,
                "TRIMed": 0
                }
area_curve_force_met_dict = { # Replace with true calculations area under the curve of muscles forces from t=0 until MET obtained from model simulations
                        "BICLong": 1800,
                        "BICShort": 1200,
                        "BRA": 3600,
                        "BRD": 1200,
                        "TRILong": 0,
                        "TRILat": 0,
                        "TRIMed": 0
                        }

# Load joint motions information
with open('joint_motions.json', 'r') as json_file:
    joint_motions = json.load(json_file)

# Calculating the maximum joint torque
max_joint_torq = max_joint_torque.begin(motion_name, torque_at_met, area_curve_torque_met)
# Distributing the MVC among the participants muscles
muscles_mvc_list = muscles_mvc.begin(motion_name, max_joint_torq)

# Preparing lists of forces at met and area under the curve of forces of participants muscles
forces_at_met = []
try:
    # generate list of forces of participant muscles at met
    for muscle in joint_motions[motion_name]["muscles"]:
        forces_at_met.append(forces_at_met_dict[muscle])
except KeyError:
    # explain error
    print(f'＞ The muscle: "{muscle}" does not exist in dictionary of forces at met')
area_curve_force_met = []
try:
    # generate list of area under the curve of forces of participants muscles
    for muscle in joint_motions[motion_name]["muscles"]:
        area_curve_force_met.append(area_curve_force_met_dict[muscle])
except KeyError:
    # explain error
    print(f'＞ The muscle: "{muscle}" does not exist in dictionary of area under the curve of forces')

# Calculating the fatigue ratio per participant muscle
print(muscles_mvc_list)
print(forces_at_met)
print(area_curve_force_met)
muscles_f_ratio_list = muscles_f_ratio.begin(muscles_mvc_list, forces_at_met, area_curve_force_met)

print("Results")
print(f'participant muscles: {joint_motions[motion_name]["muscles"]}')
print(f'max_joint_torq: {max_joint_torq}')
print(f'muscles_mvc_list: {muscles_mvc_list}')
print(f'muscles_f_ratio_list: {muscles_f_ratio_list}')

# TODO: store the values of MVC and fatigue ratio (λ_F) in a JSON file
# TODO: read the muscles individual characteristics and draw the muscle capacity curves