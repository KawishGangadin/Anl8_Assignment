import subprocess
import sys

class Dependencies:

    def dependenciesInstaller():

        depens = ["bcrypt==4.1.3", "cryptography==42.0.8"]

        for i in depens:
            try:
                subprocess.call([sys.executable, '-m', 'pip', 'install', i])
                print(f"Installed {i}")
            except Exception as e:
                print(f"Error installing {i}: {e}")