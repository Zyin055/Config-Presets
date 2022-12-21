import time

import modules.scripts as scripts
import modules.sd_samplers
import gradio as gr
import json
import os
import platform
import subprocess as sp
import logging
from pprint import pprint as pp

#logging.basicConfig(level=logging.DEBUG)


basedir = scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path


def write_config_presets_to_file(config_presets):
    json_object = json.dumps(config_presets, indent=4)
    with open(f"{basedir}/config.json", "w") as outfile:
        outfile.write(json_object)

class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        #self.basedir = scripts.basedir()     #C:\Stable Diffusion      #use at global instead to get the extra 'extensions\Config-Presets' path.

        # self.component_labels = [
        #     "Sampling Steps",
        #     "Sampling method",
        #     "Width",
        #     "Height",
        #     "Highres. fix",
        #     "Firstpass width",
        #     "Firstpass height",
        #     "Denoising strength",
        #     "Batch count",
        #     "Batch size",
        #     "CFG Scale",
        # ]
        self.component_labels = {
            "Sampling Steps": "steps",
            "Sampling method": "sampler_index",
            "Width": "width",
            "Height": "height",
            "Highres. fix": "enable_hr",
            "Firstpass width": "firstphase_width",
            "Firstpass height": "firstphase_height",
            "Denoising strength": "denoising_strength",
            "Batch count": "batch_count",
            "Batch size": "batch_size",
            "CFG Scale": "cfg_scale",
        }
        self.component_map = {k: None for k in self.component_labels}  # gets filled up in after_component()
        #print(f"init self.component_map={self.component_map}")
        self.settings_file = "config.json"
        self.save_as = gr.Text(render=False)

        # Load config from file
        try:
            with open(f"{basedir}/config.json") as file:
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
            write_config_presets_to_file()
            print(f"Config Presets: Config file not found, created default config at {basedir}/config.json")


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
                            #print(f"config_preset_dropdown_change(dropdown_value={dropdown_value})")
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
                        if self.component_map["Highres. fix"]:
                            config_preset_dropdown.change(
                                fn=config_preset_dropdown_change,
                                show_progress=False,
                                inputs=[config_preset_dropdown],
                                #outputs=[ui_steps, ui_sampler_index, ui_width, ui_height, ui_enable_hr, ui_denoising_strength, ui_batch_count, ui_batch_size, ui_cfg_scale],
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
                    with gr.Column(scale=15, min_width=100, visible=False) as save_column:
                        with gr.Row():
                            with gr.Column(scale=1, min_width=10):

                                def delete_selected_preset(config_preset_name):
                                    if config_preset_name in self.config_presets.keys():

                                        del self.config_presets[config_preset_name]
                                        print(f'Config Presets: deleted "{config_preset_name}"')
                                        #print(f"new self.config_presets={self.config_presets}")

                                        write_config_presets_to_file(self.config_presets)

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

                                open_config_file_button = gr.Button(  # tooltip is set in javascript/config_presets.js
                                    value="Open...",
                                    elem_id="config_presets_open_config_file_button",
                                    # visible=False,
                                )
                                open_config_file_button.click(
                                    fn=lambda: open_file(f"{basedir}/config.json"),
                                    inputs=[],
                                    outputs=[],
                                )

                            with gr.Column(scale=2, min_width=50):
                                cancel_button = gr.Button(
                                    value="Cancel",
                                    elem_id="config_preset_cancel_save_button",
                                )

                    with gr.Column(scale=1, min_width=120, visible=True) as add_column:
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
                            outputs=[save_column, add_column],
                        )
                        save_button.click(
                            fn=save_button_click,
                            inputs=[save_textbox],
                            outputs=[add_column, save_column],
                        )
                        cancel_button.click(
                            fn=cancel_button_click,
                            inputs=[],
                            outputs=[add_column, save_column],
                        )




                    #with gr.Column(scale=1, min_width=30) as edit_column:

    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass

    def save_config(self):
        """
            Helper function to utilize closure
        """


        # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
        def func(new_setting_name, *new_setting):
            """
                Formats setting and overwrites file
                input: setting_name is text autoformatted from clicks input
                       new_settings is a tuple (by using packing) of formatted text, outputs from
                            click method must be in same order of labels
            """

            print(f"save_config() in python")
            #print(f"save_config() func() setting_name={setting_name} *new_setting={new_setting}")

            if new_setting_name == "":
                return gr.Dropdown.update(), "" # do nothing

            # Format new_setting from tuple of values, and map them to their label
            # Using presence of hires button to determine if we are img2img or txt2img
            # if self.is_txt2img:
            #     new_setting = {k:new_setting[i] if k != "Sampling method" else modules.sd_samplers.samplers[new_setting[i]].name for i, k in enumerate(self.component_labels) if self.component_map[k] is not None}
            # else:
            #     new_setting = {k:new_setting[i] if k != "Sampling method" else modules.sd_samplers.samplers_for_img2img[new_setting[i]].name for i, k in enumerate(self.component_labels) if self.component_map[k] is not None}

            new_setting_map = {}

            for i, k in enumerate(self.component_labels):
                #print(f"i={i}, k={k}")  # i=1,2,3... k="Sampling Steps", "Sampling methods", etc
                if self.component_map[k] is not None:
                    internal_name = self.component_labels[k]
                    new_value = new_setting[i]
                    #print(f"internal_name={internal_name}, new_value={new_value}")
                    if k != "Sampling method":
                        #pass
                        new_setting_map[internal_name] = new_value
                    else:
                        if self.is_txt2img:
                            new_setting_map[internal_name] = modules.sd_samplers.samplers[new_value].name
                        else:
                            new_setting_map[internal_name] = modules.sd_samplers.samplers_for_img2img[new_value].name

            print(f"new_setting_name={new_setting_name}")
            self.config_presets.update({new_setting_name: new_setting_map})

            write_config_presets_to_file(self.config_presets)

            #print(f"new dropdown values: {list(self.config_presets.keys())}")
            return gr.Dropdown.update(value=new_setting_name, choices=list(self.config_presets.keys())), ""


        return func
