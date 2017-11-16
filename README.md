# chinese_licence_plate_generator
A tool for generating Chinese license plate dataset for plate detecting
 
When you are working on a Automatic Number Plate Recognition(ANPR) project, you may need thoundands of samples to train. Heres is
 my solution for generating chinese licence plate samples.
 
## First Stage: Generate the plate
There are two kind of plates:
1 real plate are cutted from pictures

2 Fake plate are formed with several random characters 
 
## Second Stage: Generate world(background)
I named background with ‘world’ in my code. 
There are two kinds of world image:
1 image with only one color
I used only blue image for blue plate, yellow and white image could be added. 
2 Random image from some big datasets
 
## Third stage: Add objects to world
I add some negative objects for hard nagative mining, and adds only one plate to one world. I put the position of the plate relative to the world in the image file name. You can read the position from the image file name as ground truth.
 
## Here are some examples:
 
 
