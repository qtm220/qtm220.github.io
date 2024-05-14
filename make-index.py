from pathlib import Path
from pybars import Compiler
import math
import subprocess
import yaml

ASSETS_PATH = Path('assets')
ENCRYPTION_KEY = "WdHXFuNAA7HQVtn1BDDY3EEOMaShYf5ruZJxVfjFwGOBlFRIemiMBfRkJYDayRxc34dA3HcmFYhBdoFp6KuPyOzypFIhi2Prw1X6gcgYRlKrdz9RHpNySzvHT1NqViCagzSHJgcamyDuKlTZbAM9OFYDykLjOuPoxDDwd20q0jkcJeeza5StMMTKKJ3RIompZBlksW8bsFbcEGgnxQwimsrsSNxaqItpodVzn422zFwfAZENDtUwrXkH6C75c9vv"

# Materials
exam_names = ['practice-midterm-1.qmd', 'midterm-1.qmd', 'practice-midterm-2.qmd', 'midterm-2.qmd', 'practice-final.qmd', 'final.qmd']
exams = [Path('qtm220/exams') / exam_name for exam_name in exam_names]
lectures = list(Path().glob("qtm220/lectures/Lecture*.qmd"))
homeworks = list(Path().glob("qtm220/homework/homework*.qmd"))

# Functions
def yaml_header(path): 
  return next(yaml.safe_load_all(path.open()))

def rendered(path, encryption_key=None):
  html_path = ASSETS_PATH / path.relative_to('qtm220').with_suffix('.html')
  if (html_path.exists() and html_path.stat().st_mtime > path.stat().st_mtime):
    return html_path
  print(f"rendering {path.name}")
  output=subprocess.run(['quarto', 'render', path.name], cwd=path.parent)
  if output.returncode:
    return ASSETS_PATH / 'does-not-render.html'
  else:
    if encryption_key:
      subprocess.run(['npx', 'pagecrypt', path.with_suffix('.html').as_posix(), html_path.as_posix(), encryption_key])
    else:
      path.with_suffix('.html').rename(html_path)
    return html_path

def href(path): 
  return path.as_posix()


# Render and Sort Lectures
def lecture_key(info): 
  try: return int(info['title'].lstrip('Lecture'))
  except: return math.inf

lecture_info = [yaml_header(path) | {"href": href(rendered(path))} for path in lectures]
lecture_info.sort(key=lecture_key)

# Render and Sort Homework
def homework_key(info): 
  try: return int(info['title'].lstrip('Homework'))
  except: return math.inf

homework_info = [yaml_header(path) | {"href": href(rendered(path, ENCRYPTION_KEY))} for path in homeworks]
homework_info.sort(key=homework_key)

# Render and Sort Exams
exam_info = [yaml_header(path) | {"href": href(rendered(path, ENCRYPTION_KEY))} for path in exams]

# Render the Index Page
compiler = Compiler()
source = open("index.template", "r").read()
template = compiler.compile(source)
output = template({
  'lecture': lecture_info,
  'homework': homework_info,
  'exam': exam_info})    
open('index.html', 'w').write(output)
