"""
    Project started by Zyin055, and co-authored by Gerschel
"""
import modules.scripts as scripts
import modules.sd_samplers
import gradio as gr
import json
import os
import platform
import subprocess as sp
import logging
from pprint import pprint as pp

logging.basicConfig(level=logging.DEBUG)


basedir = scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path


class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.basedir = scripts.basedir()     #C:\Stable Diffusion      #use at global instead to get the extra 'extensions\Config-Presets' path.

        self.component_labels = [
            "Sampling Steps",
            "Sampling method",
            "Width",
            "Height",
            "Highres. fix",
            "Firstpass width",
            "Firstpass height",
            "Denoising strength",
            "Batch count",
            "Batch size",
            "CFG Scale",
        ]
        self.component_map = {k: None for k in self.component_labels}    # gets filled up in after_component()
        self.settings_file = "config.json"
        self.save_as = gr.Text(render=False)

        #Load config from file
        self.config_presets = self.get_config(self.settings_file)

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

            with gr.Column(scale=8):
                def config_preset_dropdown_change(dropdown_value):
                    config_preset = self.config_presets[dropdown_value]
                    print(f"Config Presets: changed to {dropdown_value}")

                    if self.component_map["Highres. fix"]:
                        # if we are txt2img highres fix has a component
                        return (config_preset["Sampling Steps"] if "Sampling Steps" in config_preset else self.component_map["Sampling Steps"].value,
                                config_preset["Sampling method"] if "Sampling method" in config_preset else self.component_map["Sampling method"].value,
                                config_preset["Width"] if "Width" in config_preset else self.component_map["Width"].value,
                                config_preset["Height"] if "Height" in config_preset else self.component_map["Height"].value,
                                config_preset["Highres. fix"] if "Highres. fix" in config_preset else self.component_map["Highres. fix"].value,
                                config_preset["Firstpass width"] if "Firstpass width" in config_preset else self.component_map["Firstpass width"].value,
                                config_preset["Firstpass height"] if "Firstpass height" in config_preset else self.component_map["Firstpass height"].value,
                                config_preset["Denoising strength"] if "Denoising strength" in config_preset else self.component_map["Denoising strength"].value,
                                config_preset["Batch count"] if "Batch count" in config_preset else self.component_map["Batch count"].value,
                                config_preset["Batch size"] if "Batch size" in config_preset else self.component_map["Batch size"].value,
                                config_preset["CFG Scale"] if "CFG Scale" in config_preset else self.component_map["CFG Scale"].value,
                                )
                        
                    else:
                        # if we are img2img highres fix component is empty
                        return (config_preset["Sampling Steps"] if "Sampling Steps" in config_preset else self.component_map["Sampling Steps"].value,
                                config_preset["Sampling method"] if "Sampling method" in config_preset else self.component_map["Sampling method"].value,
                                config_preset["Width"] if "Width" in config_preset else self.component_map["Width"].value,
                                config_preset["Height"] if "Height" in config_preset else self.component_map["Height"].value,
                                #config_preset["Highres. fix"] if "Highres. fix" in config_preset else self.component_map["Highres. fix"].value,
                                #config_preset["Firstpass width"] if "Firstpass width" in config_preset else self.component_map["Firstpass width"].value,
                                #config_preset["Firstpass height"] if "Firstpass height" in config_preset else self.component_map["Firstpass height"].value,
                                config_preset["Denoising strength"] if "Denoising strength" in config_preset else self.component_map["Denoising strength"].value,
                                config_preset["Batch count"] if "Batch count" in config_preset else self.component_map["Batch count"].value,
                                config_preset["Batch size"] if "Batch size" in config_preset else self.component_map["Batch size"].value,
                                config_preset["CFG Scale"] if "CFG Scale" in config_preset else self.component_map["CFG Scale"].value,
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
            with gr.Column(scale=1, min_width=30):
                save_button = gr.Button(
                    value = "Save",
                    variant = "primary"
                )

                save_button.click(
                    fn = self.save_config(path=self.settings_file),
                    inputs = list([config_preset_dropdown, self.save_as] + [self.component_map[comp_name] for comp_name in self.component_labels if self.component_map[comp_name] is not None]),
                    #outputs = config_preset_dropdown
                )
            with gr.Column(scale=1, min_width=30):
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

                open_config_file_button = gr.Button(    # tooltip is set in javascript/config_presets.js
                    value="Edit...",
                    elem_id="config_presets_open_config_file_button"
                )
                open_config_file_button.click(
                    fn=lambda: open_file(f"{basedir}\\config.json"),
                    inputs=[],
                    outputs=[],
                )

        if component.elem_id == "script_list": # Temporary place until you figure out where you want it
            self.save_as.render()

    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass

    def save_config(self, path):
        """
            Helper function to utilize closure
        """

        # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
        def func(dropdown_component, setting_name, *new_setting):
            """
                Formats setting and overwrites file
                input: setting_name is text autoformatted from clicks input
                       new_settings is a tuple (by using packing) of formatted text, outputs from
                            click method must be in same order of labels
            """
            # Format new_setting from tuple of values, and map them to their label
            # Using presence of hires button to determine if we are img2img or txt2img
            if self.component_map["Highres. fix"]:
                new_setting = {k:new_setting[i] if k != "Sampling method" else modules.sd_samplers.samplers[new_setting[i]].name for i, k in enumerate(self.component_labels) if self.component_map[k] is not None}
            else:
                new_setting = {k:new_setting[i] if k != "Sampling method" else modules.sd_samplers.samplers_for_img2img[new_setting[i]].name for i, k in enumerate(self.component_labels) if self.component_map[k] is not None}
            file = os.path.join(basedir, path)
            self.config_presets.update({setting_name : new_setting})
            #dropdown_component.choices = [self.config_presets.keys()]
            logging.debug(self.config_presets.keys())
            #logging.debug(self.dropdown_components.choices)
            
            with open(file, "w") as f:
                json.dump(self.config_presets, f, indent=4)
            return gr.Dropdown.update(choices = self.config_presets.keys())
        return func
        
        
    def get_config(self, path, open_mode='r'):
        file = os.path.join(basedir, path)
        try:
            with open(file, open_mode) as f:
                as_dict = json.load(f) 
        except FileNotFoundError:
            print(f"[ERROR] Config Presets: Could not find config file at '{file}'. The Config Presets dropdown will not work!")
        return as_dict