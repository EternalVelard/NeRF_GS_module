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
- автоматическую оценку и выгрузку метрик.

Подходит для Windows и Linux(рекомендовано).

---
## Установка и требования

> **Рекомендуется**: использовать отдельную venv-среду и Python 3.9–3.11.

### 1. Установка зависимостей Python
```bash
python -m venv venv
venv\Scripts\activate         # или source venv/bin/activate на Linux/Mac
python -m pip install --upgrade pip

# Nerfstudio, rich
pip install nerfstudio
pip install rich
### 2. Установка COLMAP (для этапа colmap):
Для Windows: Скачайте https://colmap.github.io/install.html.
Для Linux: sudo apt install colmap
Добавьте COLMAP в PATH или укажите путь в скриптах.

## Структура репозитория
NerfstudioPipeline/
    README.md
    nerf_gs_pipeline.py             # COLMAP и подготовка
    convert_to_nerfstudio.py        # Преобразование датасета под Nerfstudio
    train_nerfstudio_model.py       # Запуск тренировки Nerfacto/Splatfacto
    evaluate_nerfstudio_model.py    # Оценка модели и сохранение метрик
    run_all_pipeline.py             # Мастер-скрипт для всего пайплайна
    images_dict/                    # &lt;- Хранилище исходных фотоснимков
    &lt;ваши рабочие проекты...&gt;
## Быстрый старт
###1. Сложите фотографии сцены в папку:
Например images_dict/images_project1

###2. Запускаем весь пайплайн одной командой:

python run_all_pipeline.py --images images_dict/images_project1 --workspace vase_flower --model nerfacto
--images — путь к папке с изображениями
--workspace vase_flower — имя будущей рабочей папки
--model — nerfacto или splatfacto

##Описание скриптов
nerf_gs_pipeline.py
Запускает COLMAP, строит структуру из движения.
convert_to_nerfstudio.py
Генерирует transforms.json и структуру для Nerfstudio.
train_nerfstudio_model.py
Запускает обучение.
evaluate_nerfstudio_model.py
Сохраняет метрики после обучения.
run_all_pipeline.py
Mастер-скрипт. Управляет всей цепочкой, запускает остальные скрипты с нужными параметрами.

