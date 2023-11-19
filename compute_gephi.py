import os
import math
import math_taxonomy as mt

def calculate_radius_for_spacing(num_points, individual_radius,separation_factor=1.5):
    """
    Calculate the radius of a circle needed to place a given number of points
    evenly spaced along its circumference, considering the size of each point.
    """
    # Each point occupies a space equal to its diameter along the circle's circumference
    total_space_needed = num_points * separation_factor * individual_radius
    # Calculate the radius needed to fit this total space on the circle's circumference
    return total_space_needed / (2 * math.pi)

def generate_coordinates(topics_and_subtopics, individual_radius_main_topics, individual_radius_subtopics,separation_main_topics,separation_sub_topics):
    num_main_topics = len(topics_and_subtopics.keys())
    radius_main_topics = calculate_radius_for_spacing(num_main_topics, individual_radius_main_topics,separation_main_topics)
    radius_subtopics = calculate_radius_for_spacing(sum([len(subtopics) for subtopics in topics_and_subtopics.values()]), individual_radius_subtopics,separation_sub_topics)

    # Adjust the starting angle to place 'Arithmetic' just below the x-axis in the 3rd quadrant
    start_angle_main_topics = math.pi  # 180 degrees, pointing left

    main_topic_coordinates = []
    for i in range(num_main_topics):
        angle = start_angle_main_topics - 2 * math.pi * i / num_main_topics
        x = radius_main_topics * math.cos(angle)
        y = radius_main_topics * math.sin(angle)
        main_topic_coordinates.append((x, y))

    # Subtopic coordinates - also counterclockwise
    subtopic_coordinates = []
    angle_step_subtopics = 2 * math.pi / sum([len(subtopics) for subtopics in topics_and_subtopics.values()])
    current_angle = start_angle_main_topics - angle_step_subtopics  # Start just after 'Arithmetic'

    for _, subtopics in topics_and_subtopics.items():
        for _ in subtopics:
            x = radius_subtopics * math.cos(current_angle)
            y = radius_subtopics * math.sin(current_angle)
            subtopic_coordinates.append((x, y))
            current_angle -= angle_step_subtopics  # Move counterclockwise

    return main_topic_coordinates, subtopic_coordinates

def find_radial_angle_of_subtopic(main_topic_coords, topics_and_subtopics, main_topic_name):
    """
    Find the radial angle of a subtopic based on its alignment with the main topic.

    :param main_topic_coords: Coordinates of main topics.
    :param topics_and_subtopics: Dictionary of main topics and their subtopics.
    :param main_topic_name: The name of the main topic.
    :param subtopic_name: The name of the subtopic to find the radial angle for.
    :return: Radial angle of the subtopic.
    """
    # Find the index of the main topic
    main_topic_index = list(topics_and_subtopics.keys()).index(main_topic_name)

    # Get the coordinates of the main topic
    x, y = main_topic_coords[main_topic_index]

    # Calculate the radial angle
    angle = math.atan2(y, x)
    return angle

def generate_subsub_topic_coordinates(subsub_topics, individual_radius_subsub_topics, separation_subsub_topics,sub_topic_radial_angle):
    num_subsub_topics = sum([len(subsub_list) for subsub_list in subsub_topics.values()])
    radius_subsub_topics = calculate_radius_for_spacing(num_subsub_topics, individual_radius_subsub_topics, separation_subsub_topics)

    # Starting angle for 'Addition' aligned with 'Basic Operations'
    start_angle_subsub_topics = sub_topic_radial_angle

    subsub_topic_coordinates = []
    angle_step_subsub_topics = 2 * math.pi / num_subsub_topics
    current_angle = start_angle_subsub_topics

    for _, subsub_list in subsub_topics.items():
        for _ in subsub_list:
            x = radius_subsub_topics * math.cos(current_angle)
            y = radius_subsub_topics * math.sin(current_angle)
            subsub_topic_coordinates.append((x, y))
            current_angle -= angle_step_subsub_topics  # Move counterclockwise

    return subsub_topic_coordinates

import math

