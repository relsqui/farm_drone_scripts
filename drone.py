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

def noop(state):
  pass

def return_false(state):
  return False

base_task = {
  "state": {},
  "start_fn": noop,
  "task_fn": noop,
  "end_fn": noop,
  "continue_fn": return_false,
  "break_fn": return_false,
}

def normalize_task_def(task_options):
  task_def = {}
  for key in base_task:
    task_def[key] = base_task[key]
  for key in task_options:
    task_def[key] = task_options[key]
  return task_def

def make_area_task(task_options):
  task_def = normalize_task_def(task_options)
  state = task_def["state"]
  x0, y0 = min(task_def["from"][0], task_def["to"][0]), min(task_def["from"][1], task_def["to"][1])
  x1, y1 = max(task_def["from"][0], task_def["to"][0]), max(task_def["from"][1], task_def["to"][1])

  def task():
    while True:
      nav.go_to(x0, y0)
      task_def["start_fn"](state)
      dir = East
      goal = {East: x1, West: x0}
      while get_pos_y() <= y1:
        if task_def["break_fn"](state):
          break
        task_def["task_fn"](state)
        while get_pos_x() != goal[dir]:
          if task_def["break_fn"](state):
            break
          move(dir)
          task_def["task_fn"](state)
        dir = nav.opposite[dir]
        move(North)
      if not task_def["continue_fn"](state):
        break
    task_def["end_fn"](state)
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
  field.clear_and_plant_crop(plan.get_next_crop())
  field.maybe_fertilize()

def harvest_task():
  if can_harvest():
    harvest()
