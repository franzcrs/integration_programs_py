import json
import sys
import numpy as np

# # Load joint motions information
# with open('joint_motions.json', 'r') as json_file:
#     joint_motions = json.load(json_file)

# # Load joint motions information
# with open('moment_arms.json', 'r') as json_file:
#     moment_arms = json.load(json_file)

# Functions
def begin(muscles_mvc, forces_at_met, area_curve_force_met):

    muscles_f_ratio = []
    # try:
    # calculate λ_F per muscle
    for i,(mvc,force_at_met,area_curve) in enumerate(zip(muscles_mvc, forces_at_met, area_curve_force_met)):
        # verification of consistency
        if force_at_met>=mvc:
            print(f'The provided force(met): {force_at_met} and MVC: {mvc}, for the muscle of index {i} does not comply with the condition: force(met)<MVC')
            return None
        muscles_f_ratio.append((-1)*np.log(force_at_met/mvc)*mvc/area_curve)
    # except KeyError:
    #     # explain error and return None
    #     print(f'＞ The provided lists does not have the same lenght')
    #     return None
    return muscles_f_ratio

###################### START OF EXECUTION ######################

if __name__ == "__main__":
    print('Usage:\nFor computing the fatigue ratio for each muscle of the joint motion:\n　import muscles_f_ratio\n　muscles_f_ratio.begin(muscles_mvc, forces_at_met, area_curve_force_met)\nin a python script. All the arguments are lists of the same lenght')