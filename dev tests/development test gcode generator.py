from datetime import datetime
import getpass
import numpy as np
import matplotlib.pyplot as plt


num_pushers = 4
first_pusher_x = 119#TODO
pusher_separation = 45#TODO
magnet_separation_radius = 22
num_points_to_interpolate = 20#TODO
center_z = 65.6#TODO

e_per_arc_length = 1#TODO

mag_clearance = 13#mm distance from magnet to magnet that has minable attraction

retract_speed= 2100


retract_distance = 10
z_bottom = center_z - magnet_separation_radius
z_clearance = z_bottom - mag_clearance

def generate_rotation(center_x, num_revolutions, direction, output_file):
    angles = np.linspace(-np.pi/2, 3 * np.pi/2, num_points_to_interpolate + 1)
    if direction == 'load':
        np.flip(angles)

    output_file.write(';start interpolate {} revolutions of a XZ circle with {} points centered at X{} Z{}\n'.format(num_revolutions, num_points_to_interpolate, center_x, center_z))
    for _ in range(num_revolutions):
        for i in range(1,len(angles)):#exclude first point because we are already there
            x = magnet_separation_radius*np.cos(angles[i]) + center_x
            z = magnet_separation_radius*np.sin(angles[i]) + center_z
            #output_file.write('{} {} {}\n'.format(angles[i], x, z))

            output_file.write('G1 X{:.2f} Z{:.2f}\n'.format(x, z))
    output_file.write(';end interpolate {} revolutions of a XZ circle with {} points centered at X{} Z{}\n'.format(num_revolutions, num_points_to_interpolate, center_x, center_z))




# # Create an array of angles from 0 to 2*pi
# angles = np.linspace(0, 2 * np.pi, num_points)

# # Calculate x and y coordinates
# x = radius * np.cos(angles)
# y = radius * np.sin(angles)

num_revolutions_to_unload = 2#TODO
num_revolutions_to_load = 3#TODO


with open('dev test {}.gcode'.format(datetime.now().strftime('%Y-%m-%d %H_%M_%S')), 'w') as output_file:
    output_file.write(';Dev test generated on {} by {};\n;\n;\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), getpass.getuser()))
    output_file.write(';\n;from prusa default startup\n')
    output_file.write('M862.3 P "MINI" ; printer model check\n')
    output_file.write('G90 ; use absolute coordinates\n')
    output_file.write('M83 ; extruder relative mode\n')
    output_file.write('M204 T1250 ; set travel acceleration\n')
    output_file.write('G28 ; home all without mesh bed level\n')
    #output_file.write('G29 ; mesh bed leveling\n')
    #output_file.write('M204 T2500 ; restore travel acceleration\n')
    output_file.write(';end prusa default startup\n;\n')              
    x_center = first_pusher_x
    output_file.write('G1 X{:.2f} F500;go to center\n'.format(x_center))
    output_file.write('G1 Z{:.2f};engage with pusher\n'.format(z_bottom))
    generate_rotation(x_center, 1, 'unload', output_file)
    output_file.write('G1 Z{:.2f};go back down to clearance z\n'.format(z_clearance))
