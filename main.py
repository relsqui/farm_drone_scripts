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

def get_adjacency(index, repeats):
  # Given an index and the side length of a square,
  # return 0 or 1 such that if you lined up the results
  # by index in the square, they'd make a checkerboard
  row = index // repeats
  column = index - (row * repeats)
  return ((column % 2) + (row % 2)) % 2

while True:
    repeats = field.get_subfield_stats()["repeats"]
    subfields = field.get_subfield_corners()
    crops = [Entities.Pumpkin, Entities.Cactus]
    for i in range(len(subfields)):
      from_xy, to_xy = subfields[i]
      crop = crops[get_adjacency(i, repeats)]
      task = drone.make_area_plant_task(from_xy, to_xy, crop)
      drone.spawn_or_do(task)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      nav.go_origin()