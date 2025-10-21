import drone
import nav

def plant_if_necessary():
    if get_entity_type() != Entities.Pumpkin:
        if can_harvest():
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Pumpkin)
        return True
    return False

def plant_pumpkin(state):
    if plant_if_necessary():
        state["to_check"].append((get_pos_x(), get_pos_y()))

def check_pumpkins(state):
    while len(state["to_check"]) > 0:
        check_next = []
        for x, y in state["to_check"]:
            nav.go_to(x, y)
            if plant_if_necessary() or not can_harvest():
                check_next.append((x, y))
        state["to_check"] = check_next
    harvest()

def make_pumpkin_task(x, y, size):
    return drone.make_area_task({
        "from": (x, y),
        "to": (x + size - 1, y + size - 1),
        "task_fn": plant_pumpkin,
        "end_fn": check_pumpkins,
        "state": {
            "to_check": []
        }
    })

def spawn_pumpkin_patch():
    repeats = ((max_drones() ** 0.5) // 1) + 1
    spacing = get_world_size() // repeats
    size = spacing - 1
    for x in range(repeats):
        for y in range(repeats):
            drone.spawn_or_do(make_pumpkin_task(x * spacing, y * spacing, size))
