# - *- coding: utf-8 - *-
# Dependencies
#      pip install pyshp
#
# Description: This script gets all the touch relations (neighboring) stored in
#              the Edges ShapeFile of Tiger Dataset. Each edge in the ShapeFile
#              has two face identifiers: one for the left face (TFIDL) and one
#              for the right face (TFIDR). We use the face identifiers to
#              construct the graph 
#

import sys
import os
import shapefile

def process_edges_shp(directory, out_path):
    out_file = open(out_path, 'w')

    vertices = {}
    num_files = 0
    
    # Extracting vertices from each ShapeFile in the folder
    for filename in os.listdir(directory):

        # Only process files with extension .shp
        if filename.endswith(".shp"):
            num_files += 1

            if num_files%100 == 0:
                print("Processed files:", num_files)

            # Read the ShapeFile
            sf = shapefile.Reader(directory + filename)

            # List of shapes in the ShapeFile
            shapes=sf.shapes()
            num_shapes=len(shapes)

            for i in range(0, num_shapes):
                rec=sf.record(i)

                # Avoid self-loops
                if rec["TFIDL"] == rec["TFIDR"]:
                    continue
                else:
                    if rec["TFIDR"] not in vertices:
                        vertices[rec["TFIDR"]] = []
                    if rec["TFIDL"] not in vertices:
                        vertices[rec["TFIDL"]] = []

                    # Inserting nodes in the adyacency lists of the vertices
                    # TFIDL stands for "Permanent face ID on the left of the edge"
                    # TFIDR stands for "Permanent face ID on the right of the
                    # edge"

                    # Note: We assume the relation is symmetric (no need to
                    # store the complement)
                    vertices[rec["TFIDR"]].append(rec["TFIDL"])
        else:
            continue

    print("Total number of processed files: ", num_files)
        
    total_relations = 0
    for vtx in vertices.values():
        total_edges += len(vtx)

    print("total relations (unique)   :", total_relations)
    print("total elements:", len(vertices))

    # Write the touch relations
    out_file.write("element1;element2\n")
    for src in vertices:
        for tgt in vertices[src]:
            out_file.write(str(src) + ";" + str(tgt) + "\n")

    out_file.close()
    
def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: " + sys.argv[0] + " <Path to .shp files> <output file>\n")
        exit(0)
        
    process_edges_shp(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
