# InfyCPU 1.5

InfyCPU Emulator is a custom, toy CPU Emulator. It has a basic ISA and has a screen. The screen is controlled by the Graphical Processor meanwhile other stuff like memory, registers, arithmetics are controlled by the normal Processor. You can adjust the ROM size, RAM size, emulated screen size and window size. A few examples of programs are included in the Programs\Examples folder.

## How to install

First you have to install Python 3 and Pygame. You can install pygame using this command:
```bash
pip install pygame
```
or if you have a newer version of python:
```bash
pip install pygame-ce
```

Next, install the repo by either downloading the ZIP file, or cloning it:
```bash
git clone https://github.com/Arghimaq/InfyCPU-1.5
```

## How to use it
### Programming

To write a program, you have to first write it in a .iasm file, which stands for Infy Assembly. If you're planning to share it, its recommended to specify the required sizes for the program in comments.
See Programming.md to see the ISA and a tutorial how to program in more detail.
After that, save it and run:

```bash
python Processor.py
```
It will open up a filedialog. Choose your .iasm program and it will run it.

#### Known problems

Choosing an .iexe file wont work for some reason. Leave it alone

### Settings

Some programs use different settings, so to adapt your settings to others' or your programs, run:

```bash
python Settings.py
```
It will open a graphical interface where you can change the RAM and ROM sizes and Screen and Window widths and lengths. It has some constraints so you can manually change it in settings.json

### Running someone else's program

If you want to run someone else's program, look inside the .iasm file and look for the recommended sizes in comments. If it is not specified, you can ask the creator of the program. After looking, enter the sizes in settings.json or Settings.py, and run it with Processor.py

## Made something?

If you have made a program, you can share it in Github Discussions in the Show and tell category. I'd love to see others' creations!

## Notes

If you want to look at an example to know how to program, Platformer.iasm is the most relevant one. It uses labels for loops.
