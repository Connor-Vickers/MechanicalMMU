from datetime import datetime
import getpass
import numpy as np
import matplotlib.pyplot as plt


num_pushers = 4
first_pusher_x = 0#TODO
pusher_separation = 45
magnet_separation_radius = 15
num_points_to_interpolate = 20#TODO
center_z = 0#TODO
#test_extruder_length = 100#TODO
test_pusher_length_per_revolution = 10#mm#TODO
max_feed_rate_z = 12#mm/s
max_feed_rate_x = 180#mm/s
max_feed_rate_e = 80#mm/s

e_per_arc_length = 1#TODO

mag_clearance = 10#mm distance from magnet to magnet that has minable attraction

retract_speed= 2100


retract_distance = 10
z_bottom = center_z - magnet_separation_radius
z_clearance = z_bottom - mag_clearance

def generate_rotation(center_x, num_revolutions, direction, output_file):
    angles = np.linspace(0, 2 * np.pi, num_points_to_interpolate + 1)
    if direction == 'load':
        np.flip(angles)

    output_file.write(';start interpolate {} revolutions of a XZ circle with {} points centered at X{} Z{}\n'.format(num_revolutions, num_points_to_interpolate, center_x, center_z))
    for _ in range(num_revolutions):
        for i in range(1,len(angles)):#exclude first point because we are already there
            #output_file.write(str(len(angles))+ '\n\n')
            prev_x = magnet_separation_radius*np.cos(angles[i-1]) + center_x
            prev_z = magnet_separation_radius*np.sin(angles[i-1]) + center_z        
            
            x = magnet_separation_radius*np.cos(angles[i]) + center_x
            z = magnet_separation_radius*np.sin(angles[i]) + center_z

            d_x = np.abs(x-prev_x)
            d_z = np.abs(z-prev_z)

            physical_dist = np.sqrt(np.power(d_x, 2)+ np.power(d_z, 2))
            e = physical_dist*e_per_arc_length
            output_file.write('G1 X{0:.2f} Z{0:.2f} E{0:.2f}\n'.format(x, z, e))
    output_file.write(';end interpolate {} revolutions of a XZ circle with {} points centered at X{} Z{}\n'.format(num_revolutions, num_points_to_interpolate, center_x, center_z))




# # Create an array of angles from 0 to 2*pi
# angles = np.linspace(0, 2 * np.pi, num_points)

# # Calculate x and y coordinates
# x = radius * np.cos(angles)
# y = radius * np.sin(angles)

num_revolutions_to_unload = 2#TODO
num_revolutions_to_load = 3#TODO


with open('custom gcode.txt', 'w') as output_file:
    output_file.write(';Paste the following into Prusa Slicer under Printers->Custom G-code tool change G-code\n')
    output_file.write(';Mechanical MMU Generated on {} by {};\n;\n;\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), getpass.getuser()))
    output_file.write('{if previous_extruder != -1};exclude initial tool change\n;\n')
    output_file.write('G1 E-1 Z{toolchange_z+' + str(retract_distance) + '} F' + str(retract_speed) + ';go up and retract a little\n;\n')
    
    output_file.write(';start load next pusher\n;\n')
    for pusher_number in range(1, num_pushers+1): # pusher number starts at 1 so aligns with prusa slicer
        output_file.write('{if previous_extruder == ' + str(pusher_number) + '};if pusher ' + str(pusher_number) + ' needs unloaded\n')
        x_center = first_pusher_x + pusher_separation * (pusher_number - 1)
        output_file.write('G1 X{};go to center\n'.format(x_center))
        output_file.write('G1 Z{};engage with pusher\n'.format(z_bottom))
        generate_rotation(x_center, num_revolutions_to_unload, 'unload', output_file)
        output_file.write('{endif};endif unload ' + str(pusher_number) + ' pusher\n')
    output_file.write(';end unload previous pusher')
    output_file.write('G1 Z{};go back down to clearance z\n'.format(z_clearance))

    output_file.write(';\n;start load next pusher\n;\n')
    for pusher_number in range(1, num_pushers+1): # pusher number starts at 1 so aligns with prusa slicer
        output_file.write('{if next_extruder == ' + str(pusher_number) + '};if pusher ' + str(pusher_number) + ' needs loaded\n')
        x_center = first_pusher_x + pusher_separation * (pusher_number - 1)
        output_file.write('G1 X{};go x center for pusher {}\n'.format(x_center, pusher_number))
        output_file.write('G1 Z{};engage with pusher\n'.format(z_bottom)) 
        generate_rotation(x_center, num_revolutions_to_load, 'load', output_file)
        output_file.write('{endif};endif load ' + str(pusher_number) + ' pusher\n')
    output_file.write(';end load next pusher\n')
    output_file.write('G1 Z{toolchange_z};go back down to layer and resume\n')
    output_file.write('{endif};endif exclude initial tool change\n')
    
    #TODO safety check in Z M0; error out otherwise we'll crash"
