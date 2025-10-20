import field
import plan
import nav

def spawn_or_do(task):
  if num_drones() < max_drones():
    return spawn_drone(task)
  else:
    task()

def all_finished(drones):
    if drones == None:
        return False
    for drone in drones:
        if has_finished(drone):
            drones.remove(drone)
        else:
            return False
    return True

def await_all(drones):
  if drones == None:
    return
  for drone in drones:
    if drone:
      wait_for(drone)

def run_if_present(state, fn):
  if fn in state:
    state[fn](state)
  return state

def make_area_task(task_state):
  # currently x0, y0 should be NW of x1, y1
  def task():
    state = task_state
    x0, y0 = state["from"]
    x1, y1 = state["to"]
    while True:
      state = run_if_present(state, "start_fn")
      dir = East
      goal = {East: x1, West: x0}
      nav.go_to(x0, y0)
      while get_pos_y() >= y1:
        state = run_if_present(state, "task_fn")
        while get_pos_x() != goal[dir]:
          move(dir)
          state = run_if_present(state, "task_fn")
        dir = nav.opposite[dir]
        move(South)
      if not ("continue_fn" in state and state["continue_fn"](state)):
        break
    run_if_present(state, "end_fn")
  return task

def make_column_task(fn):
  def task():
    start_y = get_pos_y()
    just_started = True
    while just_started == True or get_pos_y() != start_y:
      just_started = False
      fn()
      move(North)
  return task

def replant_task():
  harvest_task()
  field.plant_crop(plan.get_next_crop())

def harvest_task():
  if can_harvest():
    harvest()
