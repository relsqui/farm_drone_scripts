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

def run_if_present(task_def, fn):
  if fn in task_def:
    task_def[fn](task_def["state"])

def present_and_true(task_def, fn):
  return fn in task_def and task_def[fn](task_def["state"])

def make_area_task(task_def):
  if "state" not in task_def:
    task_def["state"] = {}

  def task():
    x0, y0 = min(task_def["from"][0], task_def["to"][0]), min(task_def["from"][1], task_def["to"][1]), 
    x1, y1 = max(task_def["from"][0], task_def["to"][0]), max(task_def["from"][1], task_def["to"][1]), 
    while True:
      nav.go_to(x0, y0)
      run_if_present(task_def, "start_fn")
      dir = East
      goal = {East: x1, West: x0}
      while get_pos_y() <= y1:
        if present_and_true(task_def, "break_fn"):
          break
        run_if_present(task_def, "task_fn")
        while get_pos_x() != goal[dir]:
          if present_and_true(task_def, "break_fn"):
            break
          move(dir)
          run_if_present(task_def, "task_fn")
        dir = nav.opposite[dir]
        move(North)
      if not present_and_true(task_def, "continue_fn"):
        break
    run_if_present(task_def, "end_fn")
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
