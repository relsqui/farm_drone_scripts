import maze
import plan
import upgrade

def go_to_origin():
    while get_pos_x() != 0:
        move(West)
    while get_pos_y() != 0:
        move(South)

def plant_crop(crop):
  if get_ground_type() != Grounds.Soil:
    till()
  plant(crop)
  maybe_fertilize()

def maybe_water():
    # Crop growth speed is not currently a limiting factor
    return
    if get_water() < 0.75 and num_items(Items.Water) > 1:
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
  costs = upgrade.get_upgrade_costs()
  for key in costs:
    cost = costs[key]
    if Items.Gold in cost and num_items(Items.Gold) < cost[Items.Gold]:
      use_item(Items.Fertilizer)
      return