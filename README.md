# GIMP Photoshop Layer Workflow

A collection of Python plugins for GIMP that bring familiar, Photoshop-style layer management to your workflow. Developed and tested on **Linux Mint**.

<img width="250" height="1012" alt="image" src="https://github.com/user-attachments/assets/d7d8ae9a-6c10-4afa-91b7-c2f30daa8ab9" />

## Features

This suite includes three essential tools to streamline your layer operations:

* **Group Selected Layers**: Groups all currently selected layers into a new layer group.
* **Ungroup Layers**: Unpacks layers from a selected group and deletes the empty group layer.
* **Merge Selected Layers**: Merges only the selected layers into a single new layer, preserving your original layers.

## Installation

1.  Download the `.py` files from the `src/` folder.
2.  Copy the files to your GIMP plug-ins directory.
    * On Linux: `~/.config/GIMP/2.10/plug-ins/`
3.  Ensure the files have execution permissions:
    ```bash
    chmod +x *.py
    ```
4.  Restart GIMP. You will find the new commands under the **Layer** menu.

info：Please set the shortcut keys yourself.

## Technical Background & AI Assistance

I am still in the process of learning Python and GIMP plugin development. To bridge the gap and create these tools, I collaborated with **AI (Google Gemini)** to write and refine the code. 

My goal was to replicate specific Photoshop behaviors that I missed in GIMP. While these scripts were developed with AI assistance, they have been manually tested and verified to work correctly in my Linux Mint environment.

## License

This project is open-source. Feel free to use, modify, and share!
