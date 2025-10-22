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

def check_treasure():
    if get_entity_type() == Entities.Treasure:
        harvest()

def maze_done():
    return get_entity_type() not in {Entities.Hedge, Entities.Treasure}

def run(facing):
    while can_move(facing):
        if maze_done():
            return
        move(facing)
        check_treasure()
        for dir in {nav.right[facing], nav.left[facing]}:
            send_drone(dir)

def send_drone(facing):
    if not can_move(facing):
        return
    def task():
        run(facing)
    drone.await_any(do_a_flip)
    spawn_drone(task)

def init_and_run():
    init()
    check_treasure()
    change_hat(Hats.Purple_Hat)
    for dir in {North, South, East, West}:
        send_drone(dir)
