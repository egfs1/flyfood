import json
import os
import time
import datetime
import matplotlib.pyplot as plt
from two_opt import melhor_percurso

CONFIG_FILE_PATH = 'config.json'

if __name__ == '__main__':
  # Read the configuration file
  config = {}
  with open(CONFIG_FILE_PATH, 'r') as config_file:
    config = json.load(config_file)

  # Create output folder
  output_folder = config['outputFolder']
  os.makedirs(output_folder, exist_ok=True)

  # Get test case file
  test_file = config['testFile']
  test_file_name = os.path.basename(test_file)

  # Extract delivery points
  delivery_points = {}
  with open(test_file, 'r') as test_file:
    lines = test_file.readlines()
    for line in lines:
      line = line.strip()
      if line == "EOF":
        break

      parts = line.split()
      if not line[0].isnumeric():
        continue

      delivery_points[parts[0]] = (int(float(parts[1])), int(float(parts[2])))

  # TODO: tratar o ponto inicial
  delivery_points['R'] = (0, 0)

  selected_algorithm = config['algorithm']
  test_quantity = config['testQuantity']
  tests = []
  times_difference = []

  for i in range(test_quantity):
    cost = 0
    path = []
    time_difference = 0

    if selected_algorithm == 'two_opt':
      start_time = time.time_ns()
      cost, path = melhor_percurso(delivery_points['R'], delivery_points)
      time_difference = (time.time_ns() - start_time) / 1000000

    if selected_algorithm == 'genetic_algorithm':
      pass

    times_difference.append(time_difference)
    tests.append({
      'test_file': test_file_name,
      'test_case': i + 1,
      'cost': cost,
      'path': path,
      'time': f'{time_difference}ms'
    })

  # Create output files
  print(f'Creating output files in {output_folder} ...')
  now = datetime.datetime.now()
  new_folder_name = f'{output_folder}/{selected_algorithm}_{now.strftime("%Y%m%d%H%M%S")}'
  os.makedirs(new_folder_name, exist_ok=True)
  for i, test in enumerate(tests):
    new_file_name = f'{new_folder_name}/test_{i + 1}.json'
    os.makedirs(new_folder_name, exist_ok=True)
    with open(new_file_name, 'w') as output_file:
      json.dump(test, output_file, indent=2)

  # Plot the path
  print('Plotting the path ...')
  path = tests[0]['path']
  path.append('R')
  coords = [delivery_points[point] for point in path]
  x, y = zip(*coords)
  plt.figure(figsize=(20, 20))
  plt.plot(x, y, marker='o', color='b', linestyle='-', markersize=8)

  for point, (x_p, y_p) in delivery_points.items():
    font_properties = {'fontsize': 9, 'color': 'black', 'ha': 'right'}
    if point == 'R':
      font_properties['weight'] = 'bold'
    plt.text(x_p, y_p, f'{point}({x_p},{y_p})', font_properties)

  plt.xticks(range(min(x) - 100, max(x) + 100, 100))
  plt.yticks(range(min(y) - 100, max(y) + 100, 100))
  plt.title('Path of the delivery points')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.grid(True, which='both', linestyle='--', linewidth=0.5)
  plt.gca().set_aspect('equal', adjustable='box')
  plt.savefig(f'{new_folder_name}/plot_path.png')
  # plt.show()

  # Plot the time difference
  print('Plotting the time difference ...')
  test_cases = [i + 1 for i in range(test_quantity)]
  plt.figure(figsize=(10, 5))
  plt.plot(test_cases, times_difference, marker='o')
  plt.xlabel('Test case')
  plt.ylabel('Time difference (ms)')
  plt.title('Time difference for each test case')

  for i, txt in enumerate(times_difference):
    plt.text(i + 1, txt, f'{txt:.2f}ms', ha='center', va='bottom', fontsize=9, color='black')

  plt.grid(True, which='both', linestyle='--', linewidth=0.5)
  plt.xticks(test_cases)

  max_time = max(int(max(times_difference) + 10), 100)
  plt.yticks(range(0, max_time, 10))
  plt.savefig(f'{new_folder_name}/plot_time_difference.png')
  # plt.show()
    