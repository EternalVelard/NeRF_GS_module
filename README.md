# NeRF_GS_module
A module that uses NeRF and GS to generate a point cloud of three-dimensional objects and metrics for them.
## Используемые технологии  
Этот проект использует [Nerfstudio](https://github.com/nerfstudio-project/nerfstudio) (Apache 2.0 License).

# О модуле

Автоматизированный пайплайн для подготовки, тренировки и оценки 3D-сцен с помощью COLMAP и Nerfstudio (Nerfacto/Splatfacto).  
Поддерживает любую последовательность:  
- COLMAP (SfM/структура из движения),
- преобразование в формат Nerfstudio,
- запуск тренировки,
- Расчёт облака точек,
- автоматическую оценку и выгрузку метрик.

Подходит для Windows и Linux(рекомендовано).

---
## Установка и требования

> **Рекомендуется**: использовать отдельную venv-среду и Python 3.9–3.11.
### 1. Установка зависимостей Python
bash
python -m venv venv
venv\Scripts\activate         # или source venv/bin/activate на Linux/Mac
python -m pip install --upgrade pip.
### 2. Nerfstudio
Полную устоновку можно найти на https://docs.nerf.studio/quickstart/installation.html
### 3. Установка COLMAP (для этапа colmap):
- **Для Windows**: Скачайте [COLMAP](https://colmap.github.io/install.html).
- **Для Linux**: sudo apt install colmap
## Быстрый старт
### 1. Сложите фотографии сцены в папку:
Например images_dict/images_project1

### 2. Запускаем весь пайплайн одной командой:

python run_all_pipeline.py --images images_dict/images_project1 --workspace vase_flower --model nerfacto
--images — путь к папке с изображениями
--workspace vase_flower — имя будущей рабочей папки
--model — nerfacto или splatfacto

## Описание скриптов
- nerf_gs_pipeline.py - Запускает COLMAP, строит структуру из движения.
- convert_to_nerfstudio.py - Генерирует transforms.json и структуру для Nerfstudio.
- train_nerfstudio_model.py - Запускает обучение.
- evaluate_nerfstudio_model.py - Сохраняет метрики после обучения.
- export_pointcloud.py - Извлекает облако точек.
- run_all_pipeline.py - Mастер-скрипт. Управляет всей цепочкой, запускает остальные скрипты с нужными параметрами.

