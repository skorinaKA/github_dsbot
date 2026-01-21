# Система управления 7-сегментным 4-х разрядным дисплеем с помощью discord-бота

В данной работе будет реализована система управления 7-сегментным 4-ех разрядного индикатора с помощью Discord.

### Для данной работы, необходимо:

OrangePi i96

7-сегментный 4-х разрядный индикатор

Преобразователь USB-TTL UART модуль CH340G

Провода, провод micro-usb для питания платы

Micro SD Card, не менее 10 класса скорости и не меньше 8Гб

### Подготовка

## 1. Установка discord-бота

Для управления дисплеем с помощью Discord, необходимо создать бота, с помощью которого мы будем передавать необходимые команды для управления дисплеем. 
Чтобы создать бота, перейдите на специальную страницу Discord для разработчиков: https://discord.com/developers/.

1. На вкладке Applications выберите New Application.

<img width="794" height="130" alt="image" src="https://github.com/user-attachments/assets/df753981-e691-479c-8696-be59ff9b5f12" />

2. Введите название будущего приложения и нажмите Create.

<img width="439" height="371" alt="image" src="https://github.com/user-attachments/assets/08c611a5-e575-434d-93b2-df66473d2c6d" />

3. Приложение создано. Перейдите не вкладку Bot и нажмите Add Bot, чтобы добавить нового бота

<img width="793" height="125" alt="image" src="https://github.com/user-attachments/assets/2318f38e-09d0-4dd9-be7d-046d8c1c41f1" />

4. Согласитесь добавить бота в ваше приложение

<img width="435" height="192" alt="image" src="https://github.com/user-attachments/assets/97cbc98f-bb2f-47ce-98cd-99ac1ecf6088" />

5. Бот создан. На вкладке Bot отобразится вся информация о нем. Тут можно изменить его имя, добавить изображение и скопировать токен бота. Этот токен понадобится вам для настройки модуля Discord.
Сохраните токен бота, чтобы при последующей настройке не возвращаться к этому шагу.

6. Перейдите в раздел Privileged Gateway Intents и включите галочки. Это необходимо, чтобы бот мог обрабатывать и писать сообщения. И сохраняем

<img width="665" height="284" alt="image" src="https://github.com/user-attachments/assets/5b670956-4e77-43d8-aa4a-9a04eb88a9d9" />

7. Теперь перейдите на вкладку OAuth2  — тут можно настроить разрешения и получить ссылку на вашего бота. В разделе SCOPES выберите bot, в BOT PERMISSIONS отметьте разрешения, которые хотите ему предоставить, в нашем случае — только отправка сообщений, поэтому выберите Send Message. После скопируйте автоматически сгенерированную Discord ссылку

<img width="786" height="476" alt="image" src="https://github.com/user-attachments/assets/5daabea4-a3eb-4e02-aaca-cd744881a272" />

8. Вставьте скопированную ссылку в адресную строку браузера и перейдите по ней — откроется окошко вашего приложения. Выберите ваш сервер в раскрывающемся списке и нажмите Continue.

<img width="326" height="306" alt="image" src="https://github.com/user-attachments/assets/ebb2e791-ee77-40ec-a66b-2f7ebb00bab7" />

9. Теперь вернитесь на ваш сервер. Бот оставил приветственное сообщение — значит, что он успешно добавлен и функционирует.

<img width="790" height="468" alt="image" src="https://github.com/user-attachments/assets/1eeb769c-8086-4599-9542-6a5345ff67a3" />

## 2. Необходимые компоненты и подготовка к запуску платы.

### Компонент	Требования и инструкции
1. Orange Pi
2. TF-карта	8 ГБ или больше; класс 10. Хорошим выбором являются фирменные TF-карты, которые гораздо надежнее
3. Адаптер питания	При аренде высококачественного адаптера питания 5 В / 2 А OTG можно использовать в качестве источника питания.
4. TTL к USB-кабелю	Поддержка входа в систему отладки.

Подготовьте SD-карту

Чтобы иметь возможность использовать Orange Pi в обычном режиме, вы должны сначала установить операционную систему на карту памяти. Следующие инструкции научат вас, как записать файл образа операционной системы на платформу Windows и Linux. На данный момент эта плата может поддерживать загрузку с SD-карты с дистрибутивами Android и Linux.

#### Запись изображения на SD-карту в Windows:

1. Загрузить инструменты для форматирования TF-карты, такие как TF Formatter, можно с https://www.sdcard.org/downloads/formatter_4/eula_windows/

2. Распакуйте загруженные файлы и запустите setup.exe

3. В настройках параметров установите для параметра тип формата значение быстрое форматирование. Опция настройки логического размера для открытия "(ВКЛ.)”

4. Убедитесь, что введенные коды TF-карт соответствуют выбранным кодам.

5. Нажмите кнопку "Форматировать".

6. Загрузите файл образа операционной системы со страницы загрузки, адрес страницы следующий: 
https://github.com/TheRemote/Legendary-OrangePi-i96/releases/download/1.36/Legendary_OrangePi_i96_debian_bullseye_server_v1.36.tar.xz

7. Разархивируйте загруженный файл

8. Щелкните правой кнопкой мыши загруженный файл, выберите "Разархивировать файл", чтобы записать изображение на карту памяти.
Я загружаю инструменты для записи образа, такие как Win32Diskimager,
http://sourceforge.net/projects/win32diskimager/files/Archive.

9. Выберите путь к файлу изображения, который был разархивирован.

10. Нажмите кнопку "Запись" и дождитесь записи изображения.

