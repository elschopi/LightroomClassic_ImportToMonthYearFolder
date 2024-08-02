# LightroomClassic_ImportToMonthYearFolder
repository with python code to be run in e.g. Thonny (as Admin) to automatically edit the strings.txt file

This repository contains the file lightroom_linechanger.py

Lightroom Classic does offer a lot of import options, unfortunately an option that is not present is to create a folder with the month (text) and year (4-digit). To get that option, a change in the appropriate translated_strings.txt can be made. However, this change gets
deleted on any update to Lightroom. 

I'm using Lightroom in Germany, so the filename of the file I need to change is "TranslatedStrings_Lr_de_DE.txt". I'm running Windows 11.
I use Thonny as my main python IDE (because I do most of my coding on micropython), but I've also used VS Code with this file.
Important: Thonny / VS Code (or any IDE, I don't know) need to be launched with administrative rights, else accessing and altering the files on the harddrive is not possible.

To use, simply load the lightroom_linechanger.py into Thonny and open it. Scroll down to the last line and edit the command to point to your appropriate translated_strings.txt. 
Then, just press "Play" or "Run current script". 

If the file already has been altered, you'll get a message.

Of course this can be used to inject other import options instead of "MONTH YEAR".

Here you can find an overview of the usable commands: [link to archive.org](https://web.archive.org/web/20160227080331/http://digital-photography-howto.com/translatedstrings-txt-explained-customizing-the-file-structure-in-adobe-lightroom/)
