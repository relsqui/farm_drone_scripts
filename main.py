import drone
import field
import maze
import nav
import plan
import upgrade

pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()
nav.go_origin()
do_a_flip()

def get_adjacency(index):
  # Given a subfield index, return 0 or 1 such that
  # subfields assigned 0 and 1 make a checkerboard
  # (Assumes world size hasn't changed)
  repeats = field.get_subfield_stats()["repeats"]
  row = index // repeats
  column = index - (row * repeats)
  return ((column % 2) + (row % 2)) % 2

def check_constraints(index, product):
  # Ensure only one sunflower field by only allowing it at index 0
  if product == Items.Power:
    return index == 0
  # Ensure cactus and pumpkin fields aren't adjacent to like fields
  if product == Items.Cactus:
    return get_adjacency(index) == 0
  if product == Items.Pumpkin:
    return get_adjacency(index) == 1
  return product != None

while True:
    subfields = field.get_subfield_corners()
    products = list(plan.producer)
    for i in range(len(subfields)):
      product = None
      while not check_constraints(i, product):
        product = products[random() * len(products) // 1]
      from_xy, to_xy = subfields[i]
      task = drone.make_area_plant_task(from_xy, to_xy, plan.producer[product])
      drone.spawn_or_do(task)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      nav.go_origin()