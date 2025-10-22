import drone
import maze
import nav
import plan
import upgrade

def get_subfield_stats(margin = 0):
    ws = get_world_size()
    repeats = ((max_drones() ** 0.5) // 1) + 1
    spacing = ws // repeats
    return {
      "repeats": repeats,
      "spacing": spacing,
      "size": spacing - margin,
      "offset": spacing - margin - 1,
      "remainder": ws - (repeats * spacing)
    }

def get_subfield_corners(margin = 0, allow_nonsquare_edges = True):
    subfield_stats = get_subfield_stats(margin)
    repeats = subfield_stats["repeats"]
    spacing = subfield_stats["spacing"]
    offset = subfield_stats["offset"]
    remainder = subfield_stats["remainder"]
    subfields = []
    for x in range(repeats):
      extra_x = 0
      if allow_nonsquare_edges and x == repeats - 1:
        extra_x = remainder
      for y in range(repeats):
        extra_y = 0
        if allow_nonsquare_edges and y == repeats - 1:
          extra_y = remainder
        subfields.append((
          (x * spacing, y * spacing),
          ((x * spacing) + offset + extra_x, (y * spacing) + offset + extra_y)
        ))
    return subfields

def index_to_row_column_repeats(index):
  repeats = get_subfield_stats()["repeats"]
  row = index // repeats
  column = index - (row * repeats)
  return row, column, repeats

def get_adjacency(x, y):
  return ((x % 2) + (y % 2)) % 2

def get_index_adjacency(index):
  # Given a subfield index, return 0 or 1 such that
  # subfields assigned 0 and 1 make a checkerboard
  # (Assumes world size hasn't changed)
  row, column, _ = index_to_row_column_repeats(index)
  return get_adjacency(row, column)

def get_pos_adjacency():
  # Like the above but for coordinates
  return get_adjacency(get_pos_x(), get_pos_y())

def is_square(from_xy, to_xy):
  return from_xy[0] - to_xy[0] == from_xy[1] - to_xy[1]

def clear():
    nav.go_origin()
    drones = []
    for x in range(get_world_size()):
        task = drone.make_column_task(drone.harvest_task)
        drones.append(drone.spawn_or_do(task))
        move(East)
    drone.await_all(drones)

def plant_crop(crop):
  if get_ground_type() != Grounds.Soil:
    till()
  plant(crop)
  maybe_fertilize()
  maybe_water()

def clear_and_plant_crop(crop, force = False):
  if can_harvest():
    harvest()
  elif force:
    till()
  plant_crop(crop)

def plant_if_necessary(crop):
  if get_entity_type() != crop:
    clear_and_plant_crop(crop, True)
    return True
  return False

def maybe_water():
  while get_water() < 0.75 and num_items(Items.Water) > 1:
    use_item(Items.Water)

def maybe_fertilize():
  if get_entity_type() in plan.get_missing_requirements():
    return
  if num_unlocked(Unlocks.Mazes) == 0:
    return
  if num_items(Items.Fertilizer) == 0:
    return
  if num_items(Items.Weird_Substance) > maze.get_substance_needed():
    return
  if Items.Gold in plan.get_priorities():
    use_item(Items.Fertilizer)
