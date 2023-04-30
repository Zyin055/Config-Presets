## What does this do?
This [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) extension adds a configurable dropdown to allow you to change settings in the txt2img and img2img tabs of the Web UI.

## Screenshots
The new dropdown in the image gallery.

![gallery](https://i.imgur.com/ef0p7wM.jpg)

Dropdown values (configurable), select one and the generation settings values will be applied to the Web UI.

![dropdown](https://i.imgur.com/WqbTZCR.jpg)

Clicking the "Add/Remove..." button lets you create and delete custom presets of settings currently in the Web UI. Custom fields added by other scripts/extensions can also be used by clicking the "Add custom fields..." button. Each button has tooltips to help you.

![addremove](https://i.imgur.com/sYANTi2.jpg)

Screenshot of config-txt2img.json, which can be opened with the "Open config file..." button. You can use this if you want manual control while editing your presets. config-img2img.json also exists for the img2img tab.

![config](https://i.imgur.com/rLONKXz.jpg)

## Installation
#### Easy way
* In your Automatic1111 Web UI, go to the Extensions tab > Install from URL > URL for extension's git repository: `https://github.com/Zyin055/Config-Presets`
* Click the Install button
#### Manually
* Git clone this repo to the `extensions` folder in your Stable Diffusion installation

## Known bugs
* [Can't fix] Updating from an old version (before 12/21/2022 update) will wipe your custom config presets

## Changelog
<details>
    <summary>Click to view Changelog</summary>
    
#### 4/29/2023
* Updated for the March 29th Automatic1111 version which uses Gradio 3.23
* Added the ability to add almost any field on the UI to a config preset with the "Add tracked fields..." button
#### 3/06/2023
* Added the ability to select which fields are saved when creating a new config preset (before, this could have been done manually by editing the .json config file)
* Moved some buttons around in the UI for creating a new config preset
* Added Hires Upscaler (txt2img_hr_upscaler), Upscale by (txt2img_hr_scale), and Restore Faces (txt2img_restore_faces) as eligible fields to be used in a config preset
* Tweaked default config preset values created during installation
* Removed "Default" preset since it doesn't work with new system that lets you ignore fields
#### 2/10/2023
* Manually removing a preset value in the config file will make that value be ignored
#### 2/09/2023
* Added 768x768, 1080p, 1440p, and 4k presets for txt2img (they won't show up for existing installations, you'd need to delete your config-txt2img.json file to have it recreated with the new presets)
#### 1/02/2023
* Your custom presets will be wiped, you will need to remake any saved custom presets because of changes made in Automatic1111
* The Config Presets dropdown in the txt2img and img2img tabs now use separate config files and thus have separate presets
* Saving a new preset now requires a Web UI restart (done automatically)
* Added support for the Sampler method turning from a checkbox into a dropdown
* Added support for the removal of Firstpass width/height being replaced by Upscale by
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
</details>