def generate_subsubsub_topic_coordinates(start_angle, subsubsub_topics, individual_radius):
    """
    Generate coordinates for subsubsub topics, starting from a given angle and using individual radius.

    :param start_angle: Starting radial angle in radians.
    :param subsubsub_topics: List of subsubsub topics.
    :param individual_radius: Radius for placing each subsubsub topic.
    :return: Dictionary of coordinates for subsubsub topics.
    """
    subsubsub_topic_coords = {}
    num_subsubsub_topics = len(subsubsub_topics)

    # Calculate the angular gap between each subsubsub topic
    if num_subsubsub_topics > 1:
        angle_gap = 2 * math.pi / num_subsubsub_topics
    else:
        angle_gap = 0  # Avoid division by zero if only one subsubsub topic

    # Generate coordinates for each subsubsub topic
    for i, subsubsub_topic in enumerate(subsubsub_topics):
        angle = start_angle + angle_gap * i
        x = individual_radius * math.cos(angle)
        y = individual_radius * math.sin(angle)
        subsubsub_topic_coords[subsubsub_topic] = (x, y)

    return subsubsub_topic_coords


def round_coordinates(coordinates):
    """
    Round the coordinates to two decimal places.
    """
    return [(round(x, 2), round(y, 2)) for x, y in coordinates]


def replace_spaces_in_dictionary(dict):
    dict_new = {key.replace(" ", "_"): [value.replace(" ", "_") for value in values]
                for key, values in dict.items()}       
    return dict_new

def rename_nodes_in_dictionary(topics_and_subtopics, subsub_topics, subsubsub_topics):
    topics_and_subtopics_new = replace_spaces_in_dictionary(topics_and_subtopics)
    subsub_topics_new = replace_spaces_in_dictionary(subsub_topics)
    subsubsub_topics_new = replace_spaces_in_dictionary(subsubsub_topics)
    subsub_topics_renamed = {}
    subsubsub_topics_renamed = {}

    # Renaming subtopics
    for km, subtopics in topics_and_subtopics_new.items():
        modified_subtopics = [km + '->' + subtopic for subtopic in subtopics]
        topics_and_subtopics_new[km] = modified_subtopics

    # Renaming subsub topics
    for ks, subsubtopics in subsub_topics_new.items():
        modified_subsubtopics = []
        for subsubtopic in subsubtopics:
            # Find the main topic and subtopic
            new_subsub_key = ''
            for main_topic, subtopics in topics_and_subtopics_new.items():
                if any(ks in subtopic for subtopic in subtopics):
                    new_subsub_key = f"{main_topic}->{ks}->{subsubtopic}"
                    modified_subsubtopics.append(new_subsub_key)
                    break
            subsub_topics_renamed[new_subsub_key] = subsubtopic

        # Assign the modified list to the key in subsub_topics_new
        subsub_topics_new[ks] = modified_subsubtopics

    # Renaming subsubsub topics based on subsub topics values
    for subsub_key, subsub_value in subsub_topics_renamed.items():
        if subsub_value in subsubsub_topics_new:
            modified_subsubsubtopics = []
            for subsubsub_topic in subsubsub_topics_new[subsub_value]:
                modified_subsubsubtopic = f"{subsub_key}->{subsubsub_topic}"
                modified_subsubsubtopics.append(modified_subsubsubtopic)
            subsubsub_topics_renamed[subsub_key] = modified_subsubsubtopics

    return topics_and_subtopics_new, subsub_topics_new, subsubsub_topics_renamed


