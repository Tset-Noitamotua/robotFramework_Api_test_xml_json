[Installation on Windows]
	1. latest python 2.X (2.7.6), make sure path is D:\Python26
	2. download ez_setup for win7 64bit. https://pypi.python.org/pypi/setuptools#windows-7-or-graphical-install
           加python环境变量  
           python ez_install
           加easy_install.exe环境变量：path C:\Python27\Scripts
           cmd运行：easy_install virtualenv

	3. wxPython (must be 2.8.12.1)  ->  for install
           环境变量：
           C:\Python27\Lib\site-packages\wx-2.8-msw-unicode
           C:\Python27\Lib\site-packages\wx-2.8-msw-unicode\wxPython
           C:\Python27\Lib\site-packages\wx-2.8-msw-unicode\wx


	4. robotframework (Robot Framework 2.8.4)  https://code.google.com/p/robotframework/  https://pypi.python.org/pypi/robotframework   
	->  test if pybot installed:  (use cmd) pybot –version
           环境变量：
           pybot  C:\Python27\lib\site-packages\

	5. Robot Ride (RIDE 1.2.3 running on Python 2.7.6.)  
	->  test if Ride installed: (use cmd) ride.py, (note: ride.py sould be in \Python27\Scripts)

        6.requests模块下载，进入有setup.py的目录，执行：python setup.py install安装

[Post Install - Import]
	Resource.txt
	Libraries
	TestSuite.txt


