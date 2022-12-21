## What does this do?
This [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension adds a configurable dropdown to allow you to change settings in the txt2img and img2img tabs of the Web UI.

Note: If you're updating from the 12/22/2022 version your config.json will be overwritten. Make a backup if you want to keep your custom presets before updating.

## Screenshots
The new dropdown in the image gallery

![gallery](https://i.imgur.com/ef0p7wM.jpg)

Dropdown values (configurable)

![dropdown](https://i.imgur.com/hWpoR9N.jpg)

Clicking the "Add/Remove..." button

![dropdown](https://i.imgur.com/OD8wcSt.jpg)

Screenshot of config.json, which can be opened with the "Edit..." button. It's created after the extension is loaded for the first time

![config](https://i.imgur.com/acFy6Hq.jpg)

## Installation
* In your Automatic1111 Web UI, go to the Extensions tab > Install from URL > URL for extension's git repository: `https://github.com/Zyin055/Config-Presets`
* Click the Install button

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
