dirs = [North, South, East, West]

right = {
    North: East,
    East: South,
    South: West,
    West: North
}

left = {
    North: West,
    West: South,
    South: East,
    East: North
}

opposite = {
  North: South,
  South: North,
  West: East,
  East: West
}

def go_to(to_x, to_y):
  ws = get_world_size()
  from_x, from_y = get_pos_x(), get_pos_y()
  if from_x - to_x > 0 and (from_x - to_x) < ws/2:
    lat_dir = West
  else:
    lat_dir = East
  if from_y - to_y > 0 and (from_y - to_y) < ws/2:
    long_dir = South
  else:
    long_dir = North
  while get_pos_x() != to_x:
    move(lat_dir)
  while get_pos_y() != to_y:
    move(long_dir)

def go_origin():
  go_to(0, 0)
