Система «свой-чужой».  

## Техническое задание
1. Загрузили через страничку фото "свой", на выходе получили сетку обученную под распознание данного экземпляра фото
2. Перенесли обученную сетку на "свое железо" , без доступа в интернет, через web-камеру (желательно любую) система дает ответ свой\чужой в виде текста в локальный текстовый файл
3. При возможности подключения "своего железа" к интернету - текст отправляется в Телеграм-бот 
4. Скорость распознания на "стандартном" железе (видеокарта до 4gb, 2014-2017гг) до 1мс (будет круто)

## Структура проекта
### Recognition
Рапсознаёт изображение конкретного человеческого лица.  
#### Варианты библиотек
| № | Библиотека | Сокращенное название | Описание |
| ----- | ----- | ----- | ----- |
| 1. | face_recognition | fr | Переводит лица в вектора и сравнивает их. Скорость около одного кадра в секунду. |
| 2. | cv2 | cv | Тренирует LBPHFaceRecognizer. Работает быстро. |
| 3. | keras + tensorflow | net | Учится долго, определяет медленно и плохо. Большой расход вычислительной мощности. |

### Server
Представляет собой сервер, на который загружаются обучающие фото и выгружаются данные.
### Telegram
Telegram-бот, отправлющий сообщения «свой» или «чужой».

## Установка
+ Работает под `Python 3.8` (другие версии не проверялись), можно скачать [отсюда](https://www.python.org/downloads/).
+ Установить библиотеки согласно `requirements.txt`.
+ Если не удалось установить `dlib`, то можете воспользоваться тем, что находится в папке `lib` проекта.
Для этого скачайте себе эти файлы и из папки с ними запустите `pip38 install dlib-19.19.0-cp38-cp38-win_amd64.whl`
или `pip37 install dlib-19.19.0-cp37-cp37m-win_amd64.whl` (версия 3.7 не проверялась).

