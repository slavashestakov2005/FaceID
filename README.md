Система «свой-чужой».  
[Презентация](https://docs.google.com/presentation/d/1TZBpWhKmof9FLp4XzRLFW6GwD1Fmsk-J/edit?usp=sharing&ouid=104378135732805691471&rtpof=true&sd=true) с предзащиты.  
[Календарный план](https://docs.google.com/spreadsheets/d/1N6Cu9KpMLCV-4HiQI2XPntv9Kqjaka5IoL8DQEBPFJ0/edit?usp=sharing).

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
| 3. | keras + tensorflow | fn | Учится долго, определяет медленно и плохо. Большой расход вычислительной мощности. |

### Server
Представляет собой сервер, на который загружаются обучающие фото и выгружаются данные.
### Telegram
Telegram-бот, отправлющий сообщения «свой» или «чужой».

## Оценка качества работы
### Формализация оценки
1. Взят открытый набор данных [отсюда](http://vis-www.cs.umass.edu/lfw/#download), его копия [здесь](https://drive.google.com/drive/folders/1CNlhu4Nc0SNAsVURhdqVsPXKjzJMYa8R?usp=sharing).
2. На каждом изображении учится модель; каждая модель проверяется на всех изображениях.
3. Подсчитывается общее число ошибок и их сумарный вес:
    + Истино «свой» и истино «чужой» — правильные предсказания.
    + Ложно «чужой» — не правильныльное предсказание, вес — 1.
    + Ложно «свой» — не правильное предсказание, вес — 10.
4. Результатом служат следующии метрики:
    + Ошибочность — <сумарный вес ошибок> / <количество тестов>.
    + Количество ложно «чужих».
    + Количество ложно «своих».

## Оценка качества работы OpenCV
### Близнецовый тест (`tests/cv-twins`)
1. Для оценивания качетва работы модели были взяты близнецы (назовём их A и B) и я (C).
2. Из [этих видео](https://drive.google.com/drive/folders/1sgXQaNVnnItobKVXmAkRPKBQVhQ3R-xk?usp=sharing) были изалечены фотографии лиц.
3. Далле эти лица случайно поделены на тестовую (15%) и тренировочную (85%) части. Распределение [здесь](https://drive.google.com/drive/folders/1tC4sC-Vmhz2E7BP6ASIQ5FSO6Lp7j2ZQ?usp=sharing).
4. Для A, B и C были обучены отдельные модели (по тренировочным частям).
5. Каждая модель была проверена на своей тестовой части; разные люди проверялись на полном наборе фото.
6. Все результаты есть в папке `tests/cv-twins` (в формате модель - фото).
7. Выводы:
    + Если модели показывают изображение «свой», то «коэффициент доверия» ниже 40, причём у близнецов показатель ниже.
    + Близнецы определяются с «коэффициентом доверия» около 75.
    + Не близнецы дают «коэффициент доверия» около 90.
8. Значит порог для «свой-чужой» должен быть примерно 60-70.
### Количественный тест (`tests/cv-count`)
1. Для оценивания качества работы было взято два [видео](https://drive.google.com/drive/folders/1p4yn2vvOJpPCBL-UU3u4SDHaAgUyAgLh?usp=sharing)
одного человека (меня): [тренировочное](https://drive.google.com/file/d/1sJB-r349A0ZBAsDdthbuYak3jwbiPcss/view?usp=sharing)
и [тестовое](https://drive.google.com/file/d/1O3XVtHe30C05H9QIM54lEncqxTWeN3-P/view?usp=sharing).
2. Из видео были извелечены фото и были сгенерированы случайные выборки разных размеров из тренировчного видео. Эти фото [здесь](https://drive.google.com/drive/folders/1ZRUeHLuM6G1OZ2b2jcMj740F85aboyKF?usp=sharing).
3. На каждой выборке тренировочных фото были обучены отдельные модели и протестированы на всех фото из тестового видео.
4. Полученные результаты в папке `tests/cv-count` (навзванием файла является число фото, на которых обучалась модель). 
5. Обобщения этих результатов в папке `tests/cv-count/results`.
6. Выводы:
    + Метрики (среднее арифметическое, медиана и диапазон «коэффициента доверия») практически перестают меняться после 200 фото.
    + После 250 фото распределение «коэффициента доверия» практически не меняется.
    + Среднее время обработки фото после 500 тренировочных фото растёт не принося пользы.
7. Итого:
    + Оптимальное количество тренировочных фото 200-250.
    + Можно установить «коэффициента доверия» по умолчанию равным 55 и проверять, что 65% из тестовых фото - подходят.
    + Можно установить «коэффициента доверия» по умолчанию равным 60 и проверять, что 80% из тестовых фото - подходят.
8. Заметим, что такой подбор параметров соотносится с предыдущим тестированием и будет давать верные предсказания.
### Формальная оценка (`tests/cv`)
1. Формальная оценка проводилась по описанию выше, все результаты в папке `tests/cv`.
2. «Коэффициента доверия» по умолчанию должен быть равным 50.
3. Тогда ошибочность будет 0.18, а это точность около 98.2%.
4. Для согласования с предыдущими тестами, нужно проверять, что 50% из тестовых фото - подходят.
5. Так «чужому» будет сложно притвориться «своих». Можно установить чуть более жесткую проверку, но тогда «своему» придётся изменять лицо не слишком сильно.

## Запуск
### Server
Файл `server.py` запускает сервер, получающий картинки и возвращающий распознаватель лиц.
### Client
Файл `client.py` запускает распознавание лиц по модели.
### Faceid
Файл `faceid.py` запускает игру с пользователем (пользователю нужно сделать вид, что он «чужой»). Сделано специально для
итогового мероприятия гимназии.

## Установка
+ Работает под `Python 3.8` (другие версии не проверялись), можно скачать [отсюда](https://www.python.org/downloads/).
+ Установить библиотеки согласно `requirements.txt`.
+ Если не удалось установить `dlib`, то можете воспользоваться тем, что находится в папке `lib` проекта.
Для этого скачайте себе эти файлы и из папки с ними запустите `pip38 install dlib-19.19.0-cp38-cp38-win_amd64.whl`
или `pip37 install dlib-19.19.0-cp37-cp37m-win_amd64.whl` (версия 3.7 не проверялась).

## Библиография
+ [Пример](https://habr.com/ru/company/netologyru/blog/434354/) с Face Recognition.
+ Ещё один [пример](https://pythonist.ru/raspoznavanie-licz-pri-pomoshhi-python-i-opencv/?ysclid=l2oyvdygyk).
+ [OpenCV и LBPHFaceRecognizer](https://robotos.in/uroki/obnaruzhenie-i-raspoznavanie-litsa-na-python).
+ Другой [пример](https://habr.com/ru/post/301096/).
+ [FaceNet](https://neurohive.io/ru/tutorial/raspoznavanie-lica-facenet/).
+ [Статья](https://habr.com/ru/company/ntechlab/blog/329412/) об оценке качества распознавания.

## Благодарности
Благодарю близнецов, принявших участие в тестировании системы. Имена не указываются без их согласия.
