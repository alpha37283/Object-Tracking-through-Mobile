import math

# finding distance and angle

def calculate_distance(focal_length, real_height, bbox_height_px):
    return (focal_length * real_height) / bbox_height_px

def calculate_angle(image_width, bbox_center_x, focal_length):
    dx = bbox_center_x - (image_width / 2)
    return math.degrees(math.atan(dx / focal_length))
