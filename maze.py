import drone
import field
import plan

right = {
    North: East,
    East: South,
    South: West,
    West: North
}

left = {
    North: West,
    West: South,
    South: East,
    East: North
}

def get_substance_needed():
    return get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

def should_start_maze():
    return len(plan.get_missing_requirements()) == 0 and num_items(Items.Weird_Substance) >= get_substance_needed()

def clear():
    field.go_to_origin()
    drones = []
    for x in range(get_world_size()):
        task = drone.make_column_task(drone.make_replant_task())
        drones.append(drone.spawn_or_do(task))
        move(East)
    drone.await_all(drones)

def init():
    harvest()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, get_substance_needed())

def run(facing = North, turn = right, drones = None):
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
    dirs = [North, South, East, West]
    dir_i = 0
    # odd numbers to get it out of phase with directions
    turns = [right, right, right, left, left, left]
    turn_i = 0
    while num_drones() < max_drones():
      def task():
        run(dirs[dir_i], turns[turn_i])
      drones.append(spawn_drone(task))
      dir_i = (dir_i + 1) % len(dirs)
      turn_i = (turn_i + 1) % len(turns)
    run(dirs[dir_i], turns[turn_i], drones)