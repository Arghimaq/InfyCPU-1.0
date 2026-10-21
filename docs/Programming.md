# How to program
## The ISA
| Opcode | Assembly name | Operands | Description |
| --- | --- | --- | --- |
| `0` | `NOP` | None | Does nothing |
| `1` | `ST` | `dst` `src` | Stores a register's value into RAM at a certain address |
| `2` | `LD` | `dst` `src` | Load a value from the RAM into a register | 
| `3` | `STI` | `dst` `imm` | Store immediate value into RAM at a certain address |
| `4` | `LDI` | `dst` `imm` | Load immediate value into a register |
| `5` | `SWP` | `reg` `reg` | Swap register values |
| `6` | `COP` | `src` `dst` | Copy register value into a register |
| `7` | `PUSH` | `reg` `none` | Push a register value into stack |
| `8` | `PUSHi` | `imm` `none` | Push an immediate value into stack |
| `9` | `POP` | `dst` `none` | Pop a value from the stack and load into a register |
| `10` | `ADD` | `src` `val` | Add a register's value into a register |
| `11` | `SUB` | `src` `val` | Subtract a register's value from a register |
| `12` | `MUL` | `src` `val` | Multiplay a register's value with a register |
| `13` | `DIV` | `src` `val` | Divide a register's value with a register |
| `14` | `ADDi` | `src` `val` | Add an immediate value into a register |
| `15` | `SUBi` | `src` `val` | Subtract an immediate value from a register |
| `16` | `MULi` | `src` `val` | Multiplay an immediate value with a register |
| `17` | `DIVi` | `src` `val` | Divide an immediate value with a register |
| `50` | `CMPei` | `reg` `imm` | Set compare flag to true if the register and immediate values are equal |
| `51` | `CMPgi` | `reg` `imm` | Set compare flag to true if the register value is greater than the immediate value |
| `52` | `CMPli` | `reg` `imm` | Set compare flag to true if the register value is lower than the immediate value |
| `53` | `CMPe` | `reg` `reg` | Set compare flag to true if the register values are equal |
| `54` | `CMPg` | `reg` `reg` | Set compare flag to true if the register value is greater than the other register value |
| `55` | `CMPl` | `reg` `reg` | Set compare flag to true if the register value is lower than the other register value |
| `20` | `JMP` | `label/address` `none` | Jump to label or address |
| `21` | `JZ` | `label/address` `inverse` | Jump to label or address if the zero flag is true. Inverse if second operand is not 0 |
| `22` | `JINP` | `label/address` `inverse` | Jump to label or address if the input flag is true. Inverse if second operand is not 0 |
| `23` | `JCMP` | `label/address` `inverse` | Jump to label or address if the compare flag is true. Inverse if second operand is not 0 |
| `24` | `CALL` | `label/address` `none` | Jump to label or address and push next instruction's address into stack |
| `25` | `CLLZ` | `label/address` `inverse` | Jump to label or address and push next instruction's address into stack if the zero flag is true. Inverse if second operand is not 0 |
| `26` | `CLLNP` | `label/address` `inverse` | Jump to label or address and push next instruction's address into stack if the input flag is true. Inverse if second operand is not 0 |
| `27` | `CLLCMP` | `label/address` `inverse` | Jump to label or address and push next instruction's address into stack if the compare flag is true. Inverse if second operand is not 0 |
| `28` | `RET` | `none` `none` | Pop from stack and jump to the value as address |
| `40` | `INP` | `dst` `none` | Set input flag to true if input received, and load pressed key into a register |
| `30` | `VST` | `addr` `clr` | Store the color value at a register into frame buffer address at a register value |
| `31` | `VSTI` | `addr` `clr` | Store the immediate color value at a register into frame buffer address at a register value |
| `32` | `BLTi` | `x` `y` | Set blitter register to calculated frame buffer address from x and y |
| `33` | `BLT` | `x` `y` | Set blitter register to calculated frame buffer address from 2 register values |
| `34` | `BLTr` | `reg` `none` | Load blitter register value into a register
| `999` | `HALT` | `none` `none` | Halt the CPU
| `1111` | `PRINT` | `reg` `none` | Print register value in python console.

## Loop labels.

The old way of making loops was difficult:

```iasm
;do something
jmp 0 0
```
But labels are now available. Here is an example how to use them:
```iasm
$loop:
  ;do something
  jmp $loop 0
```
You have to write the beginning of the loop with its label with a $ before the name at the top, and reference it in jmp using a $. However this doesnt mean you cant do immediate numbers anymore. Most programs in the examples directory use immediate addresses.
Calls and returns was also recently added. You can call a subroutine using `CALL $subroutine 0 `, and inside a subroutine to come back to the main loop you can do `RET 0 0`. subroutines look like this:
```.iasm
$subroutine:
  ;do something
  RET 0 0
```

## Video
If you want a pixel to have a color, you must assign its color using either `VST` or `VSTI`. the second operand `clr` is not RGB. It uses a color palette:

| Number | Color | RGB |
| --- | --- | --- |
| 0 | Black | 0, 0, 0 |
| 1 | White | 255, 255, 255 |
| 2 | Red | 255, 0, 0 |
| 3 | Yellow | 255, 255, 0 |
| 4 | Green | 0, 255, 0 |
| 5 | Cyan | 0, 255, 255 |
| 6 | Blue | 0, 0, 255 |
| 7 | Purple | 255, 0, 255 |

Calculating the memory address of a coordinate on the screen by hand or on the CPU takes time. `BLT` or `BLTi` fixes that problem. if you want to know the memory address of 2 and 5, you can write `BLTI 2 5` or `BLT 0 1` if they're in registers. The result will be saved into a blitter register, and to take that result, you can load the blitter register value into a register using `BLTr reg 0`.

## Flags

| Flag | Activation|
| --- | --- |
| Compare Flag | Activated by `CMP` opcodes |
| Jump Flag | Activated by `JMP` opcodes |
| Zero Flag | Activated if last arithmetic operation resulted to 0 |
| Input Flag | Activated if `INP` catched an input |

## Notes

For some opcodes like `POP`, `INP`, `JMP` or `RET` you do not need to use all operands, however it does not mean you should include nothing in the operand's place. You must put a number in it, so
```.iasm
RET
POP 4
INP 3
JMP $loop
```
will create errors. instead make placeholders
```.iasm
RET 0 0
POP 4 0
INP 3 0
JMP $loop 0
```
