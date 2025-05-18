import argparse
import os
import subprocess
import sys

def run_ns_process_data(images_dir, ns_output_dir):
    print("\n== Конвертация изображений ⇒ Nerfstudio ==")
    if not os.path.isdir(images_dir):
        raise FileNotFoundError(f"Директория с изображениями не найдена: {images_dir}")
    os.makedirs(ns_output_dir, exist_ok=True)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    cmd = [
        "ns-process-data", "images",
        "--data", images_dir,
        "--output-dir", ns_output_dir,
        "--skip-colmap"
    ]
    print("Выполняется команда:", " ".join(cmd))
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    print(res.stdout)
    if res.returncode != 0:
        print("== Ошибка конвертации! ==")
        sys.exit(res.returncode)
    print(f"\nГотово. Датасет Nerfstudio в {os.path.abspath(ns_output_dir)}")

def main():
    parser = argparse.ArgumentParser(description="Конвертация изображений в формат Nerfstudio (ns-process-data images)")
    parser.add_argument('--images', required=True, help="Путь к папке с изображениями")
    parser.add_argument('--output-dir', required=True, help="Папка для выходных данных Nerfstudio")
    args = parser.parse_args()

    run_ns_process_data(args.images, args.output_dir)

if __name__ == '__main__':
    main()