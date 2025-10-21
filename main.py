import drone
import field
import maze
import plan
import task_pumpkin
import task_sunflower
import upgrade

def get_task_for_product(from_xy, to_xy, product):
  if product == Items.Pumpkin:
    return task_pumpkin.make_pumpkin_task(from_xy, to_xy)
  elif product == Items.Power:
    return task_sunflower.make_sunflower_task(from_xy, to_xy)
  else:
    return drone.make_area_plant_task(from_xy, to_xy, plan.producer[product])

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

def assigned_drones(assignments):
  drones = []
  for i in assignments:
    drones.append(assignments[i][1])
  return drones


pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()

assignments = {}
while True:
    subfields = field.get_subfield_corners()
    products = list(plan.producer)
    for i in range(len(subfields)):
      if i in assignments:
        if not has_finished(assignments[i][1]):
          continue
      from_xy, to_xy = subfields[i]
      product = plan.get_needed_product()
      while product not in products or not check_constraints(i, product, from_xy, to_xy, assignments):
        product = products[random() * len(products) // 1]
      drone.await_any()
      drone_ref = spawn_drone(get_task_for_product(from_xy, to_xy, product))
      assignments[i] = (product, drone_ref)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      drone.await_all(assigned_drones(assignments))
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
