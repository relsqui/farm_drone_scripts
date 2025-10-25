import drone
import field
import nav

def plant_sunflower(state):
    field.plant_if_necessary(Entities.Sunflower)
    petals = measure()  
    if petals not in state["sizes"]:
        state["sizes"][petals] = []
    state["sizes"][petals].append(field.get_pos())

def harvest_sunflowers(state):
    while len(state["sizes"]) > 0:
        max_petals = max(list(state["sizes"]))
        for pos in state["sizes"][max_petals]:
            nav.go_to(pos)
            if not can_harvest():
                continue
            harvest()
            state["sizes"][max_petals].remove(pos)
            if len(state["sizes"][max_petals]) == 0:
                state["sizes"].pop(max_petals)

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