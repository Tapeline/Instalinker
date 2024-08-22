# Instalinker
![only for windows](https://img.shields.io/badge/os-windows-blue)

A neat solution for dealing with portable programs on Windows

---

<!-- TOC -->
* [Instalinker](#instalinker)
  * [Description](#description)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Adding programs](#adding-programs)
    * [Removing programs](#removing-programs)
    * [Installing programs](#installing-programs)
    * [Uninstalling programs](#uninstalling-programs)
  * [Tech stack](#tech-stack)
  * [Developer](#developer)
  * [License](#license)
<!-- TOC -->

---

## Description

Ever stumbled upon some software that is distributed without
installer (portable) and then every time you needed to run it
you searched through your folders wondering where you 
installed it?

Instalinker tries to solve this issue by providing a simple
way to add shortcuts to start menu.

## Installation
> **Notice!** <br/>
> Instalinker is only avalilable on Windows!

To install, simply run installer from Releases

## Usage
### Adding programs
1. Click on `Add program`
2. Select the executable
3. Set the name

### Removing programs
1. Select program in list
2. Click on `Remove program`

This action only removes the shortcut, the
program will stay on your drive

### Installing programs
This will come in handy when you download a zip
file with portable software

1. Click on `Install program`
2. Select your desired zip
3. Select executable in installed folder
4. Choose name

### Uninstalling programs
This, however, will not only delete the shortcut,
but also will erase the program on your drive.
Proceed with caution.

1. Select program in list
2. Click on `Uninstall program`

## Tech stack
![Tkinter](https://img.shields.io/badge/Frontend-tkinter-blue)

## Developer
Project is being developed by [@Tapeline](https://github.com/Tapeline)

## License
This work is licensed under GNU General Public License v3.0