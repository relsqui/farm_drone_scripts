import drone
import field
import nav

def plant_if_necessary():
    if get_entity_type() != Entities.Pumpkin:
        field.clear_and_plant_crop(Entities.Pumpkin)
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

def make_pumpkin_task(from_xy, to_xy):
    return drone.make_area_task({
        "from": from_xy,
        "to": to_xy,
        "task_fn": plant_pumpkin,
        "end_fn": check_pumpkins,
        "state": {
            "to_check": []
        }
    })

def spawn_pumpkin_patch():
    for from_xy, to_xy in field.get_subfield_corners(1):
        drone.spawn_or_do(make_pumpkin_task(from_xy, to_xy))
