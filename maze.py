import drone
import nav
import plan

def get_substance_needed():
    return get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

def should_start_maze():
    return plan.get_priorities()[0] == Items.Gold and num_items(Items.Weird_Substance) >= get_substance_needed()

def init():
    harvest()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, get_substance_needed())

def run(facing = North, turn = nav.right, drones = None):
    while get_entity_type() == Entities.Hedge and not drone.all_finished(drones):
        facing = turn[facing]
        while not can_move(facing):
            facing = turn[turn[turn[facing]]]
        move(facing)
    if get_entity_type() == Entities.Treasure:
        harvest()

def init_and_run():
    init()
    drones = []
    # odd numbers to get it out of phase with directions
    turns = [nav.right, nav.right, nav.right, nav.left, nav.left, nav.left]
    turn_i = 0
    dir_i = 0
    while num_drones() < max_drones():
      def task():
        run(nav.dirs[dir_i], turns[turn_i])
      drones.append(spawn_drone(task))
      dir_i = (dir_i + 1) % len(nav.dirs)
      turn_i = (turn_i + 1) % len(turns)
    run(nav.dirs[dir_i], turns[turn_i], drones)