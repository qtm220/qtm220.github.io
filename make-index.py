from pathlib import Path
from pybars import Compiler
import math
import subprocess
import yaml

ASSETS_PATH = Path('assets')

# Materials
exam_names = ['midterm-1.qmd', 'midterm-2.qmd', 'final.qmd']
exams = [Path('qtm220/exams') / exam_name for exam_name in exam_names]
practice_exams = [Path('qtm220/exams') / ('practice-' + exam_name) for exam_name in exam_names]
lectures = list(Path().glob("qtm220/lectures/Lecture*.qmd"))
homeworks = list(Path().glob("qtm220/homework/homework*.qmd"))

# Functions
def yaml_header(path): 
  return next(yaml.safe_load_all(path.open()))

def rendered(path, dash_whatever=''):
  html_path = (ASSETS_PATH / path.relative_to('qtm220').parent / (path.with_suffix('').name + dash_whatever)).with_suffix('.html') 
  if (html_path.exists() and html_path.stat().st_mtime > path.stat().st_mtime):
    return html_path
  print(f"rendering {html_path.name}")
  output=subprocess.run(['quarto', 'render', path.name], cwd=path.parent)
  if output.returncode:
    return ASSETS_PATH / 'does-not-compile.html'
  else:
    path.with_suffix('.html').rename(html_path)
    return html_path

def rendered_with_callout(path, callout='assignment-callout.lua', dash_whatever=''):
  custom_callout = path.parent / 'custom-callout.lua'
  bakfile = custom_callout.rename(custom_callout.with_suffix('.lua.bak'))
  
  custom_callout.symlink_to(callout)
  html_path = rendered(path, dash_whatever)
  
  bakfile.rename(custom_callout)
  return html_path

def assignment_and_solution(path):
  return {'assignment_href': rendered_with_callout(path, 'assignment-callout.lua'),
	  'solution_href':   rendered_with_callout(path, 'solution-callout.lua', '-solution')}

# Render and Order Lectures
def lecture_key(info): 
  try: return int(info['title'].lstrip('Lecture'))
  except: return math.inf

lecture_info = [yaml_header(path) | {"href": rendered(path)} for path in lectures]
lecture_info.sort(key=lecture_key)

# Render and Order Homework
def homework_key(info): 
  try: return int(info['title'].lstrip('Homework'))
  except: return math.inf

homework_info = [yaml_header(path) | assignment_and_solution(path) for path in homeworks]
homework_info.sort(key=homework_key)

# Render and Order Exams
exam_info = [yaml_header(path) | assignment_and_solution(path) for path in exams]
practice_exam_info = [yaml_header(path) | assignment_and_solution(path) for path in practice_exams]


# Render the Index Page
compiler = Compiler()
source = open("index.template", "r").read()
template = compiler.compile(source)
output = template({
  'lecture': lecture_info,
  'homework': homework_info,
  'exam': exam_info,
  'practice_exam': practice_exam_info})    
open('index.html', 'w').write(output)
