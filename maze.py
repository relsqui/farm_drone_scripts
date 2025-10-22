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

def available_moves(facing):
    moves = []
    for dir in {facing, nav.right[facing], nav.left[facing]}:
        if can_move(dir):
            moves.append(dir)
    return moves

def send_drone(facing):
    def task():
        run(facing)
    drone.await_any()
    spawn_drone(task)

def run(facing):
    while not maze_done():
        check_treasure()
        moves = available_moves(facing)
        while len(moves) > 1:
            send_drone(moves.pop())
        if len(moves) > 0:
            run(moves.pop())

def init_and_run():
    init()
    for dir in {South, East, West}:
        send_drone(dir)
    run(North)
