# who-are-you-like
Сервис, который определяет, на какую знаменитость вы похожи, используя нейросетевые эмбеддинги и поиск по векторной базе.

### Dataset
- IMDB-WIKI dataset
- более 10 тысяч личностей
### Frontend
- JS React
### Backend
- FastAPI
- SQLite
- Faiss
- Facenet_pytorch

## Запуск проекта
1. Скопируйте репозиторий на свое устройство
2. Установите один из датасетов
3. Распакуйте его в директорию проекта 
4. Перейдите в директорию проекта и выполните следующие команды:
```bash
docker compose build
docker compose up
```

## Dataset source:
```bibtex
@InProceedings{Rothe-ICCVW-2015,
  author = {Rasmus Rothe and Radu Timofte and Luc Van Gool},
  title = {DEX: Deep EXpectation of apparent age from a single image},
  booktitle = {IEEE International Conference on Computer Vision Workshops (ICCVW)},
  year = {2015},
  month = {December},
}
