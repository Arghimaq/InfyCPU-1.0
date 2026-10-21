### Highlights

Added stack, call, ret, removed settings.py and fixed the `.iexe` bug

# InfyCPU 2

<img width="200" height="200" alt="python_uac8REw7OP" src="https://github.com/user-attachments/assets/1eacf84d-ccbd-45db-9de8-36d0369bcf0d" />
Flying Pixel.iasm, ran by InfyCPU. Required size: 32x32. Minimum ROM size: 32



InfyCPU Emulator is a custom, toy CPU Emulator. It has a basic ISA and has a screen. The screen is controlled by the Graphical Processor meanwhile other stuff like memory, registers, arithmetics are controlled by the normal Processor. You can adjust the ROM size, RAM size, emulated screen size and window size. A few examples of programs are included in the [Examples](Programs/Examples) folder.

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
git clone https://github.com/Arghimaq/InfyCPU-2
```

## How to use it
### Programming

To write a program, you have to first write it in a `.iasm` file, which stands for Infy Assembly. If you're planning to share it, its recommended to specify the required sizes for the program in comments.
See [Programming.md](docs/Programming.md) to see the ISA and a tutorial how to program in more detail.
After that, save it and use 2 methods to run it. 1st is the file dialog method:

```bash
python Processor.py
```
It will open up a file dialog. Choose your `.iasm` program and it will compile and run it.

The second method is compiling it seperately and then selecting it as an `.iexe` file in the filedialog:

```
python Compiler.py my_program.iasm
```
A new `.iexe` file will generate near to it.

#### Notes

The `.iexe` bug has been fixed!

### Settings

Some programs use different settings, so to adapt your settings to others' or your programs, edit `settings.json`.
You'll see something like:
```json
{
    "ram_size": 128,
    "rom_size": 128,
    "stack_size": 64,
    "window_width": 640,
    "window_length": 480,
    "screen_width": 64,
    "screen_length": 48
}
```

### Running someone else's program

If you want to run someone else's program, look inside the `.iasm` file and look for the recommended sizes in comments. If it is not specified, you can ask the creator of the program. After looking, enter the sizes in `settings.json`, and run it with `Processor.py`

## Made something?

If you have made a program, you can share it in Github Discussions in the Show and tell category. I'd love to see others' creations!

<img width="320" height="240" alt="python_3RG2Bh3tYf" src="https://github.com/user-attachments/assets/726d873a-d2df-46c5-86a6-e464425e29b3" />
Platformer.iasm, ran by InfyCPU. Required size: 64x48. Minimum ROM size: 200

## Notes

If you want to look at an example to know how to program, `Platformer.iasm` is the most relevant one. It uses labels for loops.
