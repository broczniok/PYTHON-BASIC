"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '2_python_part_2'))

import importlib
res = importlib.import_module('task_read_write')

#CONTENT = str(res.read_file(filepath))
CONTENT = [1, 2, 3]

def test_read_and_write_to_file(tmp_path):
   d = tmp_path / "files"
   d.mkdir()
   file_path_1 = d / "file_1.txt"
   file_path_2 = d / "file_2.txt"
   file_path_3 = d / "file_3.txt"


   with open(file_path_1, "w") as f:
      f.write(str(CONTENT[0]))

   with open(file_path_2, "w") as f:
      f.write(str(CONTENT[1]))
      
   with open(file_path_3, "w") as f:
      f.write(str(CONTENT[2]))

   read_content = res.read_file(d)

   res.write_file(read_content, d)
    
   result_file = d / "result_1.txt"

   assert read_content == CONTENT
   assert res.read_file(result_file.parent) == CONTENT
   assert len(list(d.iterdir())) > 0
   


