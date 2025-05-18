import argparse
import os
import subprocess
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Экспорт облака точек из обученной модели Nerfstudio.')
    parser.add_argument('--config', type=str, required=False,
                        help='Путь к config.yml (если известен).')
    parser.add_argument('--outputs-dir', type=Path, default=Path('outputs'),
                        help='Папка с результатами Nerfstudio (по умолчанию outputs)')
    parser.add_argument('--project', type=str, required=False,
                        help='Название проекта (например, vase_flower)')
    parser.add_argument('--model', type=str, default='nerfacto',
                        help='Модель (nerfacto, splatfacto, ...), по умолчанию nerfacto')
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='Папка для сохранения экспортированного облака точек')
    return parser.parse_args()

def find_latest_config(outputs_dir, project, model):
    try:
        model_dir = outputs_dir / project / model
        exps = [p for p in model_dir.iterdir() if p.is_dir()]
        latest = max(exps, key=os.path.getmtime)
        config_path = latest / 'config.yml'
        if not config_path.exists():
            raise RuntimeError('config.yml не найден!')
        return config_path
    except Exception as e:
        print(f'Ошибка поиска config.yml: {e}')
        sys.exit(1)

def export_pointcloud(config_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ns-export", "pointcloud",
        "--load-config", str(config_path),
        "--output-dir", str(output_dir),
        "--normal-method", "open3d"
    ]
    print(f'Выполняется команда: {" ".join(cmd)}')
    process = subprocess.run(cmd)
    if process.returncode != 0:
        print("Ошибка экспорта облака точек!")
        sys.exit(process.returncode)
    print("\nГотово!")

def main():
    args = parse_args()

    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f'Config.yml не найден по пути {config_path}')
            sys.exit(1)
    elif args.project:
        config_path = find_latest_config(args.outputs_dir, args.project, args.model)
    else:
        print('Укажите либо --config, либо --project (и опционально --outputs-dir и --model)')
        sys.exit(1)

    export_pointcloud(config_path, args.output_dir)

if __name__ == "__main__":
    main()