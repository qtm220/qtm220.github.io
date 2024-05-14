from pathlib import Path
from pybars import Compiler
import math
import subprocess
import yaml

# Materials
exam_names = ['practice-midterm-1.qmd', 'midterm-1.qmd', 'practice-midterm-2.qmd', 'midterm-2.qmd', 'practice-final.qmd', 'final.qmd']
exams = [Path('qtm220/exams') / exam_name for exam_name in exam_names]
lectures = list(Path().glob("qtm220/lectures/Lecture*.qmd"))
homeworks = list(Path().glob("qtm220/homework/homework*.qmd"))

# Functions
def yaml_header(path): 
  return next(yaml.safe_load_all(path.open()))

def rendered(path):
  if (path.with_suffix('.html').exists() and
      path.with_suffix('.html').stat().st_mtime > path.stat().st_mtime):
    return path.with_suffix('.html')
  print(f"rendering {path.name}")
  output=subprocess.run(['quarto', 'render', path.name], cwd=path.parent)
  if output.returncode:
    return path.parent / 'does-not-compile.html'
  else:
    return path.with_suffix('.html')

def href(path): 
  return path.relative_to('.', walk_up=True).as_posix()


# Render and Order Lectures
def lecture_key(info): 
  try: return int(info['title'].lstrip('Lecture'))
  except: return math.inf

lecture_info = [yaml_header(path) | {"href": href(rendered(path))} for path in lectures]
lecture_info.sort(key=lecture_key)

# Render and Order Homework
def homework_key(info): 
  try: return int(info['title'].lstrip('Homework'))
  except: return math.inf

homework_info = [yaml_header(path) | {"href": href(rendered(path))} for path in homeworks]
homework_info.sort(key=homework_key)

# Render and Order Exams
exam_info = [yaml_header(path) | {"href": href(rendered(path))} for path in exams]

# Render the Index Page
compiler = Compiler()
source = open("index.template", "r").read()
template = compiler.compile(source)
output = template({
  'lecture': lecture_info,
  'homework': homework_info,
  'exam': exam_info})    
open('index.html', 'w').write(output)
