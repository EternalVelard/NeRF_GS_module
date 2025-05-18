import subprocess
import sys
import os
import argparse

def run(script_args, step_name):
    print(f"\n{'='*20} {step_name} {'='*20}\n")
    result = subprocess.run(script_args)
    if result.returncode != 0:
        print(f"Ошибка на этапе {step_name}. Останавливаю выполнение.")
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Мастер-пайплайн NeRF/Nerfstudio")
    parser.add_argument('--images', required=True, help='Путь к папке с изображениями')
    parser.add_argument('--workspace', required=True, help='Рабочая папка (outputs, colmap, и др.)')
    parser.add_argument('--model', required=True, choices=['nerfacto', 'splatfacto'], help='Модель для обучения')
    parser.add_argument('--max-iterations', type=int, default=20000, help='Максимальное число итераций обучения')
    parser.add_argument('--skip-colmap', action='store_true', help='Пропустить этап COLMAP (если уже построена папка colmap)')
    parser.add_argument('--skip-convert', action='store_true', help='Пропустить этап конвертации в Nerfstudio')
    parser.add_argument('--skip-train', action='store_true', help='Пропустить этап обучения')
    parser.add_argument('--skip-eval', action='store_true', help='Пропустить этап оценки')
    parser.add_argument('--dataset-dir', default=None, help='Где будет/лежит nerfstudio-датасет (по умолчанию <workspace>/nerfstudio_dataset)')
    args = parser.parse_args()

    # Пути
    images_dir = os.path.abspath(args.images)
    workspace = os.path.abspath(args.workspace)
    ns_dataset = args.dataset_dir or os.path.join(workspace)
    project_name = os.path.basename(os.path.normpath(ns_dataset))
    model = args.model

    # 1. COLMAP этап (если не пропущен)
    if not args.skip_colmap:
        run([
            sys.executable, "nerf_gs_pipeline.py", 
            "--images", images_dir, 
            "--workspace", workspace
        ], "COLMAP")

    # 2. Конвертация в Nerfstudio (если не пропущен)
    if not args.skip_convert:
        run([
            sys.executable, "convert_to_nerfstudio.py",
            "--images", images_dir,
            "--output-dir", ns_dataset
        ], "Конвертация в Nerfstudio")

    # 3. Тренировка модели (если не пропущен)
    if not args.skip_train:
        run([
            sys.executable, "train_nerfstudio_model.py",
            "--model", model,
            "--data", ns_dataset,
            "--extra", f"--max-num-iterations={args.max_iterations}"
        ], "Тренировка Nerfstudio")

    # 4. Оценка модели (если не пропущен)
    if not args.skip_eval:
        run([
            sys.executable, "evaluate_nerfstudio_model.py",
            "--outputs-dir", os.path.join(workspace, "outputs"),
            "--project", project_name,
            "--model", model
        ], "Оценка модели")

    print("\n========== Всё выполнено успешно! ==========")

if __name__ == "__main__":
    main()