# InfyCPU-1.0

InfyCPU-1.0 is a small, playful custom CPU and GPU emulator written in Python. It is designed for learning, experimentation, and sharing little programs with other people for fun.

The project combines:
- a custom instruction set
- a tiny ROM-based execution model
- a software-rendered screen and VRAM system
- JSON-based configuration for emulator sizing and display settings
- a simple compiler layer that turns readable assembly-like text into executable ROM values

This repository is intentionally lightweight and easy to tinker with. If you like building toy machines, writing assembly-like programs, or experimenting with screen rendering, this is a good project to learn from.

## Features

- Custom CPU-style instruction set
- RAM and ROM emulation
- Register-based execution model
- Simple GPU/VRAM display pipeline
- Keyboard input support through pygame event handling
- Configurable emulator memory and display sizes via settings.json
- ROM compiler that strips comments and converts text instructions into numeric instructions
- Example ROM files included for experimentation

## Project structure

- `Main.py` – entry point and module loader
- `Processor.py` – CPU execution loop, instruction handling, RAM/ROM logic, and GPU update cycle
- `Compiler.py` – converts readable instruction text into numeric ROM data
- `GraphicalProcessor.py` – screen setup, drawing, scaling, and event handling
- `Settings.py` – GUI-based configuration editor for emulator settings
- `settings.json` – default emulator configuration
- `ROM.txt` – generated compiled ROM used by the emulator
- `ROMS/Examples/Example1.txt` – example ROM program
- `LICENSE` – project license

## Requirements

This project uses Python and requires the following packages:

- Python 3
- pygame
- tkinter (built in with most Python installs on desktop systems)

Install pygame with:

