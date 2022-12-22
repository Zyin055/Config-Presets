## What does this do?
This [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension adds a configurable dropdown to allow you to change settings in the txt2img and img2img tabs of the Web UI.

Note: If you're updating from a version before 12/19/2022 your config.json settings will be overwritten. Make a backup if you want to keep your custom presets before updating.

## Screenshots
The new dropdown in the image gallery.

![gallery](https://i.imgur.com/ef0p7wM.jpg)

Dropdown values (configurable), select one and the generation settings values will be applied to the Web UI.

![dropdown](https://i.imgur.com/hWpoR9N.jpg)

Each config preset holds values for:
* Sampling Steps
* Sampling method
* Width
* Height
* Highres. fix
* Firstpass width
* Firstpass height
* Denoising strength
* Batch count
* Batch size
* CFG Scale

Clicking the "Add/Remove..." button lets you create and delete custom presets of settings currently in the Web UI. Each button has tooltips to help you.

![dropdown](https://i.imgur.com/OD8wcSt.jpg)

Screenshot of config.json, which can be opened with the "Open..." button. It's created after the extension is loaded for the first time. You can use this if you want finer control on editing your presets.

![config](https://i.imgur.com/acFy6Hq.jpg)

## Installation
* In your Automatic1111 Web UI, go to the Extensions tab > Install from URL > URL for extension's git repository: `https://github.com/Zyin055/Config-Presets`
* Click the Install button

## Known bugs
* [Won't fix] Presets added/removed in one tab won't update to the dropdown in another tab until a Gradio restart

## Changelog
#### 12/21/2022
* Added the "Add/Remove..." button to create and delete config presets within the Web UI
#### 12/19/2022
* config.json will be created on first startup, user edits will not be overwritten when updating the extension after updating to this version
#### 12/15/2022
* Fix for installation error on linux
#### 12/13/2022
* config.json was tweaked, added Firstpass width and Firstpass height
* Better support for img2img tab compatibility
#### 12/12/2022
* Initial Release
