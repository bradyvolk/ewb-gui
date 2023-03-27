# ewb-gui

Engineer's Without Borders Digital Agriculture Subteam GUI design experimentation for rover and drone control application

## Overview

We plan to build our app with Python using Kivy to develop our GUI and interface with the Google Maps API (Acutally might not use Google Maps API, we'll see?)

## Getting Started with Kivy

Install kivy virtual environment and other dependecies into `ewb-gui/application` directory.

After [installing Kivy](https://kivy.org/doc/stable/installation/installation-windows.html#install-win-dist), checkout this tutorial series to get down the basics: https://www.youtube.com/watch?v=bMHK6NDVlCM&list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn&ab_channel=TechWithTim

## Package Management

### To activate virtual environment:

- Navigate to application folder and run following command

```shell
kivy_venv\Scripts\activate
```

### Other packages to install in virtual env:

```shell
pip install -r requirements.txt
```

### Running Application

1. activate virtual environment shown above
2. Run following command

```shell
python main.py
```

### Working with Google Maps API

https://github.com/googlemaps/google-maps-services-python

### Kivy Map Widget:

https://github.com/kivy-garden/garden.mapview
