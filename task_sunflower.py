import drone
import field
import nav

def plant_sunflower(state):
    field.plant_if_necessary(Entities.Sunflower)
    petals = measure()  
    if petals not in state["sizes"]:
        state["sizes"][petals] = []
    state["sizes"][petals].append((get_pos_x(), get_pos_y()))

def harvest_sunflowers(state):
    petals = 15
    while petals > 6:
        if petals not in state["sizes"]:
            continue
        for x, y in state["sizes"][petals]:
            nav.go_to(x, y)
            while not can_harvest():
                do_a_flip()
            harvest()
        petals -= 1

def make_sunflower_task(from_xy, to_xy):
    return drone.make_area_task({
        "from": from_xy,
        "to": to_xy,
        "task_fn": plant_sunflower,
        "end_fn": harvest_sunflowers,
        "state": {
            "sizes": {}
        }
    })