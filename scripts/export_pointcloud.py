import argparse
import os
import subprocess
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Экспорт данных из обученной модели Nerfstudio.')
    parser.add_argument('--config', type=str, required=False,
                        help='Путь к config.yml (если известен).')
    parser.add_argument('--outputs-dir', type=Path, default=Path('outputs'),
                        help='Папка с результатами Nerfstudio (по умолчанию outputs)')
    parser.add_argument('--project', type=str, required=False,
                        help='Название проекта (например, vase_flower)')
    parser.add_argument('--model', type=str, required=True,
                        choices=['nerfacto', 'splatfacto'],
                        help='nerfacto (tsdf) или splatfacto (gaussian-splat)')
    parser.add_argument('--output-dir', type=Path, required=True,
                        help='Папка для сохранения результата экспорта')
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

def export_artifact(config_path, output_dir, model):
    os.makedirs(output_dir, exist_ok=True)
    if model == "nerfacto":
        export_cmd = ["ns-export", "tsdf", "--load-config", str(config_path), "--output-dir", str(output_dir)]
    elif model == "splatfacto":
        export_cmd = ["ns-export", "gaussian-splat", "--load-config", str(config_path), "--output-dir", str(output_dir)]
    else:
        print("Неизвестная модель, экспорт невозможен!")
        sys.exit(2)
    print(f'Выполняется команда: {" ".join(export_cmd)}')
    process = subprocess.run(export_cmd)
    if process.returncode != 0:
        print("Ошибка экспорта результата!")
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

    export_artifact(config_path, args.output_dir, args.model)

if __name__ == "__main__":
    main()
