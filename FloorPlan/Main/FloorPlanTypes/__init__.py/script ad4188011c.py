import bpy
from mathutils import *
import re
import os
D = bpy.data
C = bpy.context

#!!!Make sure you open the folder that contains this for Start Blender to work!!!!

def set_Colums_Points():
    file_path = "C:/Users/zpmas/Building/ColumnValues.txt"
    verts = get_point_data(file_path)
    edges = []
    
    if (type(verts) == "None"):
        return
    # Iterate through vertices to calculate current_x and next_x
    for i in range(len(verts)-1):
        current_x = verts[i][0]  # x-component of current vertex
        next_x = verts[i+1][0]   # x-component of next vertex
        
        # Check if the x-components are the same
        if current_x == next_x:
            # If they are the same, create an edge
            edges.append([i, i+1])

    # Create a new mesh
    mesh = bpy.data.meshes.new("mesh_name")
    
    # Add vertices and edges to the mesh
    mesh.from_pydata(verts, edges, faces=[])
    
    # Update the mesh
    mesh.update()

    # Create a new object using the mesh
    obj = bpy.data.objects.new("obj_name", mesh)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(obj)
    set_row_points()


def get_point_data(file_path):
    verts = []

    with open(file_path, "r") as columnFile:
        f = columnFile.read()
        # Use re.findall to extract tuples from the file content
        tuples = re.findall(r"\((.*?)\)", f, re.MULTILINE)
        # Split each tuple into a list of values and convert them to floats
        verts = [list(map(float, t.split(","))) for t in tuples]
    return verts


def set_row_points():
    file_path = "C:/Users/zpmas/Building/RowValues.txt"
    verts = get_point_data(file_path)
    edges = []
    
    # Iterate through vertices to calculate current_x and next_x
    for i in range(len(verts)-1):
        current_y = verts[i][1]  # y-component of current vertex
        next_y = verts[i+1][1]   # y-component of next vertex
        
        # Check if the x-components are the same
        if current_y == next_y:
            # If they are the same, create an edge
            edges.append([i, i+1])

    # Create a new mesh
    mesh = bpy.data.meshes.new("mesh_name2")
    
    # Add vertices and edges to the mesh
    mesh.from_pydata(verts, edges, faces=[])

    # Update the mesh
    mesh.update()

    # Create a new object using the mesh
    obj = bpy.data.objects.new("obj_name2", mesh)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(obj)
    FlipObjects()


def FlipObjects():
    #bpy.ops.object.select_all(action='DESELECT')
    objects = bpy.context.selectable_objects
    for obj in objects:
        if obj.type == "MESH":
            obj.select_set(True)
        obj.scale = (-1,1,1)
        with bpy.context.temp_override(active_object=obj, selected_objects=objects):
            bpy.ops.object.join()


def check_files_exist():
    file_path = "C:/Users/zpmas/Building/RowValues.txt"
    file_path2 = "C:/Users/zpmas/Building/ColumnValues.txt"
    if(not os.path.isfile(file_path)):
        print(f"!!!!!!File does not exist!!!!! " + file_path )
        return
    if(not os.path.isfile(file_path2)):
        print(f"!!!!!File does not exist!!!!!! " + file_path )
        return
    set_Colums_Points()

check_files_exist()