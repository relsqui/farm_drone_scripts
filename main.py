import field
import hat
import maze
import plan
import pumpkin
import sunflower
import upgrade

pet_the_piggy()
if get_entity_type() == Entities.Hedge:
  # In case we stopped running mid-maze
  maze.run()
field.go_to_origin()
hat.randomize_hat()
do_a_flip()

sunflower_sizes = []
while True:
    seen_pumpkins = 0
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            next_crop = plan.get_next_crop()
            if can_harvest():
                planted = get_entity_type()
                if planted == Entities.Pumpkin:
                    seen_pumpkins = pumpkin.maybe_harvest_pumpkin(seen_pumpkins)
                elif planted == Entities.Sunflower:
                    sunflower_sizes = sunflower.maybe_harvest_sunflower(sunflower_sizes)
                else:
                    harvest()
            if get_entity_type() != next_crop:
                field.plant_crop(next_crop)
                if next_crop == Entities.Sunflower:
                    sunflower_sizes.append(measure())
            field.maybe_water()
            move(North)
        move(East)
    hat.randomize_hat()
    upgrade.check_upgrades()
    if seen_pumpkins < 2 and maze.should_start_maze():
      maze.clear()
      while maze.should_start_maze():
        maze.init_and_run()
      field.go_to_origin()