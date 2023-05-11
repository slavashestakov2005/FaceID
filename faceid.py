from recognition.capture import *
from server.facefolder import FaceFolder
from recognition.videostream import capture_stream_cv
from recognition.cv import CVModel
from recognition.detector import Detector
from tlg.client import send_parse


data = [
    'Добро пожаловать в систему распознавания лиц!',
    'Давайте познакомимся, как Вас зовут?',
    'Ваше имя: ',
    'Вот шутник, ввёл пустое имя. Давайте ещё раз :)',
    'Приятно познакомиться, {}!',
    'Давайте запишем Ваше лицо, это займёт 30 секунд.',
    'Вам нужно всё время держать лицо на одинаковом растоянии от камеры.',
    'И показать все стороны своего лица в камеру.',
    'Можете показывать язык, пытаться надеть шапку и всё, что придумаете :)',
    'Если камера выделяет Ваше лицо синей рамочкой, значит она Вас определила, как человека.',
    'Ну что ж, начнём.',
    'Поздравляем, вы справились.',
    'Итого собрано {} фото.',
    'Все они будут использованы для обучения.',
    'Но для обучения нам понадобится только {} из них.'.format(Config.IMAGES_COUNT),
    'Начинаем обучение.',
    'Это займёт не больше 30 секунд...',
    'Поздравляем Вас, мы смогли обучиться!',
    'Теперь сможем и поиграть :)',
    'Правила простые:',
    '1. На всё игру у Вас есть 1 минута, в течении которой Вас будет снимать камера.',
    '2. Нельзя отодвигаться от камеры или предвигаться к ней.',
    '3. Зелёный квадрат означает, что Вас распознали, красный - что не распознали.',
    '4. Ваша задача сделать так, чтобы Вас не распознали на хотя бы 20% кадров.',
    '5. «Коэффициент доверия» это то, на сколько Вы похожи на себя. Чем меньше - тем лучше.',
    '6. Если Вы выиграете, то получите приз.',
    'Если готовы играть, то нажмите Enter.',
    'Я Вас ничем не удивлю, если скажу, что согласно программе Вы «{}».',
    'А это значит, что Вы {}играли.',
    'Не растраивайтесь, в другой раз обязательно выиграете!',
    'Можете забрать свой приз у организатора (ему уже пришлом сообщение в Telegram :))',
    'С вами было приятно играть.',
    'Если хотите, то можете попросить запись этой игры у организатора.',
    'До свидания, приходите играть ещё!'
]
message_template = 'Игрок: {}\nID: {}\n Результат: {}'


def write(text):
    for line in text:
        input(line + ' ')


folder = FaceFolder()
folder.create()
write(data[0:1])
print(data[1])
name = ''
while not name:
    name = input(data[2])
    if name:
        break
    print(data[3])
write([data[4].format(name), data[5]])
write(data[6:11])
images_count = capture_data(folder.image(), folder.video() + '/train.avi')
write([*data[11:12], data[12].format(images_count)])
write([data[13 + int(images_count > Config.IMAGES_COUNT)], *data[15:17]])
model = CVModel()
model.name = name
model.train(*Detector().get_data(folder.dir(), folder.temp()))
model.write(folder.dir())
send_parse(model.face)
write(data[17:27])
result = capture_stream_cv(folder.dir(), folder.video() + '/test.avi', folder.dir() + '/result.png')
write([data[27].format('свой' if result else 'чужой'), data[28].format('про' if result else 'вы')])
write([data[30 - int(result)], *data[31:34]])
