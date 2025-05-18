import os
import sys
import glob
import argparse
import subprocess
from datetime import datetime

def find_latest_experiment(outputs_dir, project, model):
    # examples: outputs/test2/nerfacto/2025-05-17_194856/config.yml
    experiments_path = os.path.join(outputs_dir, project, model)
    if not os.path.exists(experiments_path):
        raise FileNotFoundError(f"Эксперименты не найдены: {experiments_path}")
    all_exps = glob.glob(os.path.join(experiments_path, '*/config.yml'))
    if not all_exps:
        raise FileNotFoundError(f'config.yml не найден в {experiments_path}')
    # сортируем по времени создания папки (или лексикографически по имени)
    all_exps.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_config = all_exps[0]
    return latest_config

def run_eval(config_path, output_json):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    cmd = ['ns-eval', '--load-config', config_path, '--output-path', output_json]
    print("Оценка модели Nerfstudio:")
    print(" ".join(cmd))
    res = subprocess.run(cmd, env=env, text=True)
    if res.returncode != 0:
        print("== Ошибка ns-eval! ==")
        sys.exit(res.returncode)
    print(f"Готово! Метрики сохранены в {output_json}")

def main():
    parser = argparse.ArgumentParser(description="Оценка (eval) Nerfstudio модели")
    parser.add_argument('--outputs-dir', default='outputs', help="Корневая папка с результатами обучения (outputs)")
    parser.add_argument('--project', required=True, help="Имя проекта/датасета (например test2)")
    parser.add_argument('--model', required=True, help="Модель (nerfacto или splatfacto)")
    parser.add_argument('--output-json', default=None, help="Путь для сохранения вывода метрик (по умолчанию возле config.yml)")
    args = parser.parse_args()

    config_path = find_latest_experiment(args.outputs_dir, args.project, args.model)
    output_json = args.output_json
    if not output_json:
        # По умолчанию кладём рядом c config.yml с суффиксом "metrics.json"
        output_json = os.path.join(os.path.dirname(config_path), "metrics.json")

    print(f"Будет использован config: {config_path}")
    run_eval(config_path, output_json)

if __name__ == '__main__':
    main()