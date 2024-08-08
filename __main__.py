import subprocess
import sys
import os

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_path)
    script_path = os.path.join(project_path, 'src', 'organizer', 'main_code.py')
    subprocess.run([sys.executable, script_path])