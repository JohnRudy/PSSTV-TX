# SSTV Encoders

This projects goal is to create a tool to create sstv encoders for some sstv transmission modes. 
Personally, it was a tool for another project but turned out to be a bit more complex and broad for just that only so I made it available in it's current state.
In the future, there probably will be more than just 2 encoders, when I get around to it. 

## This isn't a real encoder!

Currently I create "pseudo" audio. Meaning It's close enough but I have no means of testing these and there are bugs. If I ever get my hands on proper syncing times for the encoders I'll make the necessary modifications to make it more usable in real life. 

## Plans

Plans are to improve the general usage options, add more encoders and fix the syncing issues.

* fix existing encoders
* Add a encoder manager
* launch options/arguments
* add new encoders
* A GUI would be nice but WAAAAAAY of in the future. 

Broad strokes. Yes.

### Prerequisites

What you need.

* Python 3+ should work. (Written in 3.10.4)
* a version of pip or a package manager of your choise to install requirements
* patience to read my horrible python code.

### Installation

To get this working

```
$ download and install python. 
$ install pip
$ (I suggest using a virtual environment, virtualvenv or the likes for requirements)
$ clone this repo
$ cd to the repo
$ pip install --no-cache -r requirements.txt
```
Once you have these. Make a `images` folder with your desired images to encode inside the root folder.
ALL IMAGES INSIDE THE FOLDER GET ENCODED! So make sure you have the ones there that you want to encode.
The script will make `audio` and `encoded` folders for the audio files and pseudo images. 
Note that different encoders have different size requirements. I do resize the images in code to fit the spesific encoder but it is always best to use the right size if only a spesific mode is desired. 
You can check these image sizes inside `./bin/settings/sstv_settings.py` for your spesific encoder type under `image_size` 

## Current encoders

Currently, somewhat working encoders

* Robot36 - has a header and leading tone issue
* WraaseSC2-120 - Timings are off
* WraaseSC2-180 - Timings are off

## Usage

Currently there are no arguments. These will be added later in development.
To run the script, cd into the cloned folder.
```
$ python3 sstv_encoder.py
```
To switch modes you need to modify inside `sstv_encoder.py:33` `mode = MODE.{mode setting}`. 
This will be made an argument in the future. 
