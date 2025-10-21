import drone
import field
import maze
import nav
import plan
import task_pumpkin
import upgrade

pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()
nav.go_origin()
do_a_flip()

def get_task_for_product(from_xy, to_xy, product):
  if product in plan.producer:
    return drone.make_area_plant_task(from_xy, to_xy, plan.producer[product])
  elif product == Entities.Pumpkin:
    return task_pumpkin.make_pumpkin_task(from_xy, to_xy)

def check_constraints(index, product, from_xy, to_xy):
  # Ensure only one sunflower field by only allowing it and only it at index 0
  # TODO after I have priorities working, remove the "and only it"
  if product == Items.Power:
    return index == 0
  elif index == 0:
    return False
  # Ensure cactus fields aren't adjacent to each other
  if product == Items.Cactus:
    return field.get_adjacency(index) == 0
  # Same for pumpkins, and that they're not in the non-square edge fields
  if product == Items.Pumpkin:
    return field.get_adjacency(index) == 1 and field.is_square(from_xy, to_xy)
  return product != None

while True:
    subfields = field.get_subfield_corners()
    products = list(plan.producer)
    for i in range(len(subfields)):
      from_xy, to_xy = subfields[i]
      if i == 0:
        product = Items.Power
      else:
        product = plan.get_needed_product()
        while product not in products or not check_constraints(i, product, from_xy, to_xy):
          product = products[random() * len(products) // 1]
      drone.spawn_or_do(get_task_for_product(from_xy, to_xy, product))
    upgrade.check_upgrades()
    if maze.should_start_maze():
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      nav.go_origin()