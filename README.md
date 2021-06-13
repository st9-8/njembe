# njembe

## Why njembe ?

We all use the terminal daily, and sometimes we find ourselves installing tools by following documentations and articles online or not, resulting in a series of +/- difficult steps. 
The worry is that once we finish, we close all the browser windows, and the console, because we succeeded🥳🥳.

But as soon as we have to repeat those steps a few weeks or months later, or even when we want to help someone who is in the same situation, we can't anymore because we can't remember exactly what the steps are and why each step😪.

So that's where **njembe** comes in. **njembe** is a small and simple command line tool that allows you to save the commands and steps of your processes done in console, it also provides you these documentations in a format that you can share to anyone who wants to.

## Useful tips for njembe

- By default, **njembe** uses `editor` command to permit you to write you command description, but you can set your prefered editor by setting `$EDITOR` env variable.
- When nothing happens when you type a njembe command, you can check the log file at `$HOME/Documents/njembe/logs/`.
- Only one documentation can be opened at a moment, so to open another one if one is already opened, you must close the previous one using `nj close` or `njembe close`.
- All `nj command [ARGUMENTS]` of `nj command [ARGUMENTS]` you type are saving in the current opened documentation.
- **njembe** respects this [POSIX guidelines](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html#tag_12_02), especially the guidelines 10 for command lines arguments including **-** character at the beginning.

## Installation

### From repository

1. `$ git clone https://github.com/st9-8/njembe.git`
2. `$ cd njembe`
3. `$ sudo apt install libsqlite3-dev`
4. `$ sudo python3 setup.py install`

### From PyPi
`pip install njembe`

## Example

![How it works example!](https://github.com/st9-8/njembe/blob/main/examples/njembe.gif)
