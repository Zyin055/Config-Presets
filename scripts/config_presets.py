import traceback
import modules.scripts as scripts
import gradio as gr
import json
import os
import platform
import subprocess as sp


BASEDIR = scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path
CONFIG_TXT2IMG_FILE_NAME = "config-txt2img.json"
CONFIG_IMG2IMG_FILE_NAME = "config-img2img.json"


class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.txt2img_config_preset_dropdown = None

        # These are the settings from the UI that are saved for each preset
        self.txt2img_component_ids = {   # mirrors the config_preset_dropdown.change(output) events and config_preset_dropdown_change()
            "txt2img_sampling",
            "txt2img_steps",
            "txt2img_width",
            "txt2img_height",
            "txt2img_enable_hr",
            "txt2img_hr_scale",
            "txt2img_denoising_strength",
            "txt2img_batch_count",
            "txt2img_batch_size",
            "txt2img_cfg_scale",
        }
        self.img2img_component_ids = {   # mirrors the config_preset_dropdown.change(output) events and config_preset_dropdown_change()
            "img2img_sampling",
            "img2img_steps",
            "img2img_width",
            "img2img_height",
            "img2img_denoising_strength",
            "img2img_batch_count",
            "img2img_batch_size",
            "img2img_cfg_scale",
        }

        # Mapping between component labels and the actual components in ui.py
        self.txt2img_component_map = {k: None for k in self.txt2img_component_ids}  # gets filled up in the after_component() method
        self.img2img_component_map = {k: None for k in self.img2img_component_ids}  # gets filled up in the after_component() method

        # Load txt2img and img2img config files
        try:
            with open(f"{BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}") as file:
                self.txt2img_config_presets = json.load(file)

            # #print("self.config_presets loaded:")
            # for preset_name, values_dict in self.txt2img_config_presets.items():
            #     #print(preset_name,values_dict)
            #     if "steps" in values_dict.keys():
            #         print("[ERROR][Config-Presets] Your config.json file is using an outdated format, so the Config Presets dropdown will not work. You need to delete /extensions/Config-Presets/config.json so it can be recreated with the new updated format.")
            #         break


        except FileNotFoundError:
            # txt2img config file not found
            # First time running the extension or it was deleted, so fill it with default values
            self.txt2img_config_presets = {
                "Default": {},
                "Low quality ------ 512x512, steps: 10, batch size: 8, DPM++ 2M Karras": {
                    "txt2img_sampling": "DPM++ 2M Karras",
                    "txt2img_steps": 10,
                    "txt2img_width": 512,
                    "txt2img_height": 512,
                    "txt2img_batch_count": 1,
                    "txt2img_batch_size": 8,
                    "txt2img_cfg_scale": 7,
                },
                "Medium quality - 512x512, steps: 20, batch size: 8, DPM++ 2S a Karras": {
                    "txt2img_sampling": "DPM++ 2S a Karras",
                    "txt2img_steps": 20,
                    "txt2img_width": 512,
                    "txt2img_height": 512,
                    "txt2img_batch_count": 1,
                    "txt2img_batch_size": 8,
                    "txt2img_cfg_scale": 7,
                },
                "High quality ------ 512x512, steps: 40, batch size: 8, DPM++ 2S a Karras": {
                    "txt2img_sampling": "DPM++ 2S a Karras",
                    "txt2img_steps": 40,
                    "txt2img_width": 512,
                    "txt2img_height": 512,
                    "txt2img_batch_count": 1,
                    "txt2img_batch_size": 8,
                    "txt2img_cfg_scale": 7,
                },
                "High res -------- 1024x1024, steps: 30, batch size: 1, DPM++ 2M Karras, [Upscale by: 2, Denoising: 0.4]": {
                    "txt2img_steps": 30,
                    "txt2img_sampling": "DPM++ 2M Karras",
                    "txt2img_width": 512,
                    "txt2img_height": 512,
                    "txt2img_enable_hr": "true",
                    "txt2img_hr_scale": 2,
                    "txt2img_denoising_strength": 0.4,
                    "txt2img_batch_count": 1,
                    "txt2img_batch_size": 1,
                    "txt2img_cfg_scale": 7,
                },
                "Wallpaper ----- 1920x1080, steps: 30, batch size: 1, DPM++ 2M Karras, [Upscale by: 3, Denoising: 0.3]": {
                    "txt2img_steps": 30,
                    "txt2img_sampling": "DPM++ 2M Karras",
                    "txt2img_width": 640,
                    "txt2img_height": 360,
                    "txt2img_enable_hr": "true",
                    "txt2img_hr_scale": 3,
                    "txt2img_denoising_strength": 0.3,
                    "txt2img_batch_count": 1,
                    "txt2img_batch_size": 1,
                    "txt2img_cfg_scale": 7,
                },
            }

            write_config_presets_to_file(self.txt2img_config_presets, CONFIG_TXT2IMG_FILE_NAME)
            print(f"[Config Presets] txt2img config file not found, created default config at {BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}")


        try:
            with open(f"{BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}") as file:
                self.img2img_config_presets = json.load(file)

        except FileNotFoundError:
            # img2img config file not found
            # First time running the extension or it was deleted, so fill it with default values
            self.img2img_config_presets = {
                "Default": {},
                "Low denoising ------- 512x512, denoising: 0.25, steps: 10, DPM++ 2M Karras": {
                    "img2img_sampling": "DPM++ 2M Karras",
                    "img2img_steps": 10,
                    "img2img_width": 512,
                    "img2img_height": 512,
                    "img2img_batch_count": 1,
                    "img2img_batch_size": 1,
                    "img2img_cfg_scale": 7,
                    "img2img_denoising_strength": 0.25,
                },
                "Medium denoising -- 512x512, denoising: 0.50, steps: 10, DPM++ 2M Karras": {
                    "img2img_sampling": "DPM++ 2M Karras",
                    "img2img_steps": 10,
                    "img2img_width": 512,
                    "img2img_height": 512,
                    "img2img_batch_count": 1,
                    "img2img_batch_size": 1,
                    "img2img_cfg_scale": 7,
                    "img2img_denoising_strength": 0.50,
                },
                "High denoising ------- 512x512, denoising: 0.75, steps: 10, DPM++ 2M Karras": {
                    "img2img_sampling": "DPM++ 2M Karras",
                    "img2img_steps": 10,
                    "img2img_width": 512,
                    "img2img_height": 512,
                    "img2img_batch_count": 1,
                    "img2img_batch_size": 1,
                    "img2img_cfg_scale": 7,
                    "img2img_denoising_strength": 0.75,
                },
            }

            write_config_presets_to_file(self.img2img_config_presets, CONFIG_IMG2IMG_FILE_NAME)
            print(f"[Config Presets] img2img config file not found, created default config at {BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}")


    def title(self):
        return "Config Presets"

    def show(self, is_img2img):
        #return True
        return scripts.AlwaysVisible    # hide this script in the Scripts dropdown

    def after_component(self, component, **kwargs):
        # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
        # so we can use the same code for both tabs
        component_map = None
        component_ids = None
        config_file_name = None
        if self.is_txt2img:
            component_map = self.txt2img_component_map
            component_ids = self.txt2img_component_ids
            config_file_name = CONFIG_TXT2IMG_FILE_NAME
        else:
            component_map = self.img2img_component_map
            component_ids = self.img2img_component_ids
            config_file_name = CONFIG_IMG2IMG_FILE_NAME

        #if component.label in self.component_map:
        if component.elem_id in component_map:
            component_map[component.elem_id] = component
            #print(f"[Config-Presets][DEBUG]: found component: {component.elem_id} {component}")

        #if component.elem_id == "script_list": #bottom of the script dropdown
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        #if component.elem_id == "open_folder": #bottom of the image gallery
        if component.elem_id == "txt2img_generation_info_button" or component.elem_id == "img2img_generation_info_button": #very bottom of the txt2img/img2img image gallery

            #print("Creating dropdown values...")
            #print("key/value pairs in component_map:")
            # before we create the dropdown, we need to check if each component was found successfully to prevent errors from bricking the Web UI
            for k, v in component_map.items():
                #print(k,v)
                if v is None:
                    print(f"[ERROR][Config-Presets] The component '{k}' no longer exists in the Web UI. Try updating the Config-Presets extension. This extension will not work until this issue is resolved.")
                    return

            preset_values = []
            config_presets = None
            if self.is_txt2img:
                config_presets = self.txt2img_config_presets
            else:
                config_presets = self.img2img_config_presets

            for dropdownValue in config_presets:
                preset_values.append(dropdownValue)
                #print(f"Config Presets: added \"{dropdownValue}\"")


            with gr.Column(min_width=600):  # pushes our stuff onto a new row at 1080p screen resolution
                with gr.Row():
                    with gr.Column(scale=8, min_width=100) as dropdown_column:
                        def config_preset_txt2img_dropdown_change(dropdown_value):
                            config_preset = config_presets[dropdown_value]
                            print(f"Config Presets: changed to {dropdown_value}")

                            return (config_preset["txt2img_sampling"] if "txt2img_sampling" in config_preset else component_map["txt2img_sampling"].value,
                                    config_preset["txt2img_steps"] if "txt2img_steps" in config_preset else component_map["txt2img_steps"].value,
                                    config_preset["txt2img_width"] if "txt2img_width" in config_preset else component_map["txt2img_width"].value,
                                    config_preset["txt2img_height"] if "txt2img_height" in config_preset else component_map["txt2img_height"].value,
                                    config_preset["txt2img_enable_hr"] if "txt2img_enable_hr" in config_preset else component_map["txt2img_enable_hr"].value,
                                    config_preset["txt2img_hr_scale"] if "txt2img_hr_scale" in config_preset else component_map["txt2img_hr_scale"].value,
                                    config_preset["txt2img_denoising_strength"] if "txt2img_denoising_strength" in config_preset else component_map["txt2img_denoising_strength"].value,
                                    config_preset["txt2img_batch_count"] if "txt2img_batch_count" in config_preset else component_map["txt2img_batch_count"].value,
                                    config_preset["txt2img_batch_size"] if "txt2img_batch_size" in config_preset else component_map["txt2img_batch_size"].value,
                                    config_preset["txt2img_cfg_scale"] if "txt2img_cfg_scale" in config_preset else component_map["txt2img_cfg_scale"].value,
                                    )

                        def config_preset_img2img_dropdown_change(dropdown_value):
                            config_preset = config_presets[dropdown_value]
                            print(f"Config Presets: changed to {dropdown_value}")

                            return (config_preset["img2img_sampling"] if "img2img_sampling" in config_preset else component_map["img2img_sampling"].value,
                                    config_preset["img2img_steps"] if "img2img_steps" in config_preset else component_map["img2img_steps"].value,
                                    config_preset["img2img_width"] if "img2img_width" in config_preset else component_map["img2img_width"].value,
                                    config_preset["img2img_height"] if "img2img_height" in config_preset else component_map["img2img_height"].value,
                                    config_preset["img2img_batch_count"] if "img2img_batch_count" in config_preset else component_map["img2img_batch_count"].value,
                                    config_preset["img2img_batch_size"] if "img2img_batch_size" in config_preset else component_map["img2img_batch_size"].value,
                                    config_preset["img2img_cfg_scale"] if "img2img_cfg_scale" in config_preset else component_map["img2img_cfg_scale"].value,
                                    config_preset["img2img_denoising_strength"] if "img2img_denoising_strength" in config_preset else component_map["img2img_denoising_strength"].value,
                                    )


                        config_preset_dropdown = gr.Dropdown(
                            label="Config Presets",
                            choices=preset_values,
                            elem_id="config_preset_dropdown",
                        )
                        config_preset_dropdown.style(container=False) #set to True to give it a white box to sit in

                        #self.txt2img_config_preset_dropdown = config_preset_dropdown

                        try:
                            if self.is_txt2img:
                                config_preset_dropdown.change(
                                    fn=config_preset_txt2img_dropdown_change,
                                    show_progress=False,
                                    inputs=[config_preset_dropdown],
                                    outputs=[component_map["txt2img_sampling"],
                                             component_map["txt2img_steps"],
                                             component_map["txt2img_width"],
                                             component_map["txt2img_height"],
                                             component_map["txt2img_enable_hr"],
                                             component_map["txt2img_hr_scale"],
                                             component_map["txt2img_denoising_strength"],
                                             component_map["txt2img_batch_count"],
                                             component_map["txt2img_batch_size"],
                                             component_map["txt2img_cfg_scale"],
                                             ]
                                    )
                            else:
                                config_preset_dropdown.change(
                                    fn=config_preset_img2img_dropdown_change,
                                    show_progress=False,
                                    inputs=[config_preset_dropdown],
                                    outputs=[component_map["img2img_sampling"],
                                             component_map["img2img_steps"],
                                             component_map["img2img_width"],
                                             component_map["img2img_height"],
                                             component_map["img2img_batch_count"],
                                             component_map["img2img_batch_size"],
                                             component_map["img2img_cfg_scale"],
                                             component_map["img2img_denoising_strength"],
                                             ]
                                )
                        except AttributeError:
                            print(traceback.format_exc())   # prints the exception stacktrace
                            print("[ERROR][CRITICAL][Config-Presets] The Config-Presets extension encountered a fatal error. A component required by this extension no longer exists in the Web UI. This is most likely due to the A1111 Web UI being updated. Try updating the Config-Presets extension. If that doesn't work, please post a bug report at https://github.com/Zyin055/Config-Presets/issues and delete your extensions/Config-Presets folder until an update is published.")

                        config_preset_dropdown.change(
                            fn=None,
                            inputs=[],
                            outputs=[],
                            _js="function() { config_preset_dropdown_change() }",   # JS is used to update the Hires fix row to show/hide it
                        )
                    with gr.Column(scale=15, min_width=100, visible=False) as collapsable_column:
                        with gr.Row():
                            with gr.Column(scale=1, min_width=10):

                                def delete_selected_preset(config_preset_name):
                                    if config_preset_name in config_presets.keys():
                                        del config_presets[config_preset_name]
                                        print(f'Config Presets: deleted "{config_preset_name}"')

                                        write_config_presets_to_file(config_presets, config_file_name)

                                        preset_keys = list(config_presets.keys())
                                        return gr.Dropdown.update(value=preset_keys[len(preset_keys)-1], choices=preset_keys)
                                    return gr.Dropdown.update() # do nothing if no value is selected

                                trash_button = gr.Button(
                                    value="\U0001F5D1",
                                    elem_id="config_preset_trash_button",
                                )
                                trash_button.click(
                                    fn=delete_selected_preset,
                                    inputs=[config_preset_dropdown],
                                    outputs=[config_preset_dropdown],
                                )
                            with gr.Column(scale=10, min_width=100):
                                save_textbox = gr.Textbox(
                                    label="New preset name",
                                    placeholder="Ex: Low quality",
                                    #value="My Preset",
                                    max_lines=1,
                                    elem_id="config_preset_save_textbox",
                                )
                            with gr.Column(scale=2, min_width=60):
                                save_button = gr.Button(
                                    #value="Create",
                                    value="Save & Restart",
                                    variant="primary",
                                    elem_id="config_preset_save_button",
                                )

                                save_button.click(
                                    fn=save_config(config_presets, component_map, config_file_name),
                                    inputs=list([save_textbox] + [component_map[comp_name] for comp_name in component_ids if component_map[comp_name] is not None]),
                                    #outputs=[config_preset_dropdown, save_textbox],
                                )
                                save_button.click(  # need this to runa after save_config()
                                    fn=None,
                                    _js="config_preset_settings_restart_gradio()",  # restart Gradio
                                )

                            with gr.Column(scale=2, min_width=55):
                                def open_file(f):
                                    path = os.path.normpath(f)

                                    if not os.path.exists(path):
                                        print(f'Config Presets: The file at "{path}" does not exist.')
                                        return

                                    # copied from ui.py:538
                                    if platform.system() == "Windows":
                                        os.startfile(path)
                                    elif platform.system() == "Darwin":
                                        sp.Popen(["open", path])
                                    else:
                                        sp.Popen(["xdg-open", path])

                                open_config_file_button = gr.Button(
                                    value="Open...",
                                    elem_id="config_presets_open_config_file_button",
                                )
                                open_config_file_button.click(
                                    fn=lambda: open_file(f"{BASEDIR}/{config_file_name}"),
                                    inputs=[],
                                    outputs=[],
                                )

                            with gr.Column(scale=2, min_width=50):
                                cancel_button = gr.Button(
                                    value="Cancel",
                                    elem_id="config_preset_cancel_save_button",
                                )

                    with gr.Column(scale=1, min_width=120, visible=True) as add_remove_button_column:
                        add_remove_button = gr.Button(
                            value="Add/Remove...",
                            elem_id="config_preset_add_button",
                        )


                        def add_remove_button_click():
                            return gr.update(visible=True), gr.update(visible=False)

                        def save_button_click(save_text):
                            if save_text == "":
                                return gr.update(), gr.update()
                            return gr.update(visible=True), gr.update(visible=False)

                        def cancel_button_click():
                            return gr.update(visible=True), gr.update(visible=False)

                        add_remove_button.click(
                            fn=add_remove_button_click,
                            inputs=[],
                            outputs=[collapsable_column, add_remove_button_column],
                        )
                        save_button.click(
                            fn=save_button_click,
                            inputs=[save_textbox],
                            outputs=[add_remove_button_column, collapsable_column],
                        )
                        cancel_button.click(
                            fn=cancel_button_click,
                            inputs=[],
                            outputs=[add_remove_button_column, collapsable_column],
                        )


    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass


