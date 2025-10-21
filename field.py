import drone
import maze
import nav
import plan
import upgrade


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

def maybe_water():
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