import os
import subprocess

def run_tests():
    subprocess.run(["python", "tests/products_test.py"])

if __name__ == "__main__":
    run_tests()