```bash
pip install pygame
```

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/Arghimaq/InfyCPU-1.0.git
cd InfyCPU-1.0
```

### 2. Configure emulator settings

You can edit `settings.json` manually or open the GUI editor:

```bash
python Settings.py
```

This allows you to adjust:
- RAM size
- ROM size
- window dimensions
- screen dimensions

When saved, it writes a new `settings.json` file.

### 3. Create or edit a ROM program

The source ROM format is text-based and uses a simple assembly-like syntax.

Example:

```text
LDI 0 0
ADDI 1 5
JZ 84 0
VST 2 6
HALT
```

Comments can be added with `;`:

```text
LDI 0 0 ; set register 0 to 0
ADDI 1 5 ; set register 1 to 5
```

The compiler strips everything after `;` and splits on whitespace.

### 4. Compile the ROM

Run:

```bash
python Compiler.py
```

A file dialog will open so you can select your ROM `.txt` file. The compiler then writes the result to `ROM.txt`.

### 5. Run the emulator

```bash
python Processor.py
```

This loads `ROM.txt`, executes the program, updates the virtual GPU display, and runs until the machine halts or the window is closed.

## Custom instruction set

The custom ISA used by the emulator is defined in `Compiler.py`. The instruction names include:

### Memory
- `ST` – store register value into RAM
- `LD` – load RAM value into a register
- `STI` – store immediate value into RAM
- `LDI` – load immediate value into a register
- `SWP` – swap register values
- `COP` – copy one register into another

### ALU
- `ADD`
- `SUB`
- `MUL`
- `DIV`
- `ADDI`
- `SUBI`
- `MULI`
- `DIVI`

### Comparisons
- `CMPei` – compare equal to immediate value
- `CMPgi` – compare greater than immediate value
- `CMPli` – compare less than immediate value

### Control flow
- `JMP` – unconditional jump
- `JZ` – jump based on zero flag
- `JINP` – jump based on input flag
- `JCMP` – jump based on compare flag

### Video / graphics
- `VST` – store register value into VRAM
- `VSTI` – store immediate value into VRAM
- `BLTI` – calculate a blitted address from immediate coordinates
- `BLT` – calculate a blitted address from register coordinates
- `BLTR` – move calculated blitter value into a register

### Input / output
- `INP` – poll keyboard input

### Special / debug
- `HALT` – stop execution
- `PRINT` – print a register value

## Instruction format

Most instructions follow this pattern:

```text
OPCODE operand1 operand2
```

Example:

```text
LDI 0 5
ADD 0 1
JMP 20 0
VST 2 6
```

Commands are treated as a 3-slot instruction stream, and the compiler writes each value into a line in `ROM.txt`.

## Finding ROM addresses (how to locate a word in ROM.txt)

When the compiler converts your text ROM into `ROM.txt` it writes each instruction as three numeric values on separate lines (opcode, operand1, operand2). To help you find the ROM file line (or numeric index) that corresponds to a particular word in your source text ROM, use this formula.

Formula (0-based ROM index):

ROM_index = (source_line_number - 1) * 3 + operand_offset

- source_line_number: the line number in your text ROM (1-based, as shown by most editors)
- operand_offset: 0 for the opcode, 1 for the first operand, 2 for the second operand

If you prefer a 1-based ROM line number (human-friendly line number in ROM.txt):

ROM_line_number = ROM_index + 1 = (source_line_number - 1) * 3 + operand_offset + 1

Quick shorthand:
- Opcode slot (1-based ROM line): (line - 1) * 3 + 0
- Operand1 slot (1-based ROM line): (line - 1) * 3 + 1
- Operand2 slot (1-based ROM line): (line - 1) * 3 + 2

Example

Source ROM (text file):

1 LDI 0 5
2 ADD 0 1
3 JMP 20 0

Say you want the ROM address of the value `1` that appears as the second operand on line 2 (`ADD 0 1`).

- source_line_number = 2
- operand_offset for second operand = 2 (0-based)

ROM_index = (2 - 1) * 3 + 2 = 1 * 3 + 2 = 5 (this is a 0-based index into ROM.txt)

To get the human-readable ROM line number in ROM.txt (1-based):
ROM_line_number = ROM_index + 1 = 6

So the `1` will appear on line 6 of `ROM.txt` (counting lines starting at 1). If you open `ROM.txt` you can jump to that line to see or edit the compiled value.

Notes

- Many editors display line numbers starting at 1. Use the formula above with that number and you'll get the correct ROM location.
- This mapping assumes the compiler always writes exactly three numeric slots per source instruction; if you change the compiler behavior, update the formula accordingly.

## Example programs

The repository includes a sample program in:

- `ROMS/Examples/Example1.txt`

This example demonstrates a simple graphics-style loop using registers, blitting, and VRAM updates. It is a good place to start if you want to understand how the emulator works.

## How the emulator works

The execution model is intentionally simple:

1. The compiler reads a text ROM and produces numeric instructions.
2. `Processor.py` loads the compiled ROM into memory.
3. The CPU fetches instructions in groups of 3 values.
4. Depending on the opcode, it updates registers, RAM, VRAM, flags, or control flow.
5. The GPU continuously redraws the virtual screen.
6. Execution continues until a halt condition or window-close event occurs.

## Notes and limitations

This project is experimental and educational. Some parts are intentionally minimal and are best treated as a toy emulator rather than a production-grade virtual machine.

A few examples:
- the project does not have a large or polished standard library
- the ROM format is simple and custom
- the execution model is intentionally compact and easy to study
- some code paths are straightforward experimental implementations rather than heavily optimized production code

## Contributing / sharing programs

This project is meant to be fun and community-driven. If you build a cool program, especially a visual demo or interesting ROM experiment, you are encouraged to share it with others.

Recommended ways to participate:
- add example ROMs under `ROMS/Examples`
- improve the compiler or instruction set
- add documentation for sample programs
- experiment with graphics, control flow, or new instructions

## License

This project is available under the terms of the included LICENSE file.

## Final note

InfyCPU-1.0 is best viewed as a creative coding project: a small custom machine you can run, study, modify, and use to make fun little programs. If you want to explore low-level design, display rendering, or simple virtual hardware, this repo is a playful place to start.
