//Name:         Eric Paulz
//Instructor:   Brygg Ullmer
//Class:        3220
//Date:         11-12-2018

// Base code by Bidur Bohara (LSU) in collaboration with Brygg Ullmer

//#include <QCoreApplication>
#include <vector>
#include <math.h>
#include "cscbitmap.h"
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// structure to hold arguments for pthread_create()
struct arg_struct{
    int w;
    int start_h;
    int end_h;
    int threadID;
};

int sobel_x[3][3] = { { 1, 0,-1},
                      { 2, 0,-2},
                      { 1, 0,-1}};

int sobel_y[3][3] = { { 1, 2, 1},
                      { 0, 0, 0},
                      {-1,-2,-1}};

/// Declaration of functions.
void* findEdge(void* args);

/// Memory to hold input image data
unsigned char* inData;
std::vector<unsigned char> image_sobeled;

// Qt entry point!
// Create and run a thread inside main function.
// Also assign region of image to a thread, and 
// call thread join for synchronization.
int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);
    char* bmpFile;
    if( argc < 3) // changed number of required arguments
      {
	printf("Usage: <executable> <input filename> <thread count>\n");
	return 0;
      }
    else
      bmpFile = argv[1]; 
    
    /// Open and read bmp file.
    Bitmap *image = new Bitmap();
    unsigned char*data = image->readGrayBitmap(bmpFile);
    
    image_sobeled.clear();
    image_sobeled.resize(image->bmpSize, 255);
    inData = data;

    // split image rows up equally among threads
    int numThreads = atoi(argv[2]);
    int split = image->bmpHeight / numThreads;
    
    arg_struct *args;
    args = (arg_struct *)malloc(sizeof(arg_struct));

    // loop to create threads and call findEdge()
    // pass in height/width assignments for each thread
    std::vector<pthread_t> tid(numThreads);
    int start = 0, end = split;
    for(int i=0; i < numThreads; i++){
	args->w = image->bmpWidth;
	args->start_h = start;
	args->end_h = end;
	args->threadID = i;

        pthread_create(&tid[i], NULL, findEdge, (void *)args);
	
	start = end;
	end += split;
    } 
    
    // join threads back
    for(int i=0; i < numThreads; i++){
	pthread_join(tid[i], NULL);
    }

    /// Write image data passed as argument to a bitmap file
    image->writeGrayBmp(&image_sobeled[0]);
    image_sobeled.clear();
    delete data;

    delete args;

    return 0;
    //return a.exec();
}


/// Function that implements Sobel operator.
/// Returns image data after applying Sobel operator to the original image.
/// Reimplement findEdge such that it will run in a single thread
/// and can process on a region/group of pixels
void* findEdge(void* args)
{
    arg_struct *b;
    b=(arg_struct*)args;

    printf("Running on Thread #%d...\n",b->threadID);

    int gradient_X = 0;
    int gradient_Y = 0;
    int value = 0;

    // The FOR loop apply Sobel operator
    // to bitmap image data in per-pixel level.
    for(unsigned int y = b->start_h; y < b->end_h-1; ++y)
        for(unsigned int x = 1; x < b->w-1; ++x)
        {
            // Compute gradient in +ve x direction
            gradient_X = sobel_x[0][0] * inData[ (x-1) + (y-1) * b->w ]
                    + sobel_x[0][1] * inData[  x    + (y-1) * b->w ]
                    + sobel_x[0][2] * inData[ (x+1) + (y-1) * b->w ]
                    + sobel_x[1][0] * inData[ (x-1) +  y    * b->w ]
                    + sobel_x[1][1] * inData[  x    +  y    * b->w ]
                    + sobel_x[1][2] * inData[ (x+1) +  y    * b->w ]
                    + sobel_x[2][0] * inData[ (x-1) + (y+1) * b->w ]
                    + sobel_x[2][1] * inData[  x    + (y+1) * b->w ]
                    + sobel_x[2][2] * inData[ (x+1) + (y+1) * b->w ];

            // Compute gradient in +ve y direction
            gradient_Y = sobel_y[0][0] * inData[ (x-1) + (y-1) * b->w ]
                    + sobel_y[0][1] * inData[  x    + (y-1) * b->w ]
                    + sobel_y[0][2] * inData[ (x+1) + (y-1) * b->w ]
                    + sobel_y[1][0] * inData[ (x-1) +  y    * b->w ]
                    + sobel_y[1][1] * inData[  x    +  y    * b->w ]
                    + sobel_y[1][2] * inData[ (x+1) +  y    * b->w ]
                    + sobel_y[2][0] * inData[ (x-1) + (y+1) * b->w ]
                    + sobel_y[2][1] * inData[  x    + (y+1) * b->w ]
                    + sobel_y[2][2] * inData[ (x+1) + (y+1) * b->w ];

            value = (int)ceil(sqrt( gradient_X * gradient_X +
                                    gradient_Y * gradient_Y));
            image_sobeled[ x + y * b->w ] = 255 - value;
        }
    // Visual Studio requires this to be present; and should not 
    // cause issues for other compilers. 
    // Thanks to Thomas Peters.
    return 0;
}