# Save the current values on the UI to a new entry in the config file
def save_config(config_presets, component_map, config_file_name):
    #print("save_config()")
    # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
    def func(new_setting_name, *new_setting):
        #print(f"save_config() func() new_setting_name={new_setting_name} *new_setting={new_setting}")
        #print(f"config_presets()={config_presets}")
        #print(f"component_map()={component_map}")
        #print(f"config_file_name()={config_file_name}")

        if new_setting_name == "":
            return gr.Dropdown.update(), "" # do nothing if no label entered in textbox

        new_setting_map = {}    # dict[str, Any]    {"txt2img_steps": 10, ...}

        for i, component_id in enumerate(component_map.keys()):
            if component_map[component_id] is not None:
                new_setting_map[component_id] = new_setting[i]

        config_presets.update({new_setting_name: new_setting_map})
        write_config_presets_to_file(config_presets, config_file_name)

        # print(f"self.txt2img_config_preset_dropdown.choices before =\n{self.txt2img_config_preset_dropdown.choices}")
        # self.txt2img_config_preset_dropdown.choices = list(config_presets.keys())
        # print(f"self.txt2img_config_preset_dropdown.choices after =\n{self.txt2img_config_preset_dropdown.choices}")

        print(f"[Config-Presets] Added new preset: {new_setting_name}")
        print(f"[Config-Presets] Restarting UI...") # done in _js
        # update the dropdown with the new config preset, and clear the 'new preset name' textbox
        return gr.Dropdown.update(value=new_setting_name, choices=list(config_presets.keys())), ""

        # this errors when adding a 2nd config preset
        # the solution is supposed to be updating the backend Gradio object to reflect the frontend dropdown values, but it doesn't work. still throws: "ValueError: 0 is not in list"
        # workaround is to restart the whole UI after creating a new config preset by clicking the "Restart Gradio and Refresh Components" button in javascript
        # https://github.com/gradio-app/gradio/discussions/2848

    return func


def write_config_presets_to_file(config_presets, config_file_name: str):
    json_object = json.dumps(config_presets, indent=4)
    with open(f"{BASEDIR}/{config_file_name}", "w") as outfile:
        outfile.write(json_object)
