# Config Presets script for Automatic1111
# Last updated: 12/13/2022
# Author: Zyin

import modules.scripts
import gradio as gr
import ast
import os
import platform
import subprocess as sp


ui_steps = None                  # "steps" component in ui.py:635, label='Sampling Steps'
ui_sampler_index = None          # "steps" component in ui.py:636, label='Sampling method'
ui_width = None                  # "width" component in ui.py:639, label='Width'
ui_height = None                 # "height" component in ui.py:640, label='Height'
ui_enable_hr = None              # "enable_hr" component in ui.py:645,label='Highres. fix'
ui_denoising_strength = None     # "denoising_strength" component in ui.py:650, label='Denoising strength'
ui_batch_count = None            # "batch_count" component in ui.py:653, label='Batch count'
ui_batch_size = None             # "batch_size" component in ui.py:654, label='Batch size'
ui_cfg_scale = None              # "cfg_scale" component in ui.py:656, label='CFG Scale'

#print(f"global modules.scripts.basedir()={modules.scripts.basedir()}")
basedir = modules.scripts.basedir()     #C:\Stable Diffusion\extensions\Config-Presets

# Load config from file
config_presets = {}
try:
    with open(f"{basedir}/config.json") as file:
        config_presets = ast.literal_eval(file.read())
        #print("Config Presets: loaded config file 'config.json'")
except FileNotFoundError:
    print(f"[ERROR] Config Presets: Could not find config file at '{basedir}/config.json'. The Config Presets dropdown will not work!")



class Script(modules.scripts.Script):
    def title(self):
        return "Config Presets"

    def show(self, is_img2img):
        #return True
        return modules.scripts.AlwaysVisible    # hide this script in the Scripts dropdown

    def after_component(self, component, **kwargs):
        global ui_steps
        global ui_sampler_index
        global ui_width
        global ui_height
        global ui_enable_hr
        global ui_denoising_strength
        global ui_batch_count
        global ui_batch_size
        global ui_cfg_scale

        # Since we can't get direct access to component variables in ui.py, we detect and save an old reference to them here.
        if isinstance(component, gr.components.Slider):
            if component.label == "Sampling Steps":
                ui_steps = component
                #print(f"found ui_steps component: {type(component)}")
            elif component.label == "Width":
                ui_width = component
                #print(f"found ui_width component: {type(component)}")
            elif component.label == "Height":
                ui_height = component
                #print(f"found ui_height component: {type(component)}")
            elif component.label == "Denoising strength":
                ui_denoising_strength = component
                #print(f"found ui_denoising_strength component: {type(component)}")
            elif component.label == "Batch count":
                ui_batch_count = component
                #print(f"found ui_batch_count component: {type(component)}")
            elif component.label == "Batch size":
                ui_batch_size = component
                #print(f"found ui_batch_size component: {type(component)}")
            elif component.label == "CFG Scale":
                ui_cfg_scale = component
                #print(f"found ui_cfg_scale component: {type(component)}")
        elif isinstance(component, gr.components.Checkbox):
            if component.label == "Highres. fix":
                ui_enable_hr = component
                #print(f"found ui_enable_hr component: {type(component)}")
        elif isinstance(component, gr.components.Radio):
            if component.label == "Sampling method":
                ui_sampler_index = component
                #print(f"found ui_sampler_index component: {type(component)}")


        #if component.elem_id == "script_list": #bottom of the script dropdown
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        if component.elem_id == "open_folder": #bottom of the image gallery
            global config_presets
            preset_values = []
            for k in config_presets:
                preset_values.append(k)
                #print(f"Config Presets: added \"{k}\"")


            with gr.Column(scale=9):
                def config_preset_dropdown_change(dropdown_value):
                    global config_presets
                    config_preset = config_presets[dropdown_value]
                    print(f"Config Presets: changed to {dropdown_value}")

                    # return config_dict["steps"] if "steps" in config_dict else 20,\
                    #        config_dict["sampler_index"] if "sampler_index" in config_dict else "Euler a",\
                    #        config_dict["width"] if "width" in config_dict else 512,\
                    #        config_dict["height"] if "height" in config_dict else 512,\
                    #        config_dict["enable_hr"] if "enable_hr" in config_dict else False,\
                    #        config_dict["denoising_strength"] if "denoising_strength" in config_dict else 0.7,\
                    #        config_dict["batch_count"] if "batch_count" in config_dict else 1,\
                    #        config_dict["batch_size"] if "batch_size" in config_dict else 1,\
                    #        config_dict["cfg_scale"] if "cfg_scale" in config_dict else 7,\

                    # I couldn't find a way to get up-to-date values from the UI elements, so instead we just use the default values if something is missing from the config file

                    return config_preset["steps"] if "steps" in config_preset else ui_steps.value,\
                           config_preset["sampler_index"] if "sampler_index" in config_preset else ui_sampler_index.value,\
                           config_preset["width"] if "width" in config_preset else ui_width.value,\
                           config_preset["height"] if "height" in config_preset else ui_height.value,\
                           config_preset["enable_hr"] if "enable_hr" in config_preset else ui_enable_hr.value,\
                           config_preset["denoising_strength"] if "denoising_strength" in config_preset else ui_denoising_strength.value,\
                           config_preset["batch_count"] if "batch_count" in config_preset else ui_batch_count.value,\
                           config_preset["batch_size"] if "batch_size" in config_preset else ui_batch_size.value,\
                           config_preset["cfg_scale"] if "cfg_scale" in config_preset else ui_cfg_scale.value,\

                config_preset_dropdown = gr.Dropdown(
                    label="Config Presets",
                    choices=preset_values,
                    elem_id="config_preset_dropdown",
                )
                config_preset_dropdown.style(container=False) #set to True to give it a white box to sit in
                config_preset_dropdown.change(
                    fn=config_preset_dropdown_change,
                    show_progress=False,
                    inputs=[config_preset_dropdown],
                    outputs=[ui_steps, ui_sampler_index, ui_width, ui_height, ui_enable_hr, ui_denoising_strength, ui_batch_count, ui_batch_size, ui_cfg_scale],
                )
                config_preset_dropdown.change(
                    fn=None,
                    inputs=[],
                    outputs=[],
                    _js="function() { config_preset_dropdown_change() }",
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

                #print(f"modules.scripts.basedir()={modules.scripts.basedir()}")    # base SD folder

                open_config_file_button = gr.Button(    #tooltip is set in javascript/config_presets.js
                    value="Edit...",
                    elem_id="config_presets_open_config_file_button"
                )
                open_config_file_button.click(
                    fn=lambda: open_file(f"{basedir}\\config.json"),
                    inputs=[],
                    outputs=[],
                )

    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass
