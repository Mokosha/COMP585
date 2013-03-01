COMP585
=======

Game for final project of COMP585

---

Requirements:
-------------
* [Python 2.7](http://www.python.org/download/releases/2.7/)
* [PyGame 1.9](http://pygame.org/download.shtml) (Make sure you get the one for Python 2.7)

---

Installation:
-------------

#### Windows 7: ####
1. Download and install [Git](http://msysgit.github.com/). I recommend Git for Windows, but Msys Git works just as well.
2. Open a git shell and [setup an SSH key](https://help.github.com/articles/generating-ssh-keys).
2. In the same git shell, create a clone of COMP 585 Project repository: 
```

        $ mkdir COMP585
        $ cd COMP585
        $ git clone git@github.com:Mokosha/COMP585.git Final
````
3. Assuming that you have Python 2.7 and PyGame 1.9 installed from the links above, you can do one of the following two options:

* Add Python to your system path by clicking on the Start Menu and right clicking on 'Computer' and selecting 'Properties'.
Click 'Advanced System Properties' and then 'Environment Variables'. Under System Variables, scroll down until you reach the
PATH environment variable and press 'edit'. From there you can add the string 'C:\Python27\;' to the beginning of the value
and save everything. Now if you open a command prompt (click the Start Menu, type 'cmd' and hit Enter), you should be able to
run the command 'python'. Navigate to the COMP 585 repository via the 'cd' command and execute 'python main.py' from the src directory.

* Open up the Python Interpreter from the Start Menu. You should have a prompt waiting with '>>>'. Run the following commands:
```python
>>> import os
>>> os.chdir("C:\\Path\\To\\COMP585\\Final\\src") # Note, we must escape the front slashes because they are special characters.
>>> execfile("main.py")
````

#### OS X: ####
1. Download and install [Git](http://code.google.com/p/git-osx-installer/)
2. Open up the Terminal application: Click on the desktop, and then press Command-Shift-U. Scroll down and double-click on the terminal app.
2. [Setup an SSH key](https://help.github.com/articles/generating-ssh-keys).
3. Now cloning the repository is easy:
```

        $ cd ~
        $ mkdir COMP585
        $ cd COMP585
        $ git clone git@github.com:Mokosha/COMP585.git Final
````
4. Assuming you have Python 2.7 and PyGame 1.9 installed, now you can play the game:
```

        $ cd ~/COMP585/Final
        $ python src/main.py
````
