import os
import argparse
import subprocess
import sys

def run(script_args, step_name):
    print(f"\n{'='*20} {step_name} {'='*20}\n")
    result = subprocess.run(script_args)
    if result.returncode != 0:
        print(f"Ошибка на этапе {step_name}. Останавливаю выполнение.")
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Мастер-пайплайн NeRF/Nerfstudio")
    parser.add_argument('--images', required=True, help='Путь к папке с изображениями')
    parser.add_argument('--workspace', required=True, help='Папка, куда будет положен датасет Nerfstudio, с тем же именем как проект')
    parser.add_argument('--model', required=True, choices=['nerfacto', 'splatfacto'], help='Модель для обучения')
    parser.add_argument('--max-iterations', type=int, default=20000, help='Максимальное число итераций обучения')
    parser.add_argument('--skip-colmap', action='store_true', help='Пропустить этап COLMAP')
    parser.add_argument('--skip-convert', action='store_true', help='Пропустить этап конвертации в Nerfstudio')
    parser.add_argument('--skip-train', action='store_true', help='Пропустить этап обучения')
    parser.add_argument('--skip-eval', action='store_true', help='Пропустить этап оценки')
    parser.add_argument('--skip-export', action='store_true', help='Пропустить экспорт облака точек')
    args = parser.parse_args()

    images_dir = os.path.abspath(args.images)
    workspace = os.path.abspath(args.workspace)
    dataset_dir = workspace
    project_name = os.path.basename(os.path.normpath(workspace))
    model = args.model

    # COLMAP
    if not args.skip_colmap:
        run([
            sys.executable, "nerf_gs_pipeline.py",
            "--images", images_dir,
            "--workspace", workspace
        ], "COLMAP")

    # Convert to Nerfstudio
    if not args.skip_convert:
        run([
            sys.executable, "convert_to_nerfstudio.py",
            "--images", images_dir,
            "--output-dir", dataset_dir
        ], "Конвертация в Nerfstudio")

    # Train
    if not args.skip_train:
        run([
            sys.executable, "train_nerfstudio_model.py",
            "--model", model,
            "--data", dataset_dir,
            "--extra", f"--max-num-iterations={args.max_iterations}"
        ], "Тренировка Nerfstudio")

    # Evaluate
    if not args.skip_eval:
        run([
            sys.executable, "evaluate_nerfstudio_model.py",
            "--outputs-dir", os.path.join("outputs"),
            "--project", project_name,
            "--model", model
        ], "Оценка модели")

    # Export pointcloud
    if not args.skip_export:
        # Здесь определяем папку exports/pcd/ в РАБОЧЕЙ директории (где был запущен скрипт)
        export_dir = os.path.abspath(os.path.join("exports", "pcd"))
        os.makedirs(export_dir, exist_ok=True)
        run([
            sys.executable, "export_pointcloud.py",
            "--project", project_name,
            "--model", model,
            "--output-dir", export_dir
        ], "Экспорт облака точек")

    print("\n========== Всё выполнено успешно! ==========")

if __name__ == "__main__":
    main()
    print("\n========== Всё выполнено успешно! ==========")

if __name__ == "__main__":
    main()
