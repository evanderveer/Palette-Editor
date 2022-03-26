import argparse
import numpy as np
import colormath 
import colormath.color_objects 
import colormath.color_conversions
from ast import literal_eval




def build__pal_header(file, file_size):
    file.write(bytes('RIFF', encoding='ascii'))
    file.write((file_size-8).to_bytes(4, byteorder='little'))
    file.write(bytes('PAL data', encoding='ascii'))
    file.write((file_size-20).to_bytes(4, byteorder='little'))
    file.write((0).to_bytes(1, byteorder='little'))
    file.write((3).to_bytes(1, byteorder='little'))
    file.write((int((file_size-24)/4)).to_bytes(2, byteorder='little'))
    pass
    
def write_color_list(file, color_list):
    for color in color_list:
    
        #Clip the colors to 255 if they fall outside of the RGB color space
        red = int(round(color.rgb_r*255)).to_bytes(1, 'little') if int(round(color.rgb_r*255))<256 else (255).to_bytes(1, 'little')
        green = int(round(color.rgb_g*255)).to_bytes(1, 'little') if int(round(color.rgb_g*255))<256 else (255).to_bytes(1, 'little')
        blue = int(round(color.rgb_b*255)).to_bytes(1, 'little') if int(round(color.rgb_b*255))<256 else (255).to_bytes(1, 'little')

        bytestring = red + green + blue + (255).to_bytes(1, 'little')
        file.write(bytestring)

def interpolate(x_points, x_data, y_data):
    interp_points = np.interp(x_points, x_data, y_data)
    return(interp_points)
   
def parse_args():
    parser = argparse.ArgumentParser(description='Creates Microsoft color palette files (.pal).')
    parser.add_argument('palette_file', help='Palette file name to generate.')
    parser.add_argument('--start_color', default='#000000', help='Starting color for a gradient. Must be supplied as a hex value.')
    parser.add_argument('--end_color', default='#FFFFFF', help='End color for a gradient. Must be supplied as a hex value.')
    parser.add_argument('--color_points', help='List of points to include in a color gradient. Must be supplied as a string of the form ((<point 1>,<color 1>),(<point 2>,<color 2>),...) with <point n> between 0 and 1 and <color n> being a hex value. Overrides any --start_color and --end_color specification.')
    parser.add_argument('--gradient_steps', type=int, default=256, help='Number of steps in each gradient segment. Defaults to 256.')
    parser.add_argument('--interpolation_function', default='linear', help='Interpolation function to use. Defaults to \'linear\'. Other functions are not yet available.')
    parser.add_argument('--color_space', default='lab', choices=['lab', 'rgb', 'hsv', 'hsl'], help='Color space in which to perform the interpolation. Defaults to \'lab\'. This feature is not implemented yet.')
    args = parser.parse_args()
    return(args)
   
def mainfunction(args):
    # Construct the list of colors defining the gradient
    if(args.color_points == None):
        args.color_points = f'((0, \'{args.start_color}\'), (1, \'{args.end_color}\'))'
    color_list = literal_eval(args.color_points)
    file_size = args.gradient_steps * 4 + 24 
    color_points = []
    
    # Create LAB color objects
    for color in color_list:
        rgbcolor = colormath.color_objects.sRGBColor.new_from_rgb_hex(color[1])
        labcolor = colormath.color_conversions.convert_color(rgbcolor, colormath.color_objects.LabColor)
        color_points.append((color[0], labcolor))
    
    #Create the gradient by interpolating between the colors
    interp_positions = np.linspace(0, 1, args.gradient_steps)
    color_points_exp = [[color[0],color[1].lab_l,color[1].lab_a,color[1].lab_b] for color in color_points]
    pos_lab = np.transpose(color_points_exp)
    
    interp_lab = np.transpose([interp_positions,
                               interpolate(interp_positions, pos_lab[0], pos_lab[1]),
                               interpolate(interp_positions, pos_lab[0], pos_lab[2]),
                               interpolate(interp_positions, pos_lab[0], pos_lab[3])])
    
    final_color_list = [colormath.color_conversions.convert_color(colormath.color_objects.LabColor(*color[1:]), colormath.color_objects.sRGBColor) for color in interp_lab]
    
    #Write the .pal file
    with open(args.palette_file, 'wb') as f:
        build_pal_header(f, file_size)
        write_color_list(f, final_color_list)
    
if __name__ == '__main__':
    
    args = parse_args()
    mainfunction(args)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    