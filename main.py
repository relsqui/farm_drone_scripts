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

while True:
    for from_xy, to_xy in field.get_subfield_corners():
      task = drone.make_area_plant_task(from_xy, to_xy, plan.get_next_crop())
      drone.spawn_or_do(task)
    upgrade.check_upgrades()
    if maze.should_start_maze():
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      nav.go_origin()