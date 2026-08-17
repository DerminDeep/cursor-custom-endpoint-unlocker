import os
import sys

# Run directly
script_path = os.path.join(os.path.dirname(__file__), "app.py")
os.system(f'pythonw "{script_path}"')
