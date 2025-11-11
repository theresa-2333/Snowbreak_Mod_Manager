<img width="1273" height="756" alt="v0 2 1 en img" src="https://github.com/user-attachments/assets/90e7a776-7f99-4abd-8e2c-59a0d3b65341" />


-----

## Snowbreak Mod Manager

### Introduction

 **Snowbreak Mod Manager** is a powerful and easy-to-use Mod management tool designed specifically for players of **Snowbreak: Containment Zone**. Developed by theresa-2333, it aims to help players easily manage their game Mods, including installation, enabling, disabling, and classification, significantly simplifying the process of using Mods.

### Key Features

  * **Centralized Management**: All Mods are managed within one intuitive interface, eliminating the need for manual drag-and-drop and file confusion.
  * **One-Click Enable/Disable**: Easily check or uncheck a Mod to enable or disable it, without the need for manual file renaming.
  * **Flexible Classification System**: Organize your Mods by custom classifications like character names and skins, making searching and management more efficient.
  * **Detail Preview**: Add custom names, notes, and preview images for each Mod, allowing you to quickly identify the content and effect of the Mod.
  * **Smart Path Management**: Automatically manages the storage path of Mod files, keeping your game directory neat and organized.
  * **Theme Switching**: Supports light and dark themes to accommodate different user preferences.
  * **Lightweight and Efficient**: Built on Python and PyQt5, it has low resource usage and runs smoothly.

### How to Use

1.  **Set the Mod Storage Path**:

      * Upon first launch, the program will prompt you to set a Mod storage path.
      * You can modify this path anytime via the "Change..." button on the main interface.
      * **Important Tip**: This path should be set to the `Game\Content\Paks\~mods` directory under the game's root directory. The program will automatically copy Mods to this path and control enabling/disabling through file renaming.
      * **Only one Mod can be enabled per skin at a time**. Please note that `_100_P` at the end of the filename is crucial, so do not delete it. If you encounter issues with a Mod not taking effect, check if the Mod filename contains `_100_P` before the file extension.

2.  **Add a Mod**:

      * Click the "Add New Mod..." button.
      * Select your Mod file.
      * In the pop-up window, select or create a primary classification (usually the character name) and a secondary classification (usually the skin name) for your Mod.
      * Click "OK." The Mod file will be copied to your set storage path and will appear in the management list.

3.  **Manage Mods**:

      * Click the Mod you wish to manage in the tree view on the left.
      * The panel on the right will display the Mod's detailed information.
      * You can modify the Mod name and notes.
      * Click "Change Image" to add or modify the Mod's preview image.
      * Check or uncheck the "Enable Mod" checkbox to enable or disable it.
      * Click "Save Changes" to save your modifications.

4.  **Delete a Mod**:

      * Select the Mod you wish to delete.
      * Click the "Delete Selected Mod" button.
      * The program will ask you to confirm the deletion and will permanently delete the Mod file from the storage path.

### Dependencies and Installation

  * **General Users**: Directly install and use the latest program from the Releases section.

  * **Developers**:
    This tool requires Python 3 and the PyQt5 library.

    ```bash
    # Install dependencies
    pip install PyQt5

    # Run the program
    python mod_manager_v0.2.1.py
    ```

### Future Plans

We welcome any feedback, suggestions, and contributions from the community. Please submit issues or create pull requests through our GitHub project page.


### Update Log

**Version 0.2**

  * Added custom Mod storage path functionality.
  * Added theme switching functionality (Light/Dark).
  * Fixed known bugs and improved stability.

-----

**Version 0.2.1**

  * Added English support

This is an open-source project. Stars and Forks are welcome\!

-----
