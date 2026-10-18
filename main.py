import subprocess
import sys


def main():
    print("Starting Automated Backup System...")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app/ui/dashboard.py",
        ],
        check=False,
    )


if __name__ == "__main__":
    main()
