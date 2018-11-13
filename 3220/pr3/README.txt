Name:         Eric Paulz
Instructor:   Brygg Ullmer
Class:          3220
Date:           11-12-2018

epaulz_pr3.tar.gz contains:
- cscbitmap.h
- cscbitmap.cpp
- main.cpp
- Makefile
- README
- lena512.bmp

Notes:
- Type 'make' to compile the program.
- Type 'make clean' to clean up output/executable files.
- Type 'make run' to run with a set input file and thread count
- I used 'lena512.bmp' for testing.
- As of now, my program will only perform edge detection on part of the image with
   small numbers of threads (ex. 5).  It will process the entire image when the thread
   count gets higher (ex. 15-20)