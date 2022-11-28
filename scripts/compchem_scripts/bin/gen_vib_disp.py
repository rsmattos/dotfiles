#! /usr/bin/env python3

import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='''\
Script to extrat displacements from the normal modes of vibration and generate displaced geometries. \n \
''')
parser.add_argument('input',help="File to be read which contains the normal modes.",type=str,nargs='*',default='.')
parser.add_argument('-t','--type',help="Specify the filetype being read.",type=str,nargs='?',default='molden')
parser.add_argument('-m','--modes',help="The vibrational modes of interest.",type=str,nargs='*')
parser.add_argument('-l','--lambdas',help="The intensity of displacements.",type=float,nargs='*')
args=parser.parse_args()

def read_molden(input, modes):
    # DataFrame for the coordinates
    coords = {}

    lines=open(input,"r").readlines()

    # read equilibrium geometry
    for line in range(len(lines)):
        if "[GTO]" in lines[line]:
            m_size = int(lines[line-1].split()[1])
            break

    for line in reversed(range(len(lines))):
        if "[FR-COORD]" in lines[line]:
            mode_coord=[]
            for i in range(m_size):
                mode_coord.append([lines[line+i+1].split()[0],
                            float(lines[line+i+1].split()[1]),
                            float(lines[line+i+1].split()[2]),
                            float(lines[line+i+1].split()[3])])

            tmp_df=pd.DataFrame(mode_coord,columns=['A','x','y','z'])
            tmp_df['x']=tmp_df['x']*0.529177
            tmp_df['y']=tmp_df['y']*0.529177
            tmp_df['z']=tmp_df['z']*0.529177

            coords['0'] = tmp_df

            current_line = line + i

            break
        
    # read displacements
    for line in range(current_line,len(lines)):
        if "vibration" in lines[line] and lines[line].split()[1] in modes:
            mode_coord=[]
            for i in range(m_size):
                mode_coord.append([float(lines[line+i+1].split()[0]),
                                   float(lines[line+i+1].split()[1]),
                                   float(lines[line+i+1].split()[2])])

            coords[lines[line].split()[1]] = pd.DataFrame(mode_coord,columns=['x','y','z'])*0.529177
            line = line + i
        
        else:
            line = line + m_size

    return coords

def generate_geometries(coords, modes, lambdas):
    for m in modes:
        for l in lambdas:
            print_coord = pd.DataFrame()
            print_coord['A'] = coords['0']['A']
            print_coord['x'] = coords['0']['x']+l*coords[m]['x']
            print_coord['y'] = coords['0']['y']+l*coords[m]['y']
            print_coord['z'] = coords['0']['z']+l*coords[m]['z']

            out_name = "mode_"+m+"_lambda_"+str(l)+".xyz"
            f = open(out_name, "w")
            f.write(str(len(coords[m]))+'\n')
            f.write("lambda "+str(l)+'\n')
            f.write(print_coord.to_string(header=False,index=False))
            f.write('\n')
            f.close()

###################      MAIN     ###################
if __name__=='__main__':
    if args.type == "molden":
        coords = read_molden(args.input[0],args.modes)

    generate_geometries(coords, args.modes, args.lambdas)