def generate_gephi_gdf(topics_and_subtopics, subsub_topics, main_topic_coords, subtopic_coords, subsub_topic_coords, individual_radius_main_topics, individual_radius_subtopics, individual_radius_subsub_topics, topic_colors):
    gdf_content = "nodedef>name VARCHAR,label VARCHAR,width DOUBLE,x DOUBLE,y DOUBLE,color VARCHAR\n"

    # Add nodes for main topics with coordinates, width, and color
    for i, (main_topic, subtopics) in enumerate(topics_and_subtopics.items()):
        x, y = main_topic_coords[i]
        color = f"\"{topic_colors.get(main_topic, '255,255,255')}\""
        gdf_content += f"{main_topic},{main_topic.replace('_',' ')},{individual_radius_main_topics},{x},{y},{color}\n"

        # Add nodes for each subtopic with their coordinates and parent topic's color
        for subtopic in subtopics:
            if subtopic_coords:  # Check for available coordinates
                sub_x, sub_y = subtopic_coords.pop(0)
                gdf_content += f"{subtopic},{subtopic.split('->')[-1].replace('_',' ')},{individual_radius_subtopics},{sub_x},{sub_y},{color}\n"

   # Add nodes for subsub topics with correct color based on main topic
    for subtopic_key, subsub_list in subsub_topics.items():
        # Extract the main topic name from the subtopic key
        main_topic_key = subtopic_key.split('->')[0]
        color = f"\"{topic_colors.get(main_topic_key, '255,255,255')}\""

        for subsub_topic in subsub_list:
            if subsub_topic_coords:  # Check for available coordinates
                subsub_x, subsub_y = subsub_topic_coords.pop(0)
                gdf_content += f"{subsub_topic},{subsub_topic.split('->')[-1].replace('_',' ')},{individual_radius_subsub_topics},{subsub_x},{subsub_y},{color}\n"


    # Add directed edges from main topics to subtopics and from subtopics to subsub topics
    gdf_content += "edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN\n"

 
    # Add directed edges from main topics to subtopics and from subtopics to subsub topics
    for main_topic, subtopics in topics_and_subtopics.items():
        for subtopic in subtopics:
            gdf_content += f"{main_topic},{subtopic},true\n"
            if subtopic in subsub_topics:
                for subsub_topic in subsub_topics[subtopic]:
                    gdf_content += f"{subtopic},{subsub_topic},true\n"

  # Add directed edges between main topics in the order they appear
    main_topics = list(topics_and_subtopics.keys())
    for i in range(len(main_topics) - 1):
        from_topic = main_topics[i]
        to_topic = main_topics[i + 1]
        gdf_content += f"{from_topic},{to_topic},true\n"

    # Add directed edges between adjacent subtopics
    for subtopics in topics_and_subtopics.values():
        for i in range(len(subtopics) - 1):
            gdf_content += f"{subtopics[i]},{subtopics[i + 1]},true\n"
    
    # Add directed edges between adjacent subsub topics
    for subsub_list in subsub_topics.values():
        for i in range(len(subsub_list) - 1):
            gdf_content += f"{subsub_list[i]},{subsub_list[i + 1]},true\n"

    return gdf_content




#######################################################
# Main()
#######################################################


# Parameters for individual topic and subtopic radii
topics_and_subtopics = mt.topics_and_subtopics
subsub_topics = mt.subsub_topics
subsubsub_topics = mt.subsubsub_topics

individual_radius_main_topics = 50
individual_radius_subtopics = 30
individual_radius_subsub_topics = 15
individual_radius_subsubsub_topics = 5

separation_main_topics = 2.0
separation_sub_topics = 1.5
separation_subsub_topics = 1.5
separation_subsubsub_topics = 1.5

topic_colors = mt.topic_colors

# Rename nodes, replace spaces with underscores and provide full taxonomy
topics_and_subtopics_new, subsub_topics_new, subsubsub_topics_new = rename_nodes_in_dictionary(topics_and_subtopics, subsub_topics, subsubsub_topics)

# Generate Coordinates
main_topic_coords, sub_topic_coords = generate_coordinates(topics_and_subtopics_new, individual_radius_main_topics, individual_radius_subtopics,separation_main_topics,separation_sub_topics)
rounded_main_topic_coords = round_coordinates(main_topic_coords)

subsub_topic_starting_radial_angle = find_radial_angle_of_subtopic(main_topic_coords, topics_and_subtopics_new, "Arithmetic" )
subsub_topic_coords = generate_subsub_topic_coordinates(subsub_topics_new, individual_radius_subsub_topics, separation_subsub_topics,subsub_topic_starting_radial_angle)
rounded_sub_topic_coords = round_coordinates(sub_topic_coords)


#subsubsub_topic_starting_radial_angle = find_radial_angle_of_subtopic(subsub_topics_new, subsubsub_topics_new, "Arithmetic->Recognizing_Shapes->Basic_Shapes")
subsubsub_topic_coords = generate_subsubsub_topic_coordinates(math.radians(-180), subsubsub_topics_new, individual_radius_subsubsub_topics)
rounded_subsub_topic_coords = round_coordinates(subsub_topic_coords)

# Export graph in GDF format
gdf_data = generate_gephi_gdf(topics_and_subtopics_new,subsub_topics_new, 
                         rounded_main_topic_coords,rounded_sub_topic_coords,rounded_subsub_topic_coords,
                         individual_radius_main_topics,individual_radius_subtopics,individual_radius_subsub_topics, topic_colors)

# Write the GDF content to a file
file_path = './gephi/math_nodes_and_edges.gdf'
if os.path.exists(file_path):
    os.remove(file_path)

with open(file_path, 'w') as file:
    file.write(gdf_data)

print(gdf_data)
print(f"GDF file saved to: {file_path}")
