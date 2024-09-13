import os
import shutil
import argparse
import subprocess
import sys


def RED(text):
    return "\033[91m" + text + "\033[0m"


def GREEN(text):
    return "\033[92m" + text + "\033[0m"


def YELLOW(text):
    return "\033[93m" + text + "\033[0m"


def CYAN(text):
    return "\033[96m" + text + "\033[0m"


parser = argparse.ArgumentParser(
    description="Run this script to create a testapp corresponding to each regular app "
    + "in the applications folder. The testapp groups shared and program-specific code "
    + "with the corresponding unit tests, and can be run with pytest or deployed to a "
    + "board. Optionally run all the unit tests upon building them."
)
parser.add_argument("--run_tests", action="store_true")
args = parser.parse_args()

applications_dir = os.path.join(".", "applications")
unit_test_dir = os.path.join(".", "unit_tests", "applications")
shared_source_dir = os.path.join(".", "shared")
shared_test_source_dir = os.path.join(".", "unit_tests", "shared")

pytest_directories = []

for app in os.listdir(applications_dir):

    if app.startswith(".DS_Store"):
        print(f"Skipping application {app}: .DS_Store directory.")
        continue

    source_dir = os.path.join(applications_dir, app)
    test_source_dir = os.path.join(unit_test_dir, f"{app}_test")

    if app.endswith("_testapp"):
        print(f"Not generating unit tests for application {app}: already a test app")
        continue

    print(CYAN(f"Generating application {app}_testapp..."))
    test_app_dir = os.path.join(".", "applications", f"{app}_testapp")
    print(f"Removing old test application...")
    if os.path.exists(test_app_dir):
        if os.path.isdir(test_app_dir):
            shutil.rmtree(test_app_dir)
        else:
            os.remove(test_app_dir)
    # copy shared things first, so that each application can override shared files if needed
    # copy application before tests, so that test code can override application code if needed
    print(f"Copying conftest.py to {app}_testapp...")
    os.mkdir(test_app_dir)
    shutil.copyfile(
        os.path.join(".", "config", "conftest.py"),
        os.path.join(test_app_dir, "conftest.py"),
    )
    for dir in [shared_source_dir, shared_test_source_dir, source_dir, test_source_dir]:
        if os.path.exists(dir) and os.path.isdir(dir):
            print(f"Copying source files from {dir} to {app}_testapp...")
            shutil.copytree(dir, test_app_dir, symlinks=False, dirs_exist_ok=True)
        else:
            reason = (
                "required directory, but found file"
                if os.path.exists(dir)
                else "directory does not exist"
            )
            print(
                YELLOW(f"Skipping source files from {dir} for {app}_testapp: {reason}.")
            )
    print(GREEN(f"Generated application {app}_testapp!"))

    if args.run_tests:
        pytest_directories.append(test_app_dir)

tests_passed = True
for test_app_dir in pytest_directories:
    print(CYAN(f"Running pytest for {test_app_dir}..."))
    if subprocess.run(["sys.executable", "-m", "pytest"], cwd=test_app_dir).returncode != 0:
        tests_passed = False
exit(0 if tests_passed else 1)
