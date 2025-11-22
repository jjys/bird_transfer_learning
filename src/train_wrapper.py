import setuptools
import distutils
import os
import sys

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.getcwd())

# Now run the original training script
import src.train
