# Celestial-World---Exitus-Tracker

## Warning

This tool is currently under active development and is primarily intended for personal use. It may not be fully functional, stable, or suitable for all use cases.

## About the Tool

The Cele Exitus Tracker is a GUI tool providing information about the Exitus Portals and saving the character's position as coordindates into the game client, making it possible to teleport over the Exitus Tracker GUI to the portal positions, which is done by extending the game client's functionality. For every portal you may want to change after map clear to, you can take a screenshot which is listed in the GUI automatically. Currently there is no clean interface as end user to set hotkeys. F11 is used to take a screenshot that is added to the Exitus Tracker, F12 is used to reset the GUI. The window handle of the game client is needed to send inputs to the cele client in order to realize the teleport function which is done by sending key inputs to the client. 

![Example 1](Example_Image1PNG.png)
![Example 2](Example_Image2PNG.png)




## Using with modded game client

To use with teleport function you need to mode the game client's folder cewo with the game.py file provided, which extends the game client with methods for saving coordinates in the game client and teleport to them

## Limitation

1. Currently only possible to use with one game client
2. Optimized for 2k resolution, but still usable on other
