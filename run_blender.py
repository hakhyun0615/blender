import subprocess
import os

# Blender executable path
blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"

# Blender script path
blender_script_path = os.path.abspath("blender_script.py")

# Run Blender with the script
subprocess.run([blender_path, "--background", "--python", blender_script_path])

print("Blender script executed successfully.")