11. После того, как изображение будет записано, нажмите кнопку "Выход".

Сначала вам нужно создать приложение, затем в этом приложении создать бота и настроить для него разрешения, и только после этого — добавлять бота на сервер.

#### Запись изображения на SD-карту в Linux:
	
1) запускаем команду fdisk –l, чтобы убедиться, что TF диск есть.

2) Запустите umount /dev/ sdxx, чтобы удалить все разделы TF-карты.

3) Запустите команду sudo fdisk /dev/sdx. 

4) Запустите команду sudo mkfs.vfat /dev / sdx1 для форматирования раздела TF-карты, настроенного на последнем шаге, в формат FAT32.

5) Загрузите образ ОС со страницы загрузки:
https://github.com/TheRemote/Legendary-OrangePi-i96/releases/download/1.36/Legendary_OrangePi_i96_debian_bullseye_server_v1.36.tar.xz

6) Разархивируйте загруженный файл и щелкните его правой кнопкой мыши, выберите "Разархивировать файл"

7) Запишите изображение на TF-карту

8) Запустите команду umount /dev/ sdxx для удаления всех разделов на TF-карте

9) Выполните команду sudo dd bs=4M if=[path]/[imagename] of=/dev/sdx для записи файла изображения и ожидания его завершения. 

## 3. Запуск Orange Pi

Вставьте карту памяти с записанным изображением в гнездо для карты памяти

<img width="353" height="277" alt="image" src="https://github.com/user-attachments/assets/1e9a880d-0c88-44d2-baf0-5f10ebd9f334" />

Убедитесь, что тумблер отображается следующим образом при загрузке с SD-карты.

<img width="505" height="306" alt="image" src="https://github.com/user-attachments/assets/e3579598-8278-41be-9c89-9e24516fa1cc" />

Подключите кабель TTL, затем вы можете подключится к плате через Serial Port

<img width="544" height="399" alt="image" src="https://github.com/user-attachments/assets/b04a9453-b126-49b8-a52c-c6451edfca05" />

Скачать Putty для управления платой с компьютера https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe

Через диспетчер устройств находим название COM-порта который необходим для подключения

Заходим в Putty и устанавливаем Connection Type, Serial line, Speed, и нажимаем на Open

<img width="440" height="439" alt="image" src="https://github.com/user-attachments/assets/3be0d0ec-314e-4ddb-a7ef-08ee4a4fd1a6" />

После успешного подключения вводим логин: orangepi и пароль: orangepi


## 4. Настройка Orange Pi

После того, как вы использовали serial для входа в систему, ввели пароль, система предложит вам использовать инструмент orangepi_config для выполнения некоторых базовых настроек, включая настройку Wi-Fi. Вы можете использовать следующую команду в терминале:

```sudo orangepi_config```

<img width="646" height="302" alt="image" src="https://github.com/user-attachments/assets/b56c6900-40e4-4417-a60d-5c2594c28a99" />

> Выбираем Wi-Fi settings

Эта настройка включает в себя функции настройки статуса Wi-Fi, поиска Wi-Fi и подключения к точке доступа. Вы можете использовать этот метод для настройки Wi-Fi.

Установите правильный часовой пояс:

```sudo dpkg-reconfigure tzdata```

Время синхронизации:

```sudo ntpd -gq```

Установите правильный язык:

```sudo apt install locales -y && sudo dpkg-reconfigure locales```

Установите страну:

```sudo nano /etc/default/crda```

Добавьте свой двухбуквенный код страны (мой - Россия) в конец нижней строки (после знака равенства) с надписью REGDOMAIN =
Нажмите Ctrl + X, затем Y, чтобы сохранить файл.

Сначала нужно клонировать репозиторий OrangePi_Build:

```bash
git clone https://github.com/orangepi-xunlong/OrangePi_Build.git --depth=1
cd OrangePi_Build
./Build_OrangePi.sh
```

Выберите опцию "Orange Pi i96", которая создаст папку "OrangePiRDA".

Файлы в этом репозитории предназначены для замены стандартных файлов OrangePiRDA, которые создаются (в частности, в папке scripts). Вы просто копируете их поверх сгенерированной папки следующим образом:

```bash
cd ..
git clone https://github.com/TheRemote/Legendary-OrangePi-i96.git
cp -R Legendary-OrangePi-i96/OrangePiRDA/* OrangePiRDA/
```

## Этап 5. На данном этапе необходимо подключить дисплей к плате. 

Распиновка платы с помощью команды gpio readall

<img width="646" height="404" alt="image" src="https://github.com/user-attachments/assets/ac513307-cd74-4bbd-9b5f-d9935895d000" />

Подключим дисплей следующим образом:
	GND	- Physical 39
	VCC 	- Physical 37
	DIO 	- Physical 3
	CLK 	- Physical 2

## Этап 6. Установка 

```bash
sudo apt update
sudo apt-get install git gcc make
sudo apt install python3.9
pip install discord.py
pip install python-periphery 
pip install requests
pip install publicip 
git clone https://github.com/vsergeev/python-periphery.git
git clone https://github.com/nopnop2002/python-periphery-tm1637
```

## Этап 7. Тестирование устройства с помощью команд в Discord:

С помощью команды !dark IP выводится на дисплей локальный IP адрес

Команда !dark TIME выводит на дисплей время

Команда !disp SET num выводит на дисплей число, где num - любое число

Команда !test @User выводит на  дисплей id пользователя, где @User-это никнейм пользователя

Команда !show IP выводит на дисплей публичный IP-адрес бота
