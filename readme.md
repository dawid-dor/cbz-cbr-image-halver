# CBZ/CBR Image Halver

## About:

Lightweight script that splits the images that are packed in .CBZ (or .CBR) format into two (by halving them) and creating a new archive with halved images inside.
Useful if scans that you are currently reading are made by scanning the whole comic book (literally, two pages at the same time). The program will then split those two pages into two separate file.

## How to use:

- Put \*.cbz (or \*.cbr) files (with images) into **./data** folder
- After script completes its run, it will store its output in **./output** folder

## Note:

- Depending on you system or system language, you might need to change global variable _FOLDER_SEPARATOR_ from its default value (**"\\"**) to the more common one (**"/"**).
  It was tested on polish version of Windows 10 (and that is the default settings currently set up).

- Default behavior is set to handle comics that are ridden from right to left. You can change this behavior by changing global variable _READING_LEFT_TO_RIGHT_ from its default value (**False**) to **True**
