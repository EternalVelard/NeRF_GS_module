import argparse
import subprocess
import os
import sys

def run_training(model, data_dir, extra_args):
    import os, sys
    cmd = ["ns-train", model, "--data", data_dir]
    if extra_args:
        cmd.extend(extra_args)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    print("Запускается тренировка Nerfstudio:")
    print(" ".join(cmd))
    proc = subprocess.Popen(
        cmd,
        env=env,
        # Ключевой момент — не переопределяем stdout/stderr!
    )
    proc.wait()
    if proc.returncode != 0:
        print("== Ошибка тренировки! ==")
        sys.exit(proc.returncode)
    print("\n== Тренировка завершена успешно! ==")
    
def main():
    parser = argparse.ArgumentParser(description="Автозапуск тренировки Nerfstudio (nerfacto/splatfacto)")
    parser.add_argument("--model", required=True, choices=["nerfacto", "splatfacto"], help="Модель Nerfstudio")
    parser.add_argument("--data", required=True, help="Папка с датасетом Nerfstudio (transforms.json и изображения)")
    parser.add_argument('--extra', nargs=argparse.REMAINDER, help="Любые дополнительные параметры к ns-train <model>")
    args = parser.parse_args()

    run_training(args.model, args.data, args.extra if args.extra else [])

if __name__ == "__main__":
    main()
    