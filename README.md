ShareSphere is a sharing system on your router which can be run on your desktop computer.

**On Unix-likes**<br>
In order to use it go to ShareSphere directory and run the following commands:
```bash
pip3 install flask && ./app.py
```

now you'll be given some IPs (Note: all your devices should be connected to one router
and if you don't have one then you can connect all your devices to your phone's hotspot and use hotspot as a router).

Choose the on that is not 127.0.0.1 (because this IP is only accessible to your computer locally) and open it in any device connected to the same network.

for setting the folder to be shared you should pass it ```-d``` or ```--directory```argument for example:

```bash
python3 app.py -d ~/Music
```

if you dont pass the argument ```-d``` it will set to ```~/Downloads```

**if you want to use ShareSphere as a command line tool which has a name do as per:**
```bash
sudo ln -s [source_folder]/app.py /usr/local/bin/sharesphere
```


.کره اشتراک گذاری یک سیستم اشتراک گذاری روی روتر شماست که میتونه روی کامپیوتر های شخصی اجرا بشه

**سیستم های بر پایه یونیکس**<br>
برای احرای راه اندازی و استفاده از این برنامه دستورات زیر را پیروی کنید. 

```bash
pip3 install flask && ./app.py
```
حال شما یک یا چند ادرس شبکه دریافت میکنید دقت کنید که همه دستگاه های شما باید به روتر یا مودم متصل باشد اگر مودم ندارید از هاتسپات تلفن همراه استفاده کنید و تمام دستگاه ها را به ان متصل کنید
ایپی 127.0.0.1 فقط روی کامپیوتر شما اجرا میشود پس حواستان باشد برای اتصال به شبکه روی گوشی حتما از ایپی های دیگر که به شما نمایش داده میشود استفاده کنید
برای مثال 192.168.1.112:5000 برای اتصال در دیگر دستگاه مناسب است
برای تنظیم پوشه مورد نظر از ارگومان های ```-d``` / ```--directory``` استفاده کنید

مثال
```bash
python3 app.py -d ~/Music
```
**اگر مشتاق استفاده از این برنامه بصورت ابزار دستوری استفاده کنید که نامی بر خود دارد دستور زیر را اجرا کنید:**
```bash
sudo ln -s [source_folder]/app.py /usr/local/bin/sharesphere
```