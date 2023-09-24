import subprocess

# 순차적으로 실행할 파일 목록
files_to_run = ["opencv1.py", "opencv2.py"]

for file in files_to_run:
    print(f"Running {file}...")
    subprocess.run(["python", file])
    print(f"{file} finished.\n")
