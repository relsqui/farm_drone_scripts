import drone
import field
import maze
import nav
import plan
import task_pumpkin
import task_sunflower
import upgrade

def get_task_for_product(from_xy, to_xy, product):
  if product in plan.producer:
    return drone.make_area_plant_task(from_xy, to_xy, plan.producer[product])
  elif product == Items.Pumpkin:
    return task_pumpkin.make_pumpkin_task(from_xy, to_xy)
  elif product == Items.Power:
    return task_sunflower.make_sunflower_task(from_xy, to_xy)

def currently_growing(product, assignments):
  for i in assignments:
    if assignments[i][0] == product:
      return True
  return False

def check_constraints(index, product, from_xy, to_xy, assignments):
  if product == Items.Power:
    return not currently_growing(Items.Power, assignments)
  if product == Items.Cactus:
    return field.get_adjacency(index) == 0
  if product == Items.Pumpkin:
    return field.get_adjacency(index) == 1 and field.is_square(from_xy, to_xy)
  return True


pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()

while True:
    subfields = field.get_subfield_corners()
    products = list(plan.producer)
    assignments = {}
    for i in range(len(subfields)):
      if i in assignments:
        drone_ref = assignments[i][1]
        if drone_ref != None and not has_finished(drone_ref):
          print(i, assignments[i], "isn't done yet")
          continue
      from_xy, to_xy = subfields[i]
      product = plan.get_needed_product()
      while product not in products or not check_constraints(i, product, from_xy, to_xy, assignments):
        product = products[random() * len(products) // 1]
      drone_ref = drone.spawn_or_do(get_task_for_product(from_xy, to_xy, product))
      assignments[i] = (product, drone_ref)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      for i in assignments:
        _, drone_ref = assignments[i]
        if drone_ref != None:
          wait_for(drone_ref)
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
