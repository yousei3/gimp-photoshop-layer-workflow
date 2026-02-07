# GIMP Photoshop Layer Workflow

A collection of Python plugins for GIMP designed to bring familiar, Photoshop-style layer management to your workflow. This suite is specifically developed and tested for the **GIMP 3.0 series (including 3.2)** on **Linux Mint**.

<img width="250" height="1012" alt="image" src="https://github.com/user-attachments/assets/d7d8ae9a-6c10-4afa-91b7-c2f30daa8ab9" />

## Features

This suite includes three essential tools to streamline your layer operations:

* **Group Selected Layers**: Groups all currently selected layers into a new layer group.
* **Ungroup Layers**: Unpacks layers from a selected group and deletes the empty group layer.
* **Merge Selected Layers**: Merges only the selected layers into a single new layer, preserving your original layers.

## Installation (Important for GIMP 3.0+)

In GIMP 3.0 and newer, each plugin must be placed in its own subfolder within the plug-ins directory. **The folder name must be identical to the filename (without the .py extension).**

1.  Download the `.py` files from the `src/` folder.
2.  Navigate to your GIMP plug-ins directory:
    * Linux: `~/.config/GIMP/3.0/plug-ins/`
3.  Create a separate folder for each script and place the file inside as shown below:

### Directory Structure
```text
plug-ins/
├── group_selected_layers/
│   └── group_selected_layers.py
├── merge_selected_layers/
│   └── merge_selected_layers.py
└── ungroup_layers/
    └── ungroup_layers.py

```

4. Ensure the `.py` files have execution permissions:
```bash
chmod +x *.py

```


5. Restart GIMP. You will find the new commands under the **Layer** menu.

> [!TIP]
> **Shortcut Keys:** These tools are much more powerful when assigned to shortcuts. Please set them yourself in GIMP (Edit > Keyboard Shortcuts).

## Technical Background & AI Assistance

I am still in the process of learning Python and GIMP plugin development. To bridge the gap and create these tools, I collaborated with **AI (Google Gemini)** to write and refine the code.

My goal was to replicate specific Photoshop behaviors that I missed in GIMP. While these scripts were developed with AI assistance, they have been manually tested and verified to work correctly in my Linux Mint environment.

## License

This project is open-source under the [MIT License](https://www.google.com/search?q=LICENSE). Feel free to use, modify, and share!


