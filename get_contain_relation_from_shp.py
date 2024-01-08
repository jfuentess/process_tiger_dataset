# - *- coding: utf-8 - *-
# Dependencies
#      pip install pyshp
#
# Description: This script gets all the contain/subsumption relations stored in
#              the Faces ShapeFile of Tiger Dataset.
#
#
# Note: We are using the following containment hierarchy
#
#   State (STATEFP)
#     |
#   County (COUNTYFP)
#     |
#   Census tract (TRACTCE)
#     |
#   Block group (BLKGRPCE)
#     |
#   Census block (BLOCKCE10)
#     |
#   Face (TFID)
#     

import shapefile
import sys
import os
import pickle

def read_faces_shp(directory):

    lim = 0
    # Dictionaries to store containment between consecutive levels of the hierarchy
    county_state = {} # county is the key and state the value
    tract_county= {} # tract is the key and county the value
    blockgroup_tract = {} # block group is the key and tract the value
    block_blockgroup = {} # block is the key and block group the value
    face_block = {} # face is the key and block the value

    # Extracting vertices
    for filename in os.listdir(directory):
        if filename.endswith(".shp"):    
            lim += 1
            if lim % 100 == 1:
                print("Processed files:", lim)

            sf = shapefile.Reader(directory + filename)
  
            shapes=sf.shapes()
            num_shapes=len(shapes)
    
            for i in range(0, num_shapes):
                rec=sf.record(i)

                face_id = rec["TFID"]
                state_id = rec["STATEFP"]
                county_id = rec["STATEFP"] + rec["COUNTYFP"]
                tract_id = rec["STATEFP"] + rec["COUNTYFP"] + rec["TRACTCE"]
                blockgroup_id = rec["STATEFP"] + rec["COUNTYFP"] + rec["TRACTCE"] + rec["BLKGRPCE"]
                block_id = rec["STATEFP"] + rec["COUNTYFP"] + rec["TRACTCE"] + rec["BLKGRPCE"] + rec["BLOCKCE10"]

                if face_id not in face_block:
                    face_block[face_id] = block_id;
                if block_id not in block_blockgroup:
                    block_blockgroup[block_id] = blockgroup_id;
                if blockgroup_id not in blockgroup_tract:
                    blockgroup_tract[blockgroup_id] = tract_id;
                if tract_id not in tract_county:
                    tract_county[tract_id] = county_id;
                if county_id not in county_state:
                    county_state[county_id] = state_id;

        else:
            continue

    print("Total number of processed files: ", lim)

    # Write the contain relations
    out_file.write("element1;element2\n")

    for key, value in county_state.items():
        out_file.write(str(key) + ";" + str(value) + "\n")

    for key, value in tract_county.items():
        out_file.write(str(key) + ";" + str(value) + "\n")

    for key, value in blockgroup_tract.items():
        out_file.write(str(key) + ";" + str(value) + "\n")

    for key, value in block_blockgroup.items():
        out_file.write(str(key) + ";" + str(value) + "\n")

    for key, value in face_block.items():
        out_file.write(str(key) + ";" + str(value) + "\n")
        
    out_file.close()
    
        
def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <Pah to *_faces.shp files>\n")
        exit(0)
        
    read_faces_shp(sys.argv[1])


if __name__ == '__main__':
    main()
