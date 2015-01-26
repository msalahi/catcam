# catcam

Stream video to ascii art in the command line!

![Demo](https://raw.githubusercontent.com/msalahi/catcam/master/demo.gif)

## Why?
Because why not.

## Install

This project is still in its very early days, and thus currently only supports:

- Python3.4
- Environments that play nice with NCurses
- Terminals with an XTerm256 color scheme
- URLs to MJPEG resources 

If you happen to be one of the five or six people in the world to whom all of the above criteria apply, or you'd just like to poke around, I'd recommend doing so by cloning this repo, and installing it into a virtualenv.
```
    git clone https://github.com/msalahi/catcam.git
    cd catcam/
    pip install -e .
```

## Test

To run the tests, first install pytest.
```
pip install pytest
```
Then, make sure you are in the `catcam/` directory containing `tests/`. From there, simply invoke `py.test`, and the tests should run! 

## Usage

Provided you've got a URL to an MJPEG stream handy, running is as simple as:
```
catcam http://example.com/videostream
```
