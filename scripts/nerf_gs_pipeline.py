import os
import argparse
import subprocess
import sys

def run_colmap(images_path, workspace_path):
    """Запускает COLMAP и собирает colmap/sparse/0 + database.db + project.ini"""

    # Структура каталогов
    colmap_dir = os.path.join(workspace_path, "colmap")
    sparse0_dir = os.path.join(colmap_dir, "sparse", "0")
    database_path = os.path.join(colmap_dir, "database.db")

    os.makedirs(sparse0_dir, exist_ok=True)

    # 1. Feature extraction
    print("== COLMAP: Feature extraction ==")
    subprocess.run([
        "colmap", "feature_extractor",
        "--database_path", database_path,
        "--image_path", images_path
    ], check=True)

    # 2. Feature matching
    print("== COLMAP: Feature matching ==")
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", database_path
    ], check=True)

    # 3. Mapper (Sparse reconstruction)
    print("== COLMAP: Mapping ==")
    subprocess.run([
        "colmap", "mapper",
        "--database_path", database_path,
        "--image_path", images_path,
        "--output_path", os.path.join(colmap_dir, "sparse")
    ], check=True)

    # 4. project.ini внутрь sparse/0
    project_ini_path = os.path.join(sparse0_dir, "project.ini")
    with open(project_ini_path, 'w', encoding='utf-8') as f:
        f.write('[export]\nformat=bin\n')

    # 5. Проверим существование всех файлов
    print("\n== Проверка результатов ==")
    filenames = ["cameras.bin", "images.bin", "points3D.bin", "project.ini"]
    for fname in filenames:
        fpath = os.path.join(sparse0_dir, fname)
        print(f"{fname}: {'OK' if os.path.exists(fpath) else 'ОТСУТСТВУЕТ!'}")
    print(f"database.db: {'OK' if os.path.exists(database_path) else 'ОТСУТСТВУЕТ!'}")

    return colmap_dir

def main():
    parser = argparse.ArgumentParser(description='NeRF/GS preproc: COLMAP этап')
    parser.add_argument('--images', required=True, help='Путь к папке с изображениями')
    parser.add_argument('--workspace', required=True, help='Рабочая директория (будет создан /colmap внутри)')

    args = parser.parse_args()
    images_path = os.path.abspath(args.images)
    workspace_path = os.path.abspath(args.workspace)

    if not os.path.isdir(images_path):
        print(f"Папка с изображениями не найдена: {images_path}")
        sys.exit(1)

    print(f"Изображения: {images_path}")
    print(f"Рабочая папка: {workspace_path}")

    try:
        colmap_dir = run_colmap(images_path, workspace_path)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка COLMAP: {e}")
        sys.exit(2)

    print("\nГотово! Всё необходимое для Nerfstudio находится в:")
    print(f"{os.path.abspath(colmap_dir)}")

if __name__ == '__main__':
    main()