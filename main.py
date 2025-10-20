import drone
import field
import hat
import maze
import plan
import upgrade

pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()
field.go_to_origin()
hat.randomize_hat()
do_a_flip()

while True:
    for x in range(get_world_size()):
        next_crop = plan.get_next_crop()
        task = drone.make_column_task(drone.make_replant_task(next_crop))
        drone.spawn_or_do(task)
        move(East)
    hat.randomize_hat()
    upgrade.check_upgrades()
    if maze.should_start_maze():
      field.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      field.go_to_origin()