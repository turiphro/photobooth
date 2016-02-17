Installation
============

Install all requirements:

    sudo apt-get install bluetooth blueman ussp-push python-bluetooth libbluetooth-dev`
    sudo pip3 install -r requirements.txt

Run the setup script (bt pincode etc):

    sudo python setup.py

I've had some problems getting bluetooth transfer to work;
different people are reporting variations in success with
different tools. You might need to experiment a bit, pair
via the various UI's and print some test selfies while
looking annoyed.


Running
=======

To run the GUI application, start with:

    python3 main.py

