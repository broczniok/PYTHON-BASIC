"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_part_2')))
import task_read_write

filepath = "/Users/broczniok/Desktop/PYTHON-BASIC/practice/python_part_2/files/"
CONTENT = str(task_read_write.read_file(filepath))

def test_read_and_write_to_file(tmp_path):
   d = tmp_path / "files"
   d.mkdir()
   p = d / "result_1.txt"

   task_read_write.write_file(task_read_write.read_file(filepath),filepath)

   p.write_text(str(task_read_write.read_file(filepath)))

   result_file = tmp_path / "files/result_1.txt"
   
   assert result_file.read_text() == CONTENT
   assert len(list(tmp_path.iterdir())) == 1
   assert 0


