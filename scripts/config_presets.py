import modules.scripts as scripts
import modules.sd_samplers
import gradio as gr
import json
import os
import platform
import subprocess as sp


BASEDIR = scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path
CONFIG_FILE_NAME = "config.json"


class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # These are the settings from the UI that are saved for each preset
        # First value is the component label, second value is the internal name which is kept for legacy version support
        self.component_labels = {   # mirrors the config_preset_dropdown.change(output) events and config_preset_dropdown_change()
            "Sampling Steps":       {"internal_name": "steps",              "not_used_in_img2img": False},
            "Sampling method":      {"internal_name": "sampler_index",      "not_used_in_img2img": False},
            "Width":                {"internal_name": "width",              "not_used_in_img2img": False},
            "Height":               {"internal_name": "height",             "not_used_in_img2img": False},
            "Highres. fix":         {"internal_name": "enable_hr",          "not_used_in_img2img": True},
            "Firstpass width":      {"internal_name": "firstphase_width",   "not_used_in_img2img": True},
            "Firstpass height":     {"internal_name": "firstphase_height",  "not_used_in_img2img": True},
            "Denoising strength":   {"internal_name": "denoising_strength", "not_used_in_img2img": False},
            "Batch count":          {"internal_name": "batch_count",        "not_used_in_img2img": False},
            "Batch size":           {"internal_name": "batch_size",         "not_used_in_img2img": False},
            "CFG Scale":            {"internal_name": "cfg_scale",          "not_used_in_img2img": False},
        }

        # Mapping between component labels and the actual components in ui.py
        self.component_map = {k: None for k in self.component_labels}  # gets filled up in the after_component() method

        # Load config file
        try:
            with open(f"{BASEDIR}/{CONFIG_FILE_NAME}") as file:
                self.config_presets = json.load(file)
        except FileNotFoundError:
            # Config file not found
            # First time running the extension or it was deleted, so fill it with default values
            self.config_presets = {
                "Default": {
                },
                "Low quality ------ 512x512, steps: 10, batch size: 8, DPM++ 2M Karras": {
                    "steps": 10,
                    "sampler_index": "DPM++ 2M Karras",
                    "width": 512,
                    "height": 512,
                    "batch_count": 1,
                    "batch_size": 8,
                    "cfg_scale": 7
                },
                "Medium quality - 512x512, steps: 20, batch size: 8, DPM++ 2S a Karras": {
                    "steps": 20,
                    "sampler_index": "DPM++ 2S a Karras",
                    "width": 512,
                    "height": 512,
                    "batch_count": 1,
                    "batch_size": 8,
                    "cfg_scale": 7
                },
                "High quality ------ 512x512, steps: 40, batch size: 8, DPM++ 2S a Karras": {
                    "steps": 40,
                    "sampler_index": "DPM++ 2S a Karras",
                    "width": 512,
                    "height": 512,
                    "batch_count": 1,
                    "batch_size": 8,
                    "cfg_scale": 7
                },
                "High res -------- 1024x1024, steps: 30, batch size: 1, DPM++ 2M Karras, [Highres fix: 512x512, Denoising: 0.4]": {
                    "steps": 30,
                    "sampler_index": "DPM++ 2M Karras",
                    "width": 1024,
                    "height": 1024,
                    "enable_hr": "true",
                    "firstphase_width": 512,
                    "firstphase_height": 512,
                    "denoising_strength": 0.4,
                    "batch_count": 1,
                    "batch_size": 1,
                    "cfg_scale": 7
                },
                "Wallpaper ----- 1920x1088, steps: 30, batch size: 1, DPM++ 2M Karras, [Highres fix: 768x448, Denoising: 0.3]": {
                    "steps": 30,
                    "sampler_index": "DPM++ 2M Karras",
                    "width": 1920,
                    "height": 1088,
                    "enable_hr": "true",
                    "firstphase_width": 768,
                    "firstphase_height": 448,
                    "denoising_strength": 0.3,
                    "batch_count": 1,
                    "batch_size": 1,
                    "cfg_scale": 7
                }
            }

            self.write_config_presets_to_file()
            print(f"Config Presets: Config file not found, created default config at {BASEDIR}/{CONFIG_FILE_NAME}")


    def title(self):
        return "Config Presets"

    def show(self, is_img2img):
        #return True
        return scripts.AlwaysVisible    # hide this script in the Scripts dropdown

    def after_component(self, component, **kwargs):

        if component.label in self.component_map:
            self.component_map[component.label] = component
            #print(f"DEBUG: found component: {component} {component.label}")

        #if component.elem_id == "script_list": #bottom of the script dropdown
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        if component.elem_id == "open_folder": #bottom of the image gallery
            preset_values = []
            for k in self.config_presets:
                preset_values.append(k)
                #print(f"Config Presets: added \"{k}\"")


            with gr.Column(min_width=600):  # pushes our stuff onto a new row at 1080p screen resolution
                with gr.Row():
                    with gr.Column(scale=8, min_width=100) as dropdown_column:
                        def config_preset_dropdown_change(dropdown_value):
                            config_preset = self.config_presets[dropdown_value]
                            print(f"Config Presets: changed to {dropdown_value}")

                            if self.is_txt2img:
                                # if we are txt2img highres fix has a component
                                return (config_preset["steps"] if "steps" in config_preset else self.component_map["Sampling Steps"].value,
                                        config_preset["sampler_index"] if "sampler_index" in config_preset else self.component_map["Sampling method"].value,
                                        config_preset["width"] if "width" in config_preset else self.component_map["Width"].value,
                                        config_preset["height"] if "height" in config_preset else self.component_map["Height"].value,
                                        config_preset["enable_hr"] if "enable_hr" in config_preset else self.component_map["Highres. fix"].value,
                                        config_preset["firstphase_width"] if "firstphase_width" in config_preset else self.component_map["Firstpass width"].value,
                                        config_preset["firstphase_height"] if "firstphase_height" in config_preset else self.component_map["Firstpass height"].value,
                                        config_preset["denoising_strength"] if "denoising_strength" in config_preset else self.component_map["Denoising strength"].value,
                                        config_preset["batch_count"] if "batch_count" in config_preset else self.component_map["Batch count"].value,
                                        config_preset["batch_size"] if "batch_size" in config_preset else self.component_map["Batch size"].value,
                                        config_preset["cfg_scale"] if "cfg_scale" in config_preset else self.component_map["CFG Scale"].value,
                                        )

                            else:
                                # if we are img2img highres fix component is empty
                                return (config_preset["steps"] if "steps" in config_preset else self.component_map["Sampling Steps"].value,
                                        config_preset["sampler_index"] if "sampler_index" in config_preset else self.component_map["Sampling method"].value,
                                        config_preset["width"] if "width" in config_preset else self.component_map["Width"].value,
                                        config_preset["height"] if "height" in config_preset else self.component_map["Height"].value,
                                        #config_preset["enable_hr"] if "enable_hr" in config_preset else self.component_map["Highres. fix"].value,
                                        #config_preset["firstphase_width"] if "firstphase_width" in config_preset else self.component_map["Firstpass width"].value,
                                        #config_preset["firstphase_height"] if "firstphase_height" in config_preset else self.component_map["Firstpass height"].value,
                                        config_preset["denoising_strength"] if "denoising_strength" in config_preset else self.component_map["Denoising strength"].value,
                                        config_preset["batch_count"] if "batch_count" in config_preset else self.component_map["Batch count"].value,
                                        config_preset["batch_size"] if "batch_size" in config_preset else self.component_map["Batch size"].value,
                                        config_preset["cfg_scale"] if "cfg_scale" in config_preset else self.component_map["CFG Scale"].value,
                                        )


                        config_preset_dropdown = gr.Dropdown(
                            label="Config Presets",
                            choices=preset_values,
                            elem_id="config_preset_dropdown",
                        )
                        config_preset_dropdown.style(container=False) #set to True to give it a white box to sit in

                        if self.is_txt2img:
                            config_preset_dropdown.change(
                                fn=config_preset_dropdown_change,
                                show_progress=False,
                                inputs=[config_preset_dropdown],
                                outputs=[self.component_map["Sampling Steps"],
                                         self.component_map["Sampling method"],
                                         self.component_map["Width"],
                                         self.component_map["Height"],
                                         self.component_map["Highres. fix"],
                                         self.component_map["Firstpass width"],
                                         self.component_map["Firstpass height"],
                                         self.component_map["Denoising strength"],
                                         self.component_map["Batch count"],
                                         self.component_map["Batch size"],
                                         self.component_map["CFG Scale"]]
                            )
                        else:
                            config_preset_dropdown.change(
                                fn=config_preset_dropdown_change,
                                show_progress=False,
                                inputs=[config_preset_dropdown],
                                #outputs = list([self.component_map[e] for e in AVAILABLE_COMPONENTS if e != "Seeds" and e != "Highres. fix"]) # **** LIST COMPS FAIL W/ GRADIO'S IN/OUTPUTS
                                outputs=[self.component_map["Sampling Steps"],
                                         self.component_map["Sampling method"],
                                         self.component_map["Width"],
                                         self.component_map["Height"],
                                         #self.component_map["Highres. fix"],   no highres fix in img2img
                                         #self.component_map["Firstpass width"],
                                         #self.component_map["Firstpass height"],
                                         self.component_map["Denoising strength"],
                                         self.component_map["Batch count"],
                                         self.component_map["Batch size"],
                                         self.component_map["CFG Scale"]]
                                )

                        config_preset_dropdown.change(
                            fn=None,
                            inputs=[],
                            outputs=[],
                            _js="function() { config_preset_dropdown_change() }",   # JS is used to update the Highres fix row to show/hide it
                        )
                    with gr.Column(scale=15, min_width=100, visible=False) as collapsable_column:
                        with gr.Row():
                            with gr.Column(scale=1, min_width=10):

                                def delete_selected_preset(config_preset_name):
                                    if config_preset_name in self.config_presets.keys():
                                        del self.config_presets[config_preset_name]
                                        print(f'Config Presets: deleted "{config_preset_name}"')

                                        self.write_config_presets_to_file()

                                        preset_keys = list(self.config_presets.keys())
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
                            with gr.Column(scale=2, min_width=50):
                                save_button = gr.Button(
                                    value="Create",
                                    variant="primary",
                                    elem_id="config_preset_save_button",
                                )
                                save_button.click(
                                    fn=self.save_config(),
                                    inputs=list([save_textbox] + [self.component_map[comp_name] for comp_name in self.component_labels if self.component_map[comp_name] is not None]),
                                    outputs=[config_preset_dropdown, save_textbox],
                                )

                            with gr.Column(scale=2, min_width=50):
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
                                    fn=lambda: open_file(f"{BASEDIR}/{CONFIG_FILE_NAME}"),
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
    # Gerschel came up with the idea for this code trick
    def save_config(self):
        # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
        def func(new_setting_name, *new_setting):
            #print(f"save_config() func() new_setting_name={new_setting_name} *new_setting={new_setting}")
            #print(f"new_setting_name={new_setting_name}")

            if new_setting_name == "":
                return gr.Dropdown.update(), "" # do nothing if no label entered in textbox

            new_setting_map = {}

            j = 0
            for i, k in enumerate(self.component_labels):
                #print(f"i={i}, j={j} k={k}")  # i=1,2,3... k="Sampling Steps", "Sampling methods", ...

                if self.is_img2img and self.component_labels[k]["not_used_in_img2img"] == True:
                    #if we're in the img2img tab, skip Highres. fix, Firstpass width, Firstpass height
                    #print(f"{k} is not in the img2img tab, skipping")
                    continue

                if self.component_map[k] is not None:
                    internal_name = self.component_labels[k]["internal_name"]
                    new_value = new_setting[j]
                    #print(f"internal_name={internal_name}, new_value={new_value}")
                    if k != "Sampling method":
                        new_setting_map[internal_name] = new_value
                    else:
                        if self.is_txt2img:
                            new_setting_map[internal_name] = modules.sd_samplers.samplers[new_value].name
                        else:
                            new_setting_map[internal_name] = modules.sd_samplers.samplers_for_img2img[new_value].name

                j += 1

            self.config_presets.update({new_setting_name: new_setting_map})

            self.write_config_presets_to_file()

            #print(f"new dropdown values: {list(self.config_presets.keys())}")
            # update the dropdown with the new config preset, clear the 'new preset name' textbox
            return gr.Dropdown.update(value=new_setting_name, choices=list(self.config_presets.keys())), ""

        return func



    def write_config_presets_to_file(self):
        json_object = json.dumps(self.config_presets, indent=4)
        with open(f"{BASEDIR}/{CONFIG_FILE_NAME}", "w") as outfile:
            outfile.write(json_object)
    