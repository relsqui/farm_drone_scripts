import drone
import field
import maze
import plan
import task_pumpkin
import task_sunflower
import upgrade

product_task = {
  Items.Pumpkin: task_pumpkin.make_pumpkin_task,
  Items.Power: task_sunflower.make_sunflower_task
}

producer = {
  Items.Carrot: Entities.Carrot,
  Items.Hay: Entities.Grass,
  Items.Power: Entities.Sunflower,
  Items.Cactus: Entities.Cactus,
  Items.Pumpkin: Entities.Pumpkin
}

def get_task_for_product(from_xy, to_xy, product):
  if product in product_task:
    return product_task[product](from_xy, to_xy)
  if product in producer:
    return drone.make_area_plant_task(from_xy, to_xy, producer[product])
  return None

def currently_growing(product, assignments):
  for i in assignments:
    p, d = assignments[i]
    if p == product and not has_finished(d):
      return True
  return False

def check_constraints(index, product, from_xy, to_xy, assignments):
  if product not in product_task and product not in producer:
    return False
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
    for i in range(len(subfields)):
      if i in assignments:
        if not has_finished(assignments[i][1]):
          continue
      from_xy, to_xy = subfields[i]
      product = Items.Hay
      if not currently_growing(Items.Power, assignments):
        product = Items.Power
      for p in plan.get_priorities():
        if check_constraints(i, p, from_xy, to_xy, assignments):
          product = p
          break
      drone.await_any()
      drone_ref = spawn_drone(get_task_for_product(from_xy, to_xy, product))
      assignments[i] = (product, drone_ref)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      drone.await_all(assigned_drones(assignments))
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
