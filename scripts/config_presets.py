import traceback
import modules.sd_samplers
import modules.scripts as scripts
import gradio as gr
import json
import os
import platform
import subprocess as sp


BASEDIR = scripts.basedir()     #C:\path\to\Stable Diffusion\extensions\Config-Presets   needs to be set in global space to get the extra 'extensions\Config-Presets' path
CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = "config-txt2img-custom-tracked-components.txt"
CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME = "config-img2img-custom-tracked-components.txt"
CONFIG_TXT2IMG_FILE_NAME = "config-txt2img.json"
CONFIG_IMG2IMG_FILE_NAME = "config-img2img.json"


def load_txt2img_custom_tracked_component_ids() -> list[str]:
    txt2img_custom_tracked_components_ids = []
    try:
        with open(f"{BASEDIR}/{CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME}", "r") as file:
            for line in file:
                line = line.strip()
                if not line.startswith("#") and line != "":  # ignore lines that start with # or are empty
                    txt2img_custom_tracked_components_ids.append(line)
                    #print(f"Added txt2img custom tracked component: {line}")

    except FileNotFoundError:
        # config file not found
        # First time running the extension or it was deleted, so fill it with default values
        txt2img_custom_tracked_components_default_text = """# Put custom txt2img tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
# Component IDs can be found in the HTML (id="..."), in modules/ui.py (elem_id="..."), or in an extensions python code. IDs like "component-5890" won't work because the number at the end will change each startup.
# Entering an invalid component ID here will cause this extension to error and not load. Components that do not have a value associated with them, such as tabs and accordions, are not supported.
# Note that components on the top row of the UI cannot be added here, such as "setting_sd_model_checkpoint", "setting_sd_vae", and "setting_CLIP_stop_at_last_layers".

# Other fields:
#txt2img_prompt
#txt2img_neg_prompt
#txt2img_styles
#txt2img_subseed_show
#txt2img_subseed
#txt2img_subseed_strength
#txt2img_seed_resize_from_w
#txt2img_seed_resize_from_h
#txt2img_tiling
#txt2img_hr_resize_x
#txt2img_hr_resize_y
#hr_sampler
#hires_prompt
#hires_neg_prompt

# Script dropdown:
#script_list

# X/Y/Z plot (script):
#script_txt2img_xyz_plot_x_type
#script_txt2img_xyz_plot_y_type
#script_txt2img_xyz_plot_z_type
#script_txt2img_xyz_plot_x_values
#script_txt2img_xyz_plot_y_values
#script_txt2img_xyz_plot_z_values

# Latent Couple (extension):
#cd_txt2img_divisions
#cd_txt2img_positions
#cd_txt2img_weights
#cd_txt2img_end_at_this_step

# ControlNet (extension):
#txt2img_controlnet_ControlNet-0_controlnet_enable_checkbox
#txt2img_controlnet_ControlNet-0_controlnet_low_vram_checkbox
#txt2img_controlnet_ControlNet-0_controlnet_pixel_perfect_checkbox
#txt2img_controlnet_ControlNet-0_controlnet_preprocessor_preview_checkbox
#txt2img_controlnet_ControlNet-0_controlnet_preprocessor_dropdown
#txt2img_controlnet_ControlNet-0_controlnet_model_dropdown
#txt2img_controlnet_ControlNet-0_controlnet_control_weight_slider
#txt2img_controlnet_ControlNet-0_controlnet_start_control_step_slider
#txt2img_controlnet_ControlNet-0_controlnet_ending_control_step_slider
#txt2img_controlnet_ControlNet-0_controlnet_control_mode_radio
#txt2img_controlnet_ControlNet-0_controlnet_resize_mode_radio
#txt2img_controlnet_ControlNet-0_controlnet_automatically_send_generated_images_checkbox

#txt2img_controlnet_ControlNet-1_controlnet_enable_checkbox
#txt2img_controlnet_ControlNet-1_controlnet_low_vram_checkbox
#txt2img_controlnet_ControlNet-1_controlnet_pixel_perfect_checkbox
#txt2img_controlnet_ControlNet-1_controlnet_preprocessor_preview_checkbox
#txt2img_controlnet_ControlNet-1_controlnet_preprocessor_dropdown
#txt2img_controlnet_ControlNet-1_controlnet_model_dropdown
#txt2img_controlnet_ControlNet-1_controlnet_control_weight_slider
#txt2img_controlnet_ControlNet-1_controlnet_start_control_step_slider
#txt2img_controlnet_ControlNet-1_controlnet_ending_control_step_slider
#txt2img_controlnet_ControlNet-1_controlnet_control_mode_radio
#txt2img_controlnet_ControlNet-1_controlnet_resize_mode_radio
#txt2img_controlnet_ControlNet-1_controlnet_automatically_send_generated_images_checkbox

#txt2img_controlnet_ControlNet-2_controlnet_enable_checkbox
#txt2img_controlnet_ControlNet-2_controlnet_low_vram_checkbox
#txt2img_controlnet_ControlNet-2_controlnet_pixel_perfect_checkbox
#txt2img_controlnet_ControlNet-2_controlnet_preprocessor_preview_checkbox
#txt2img_controlnet_ControlNet-2_controlnet_preprocessor_dropdown
#txt2img_controlnet_ControlNet-2_controlnet_model_dropdown
#txt2img_controlnet_ControlNet-2_controlnet_control_weight_slider
#txt2img_controlnet_ControlNet-2_controlnet_start_control_step_slider
#txt2img_controlnet_ControlNet-2_controlnet_ending_control_step_slider
#txt2img_controlnet_ControlNet-2_controlnet_control_mode_radio
#txt2img_controlnet_ControlNet-2_controlnet_resize_mode_radio
#txt2img_controlnet_ControlNet-2_controlnet_automatically_send_generated_images_checkbox

# Tiled Diffusion (extension)
#MD-t2i-enabled
#MD-t2i-overwrite-image-size
#MD-overwrite-width-t2i
#MD-overwrite-height-t2i
#MD-t2i-method
#MD-t2i-control-tensor-cpu
#MD-t2i-latent-tile-width
#MD-t2i-latent-tile-height
#MD-t2i-latent-tile-overlap
#MD-t2i-latent-tile-batch-size
# Tiled Diffusion - Region Prompt Control
#MD-t2i-enable-bbox-control
#MD-t2i-draw-background
#MD-t2i-cfg-name
# Tiled Diffusion - Region Prompt Control - Region 1
#MD-bbox-t2i-0-enable
#MD-t2i-0-blend-mode
#MD-t2i-0-feather
#MD-t2i-0-x
#MD-t2i-0-y
#MD-t2i-0-w
#MD-t2i-0-h
#MD-t2i-0-prompt
#MD-t2i-0-neg-prompt
#MD-t2i-0-seed
# Tiled Diffusion - Region Prompt Control - Region 2
#MD-bbox-t2i-1-enable
#MD-t2i-1-blend-mode
#MD-t2i-1-feather
#MD-t2i-1-x
#MD-t2i-1-y
#MD-t2i-1-w
#MD-t2i-1-h
#MD-t2i-1-prompt
#MD-t2i-1-neg-prompt
#MD-t2i-1-seed
# Tiled Diffusion - Region Prompt Control - Region 3
#MD-bbox-t2i-2-enable
#MD-t2i-2-blend-mode
#MD-t2i-2-feather
#MD-t2i-2-x
#MD-t2i-2-y
#MD-t2i-2-w
#MD-t2i-2-h
#MD-t2i-2-prompt
#MD-t2i-2-neg-prompt
#MD-t2i-2-seed
# Tiled Diffusion - Tiled VAE
#tiledvae-t2i-enable
#tiledvae-t2i-vae2gpu
#tiledvae-t2i-enc-size
#tiledvae-t2i-dec-size
#tiledvae-t2i-fastenc
#tiledvae-t2i-fastenc-colorfix
#tiledvae-t2i-fastdec

# ADetailer (extension)
#script_txt2img_adetailer_ad_enable
# ADetailer - 1st tab
#script_txt2img_adetailer_ad_model
#script_txt2img_adetailer_ad_prompt
#script_txt2img_adetailer_ad_negative_prompt
# ADetailer - 1st tab - Detection
#script_txt2img_adetailer_ad_confidence
#script_txt2img_adetailer_ad_mask_min_ratio
#script_txt2img_adetailer_ad_mask_max_ratio
# ADetailer - 1st tab - Mask Preprocessing
#script_txt2img_adetailer_ad_x_offset
#script_txt2img_adetailer_ad_y_offset
#script_txt2img_adetailer_ad_dilate_erode
#script_txt2img_adetailer_ad_mask_merge_invert
# ADetailer - 1st tab - Inpainting
#script_txt2img_adetailer_ad_mask_blur
#script_txt2img_adetailer_ad_denoising_strength
#script_txt2img_adetailer_ad_inpaint_full_res
#script_txt2img_adetailer_ad_inpaint_full_res_padding
#script_txt2img_adetailer_ad_use_inpaint_width_height
#script_txt2img_adetailer_ad_inpaint_width
#script_txt2img_adetailer_ad_inpaint_height
#script_txt2img_adetailer_ad_use_steps
#script_txt2img_adetailer_ad_steps
#script_txt2img_adetailer_ad_use_cfg_scale
#script_txt2img_adetailer_ad_cfg_scale
#script_txt2img_adetailer_ad_restore_face
# ADetailer - 1st tab - ControlNet
#script_txt2img_adetailer_ad_controlnet_model
#script_txt2img_adetailer_ad_controlnet_weight
#script_txt2img_adetailer_ad_controlnet_guidance_start
#script_txt2img_adetailer_ad_controlnet_guidance_end
# ADetailer - 2nd tab
#script_txt2img_adetailer_ad_model_2nd
#script_txt2img_adetailer_ad_prompt_2nd
#script_txt2img_adetailer_ad_negative_prompt_2nd
# ADetailer - 2nd tab - Detection
#script_txt2img_adetailer_ad_confidence_2nd
#script_txt2img_adetailer_ad_mask_min_ratio_2nd
#script_txt2img_adetailer_ad_mask_max_ratio_2nd
# ADetailer - 2nd tab - Mask Preprocessing
#script_txt2img_adetailer_ad_x_offset_2nd
#script_txt2img_adetailer_ad_y_offset_2nd
#script_txt2img_adetailer_ad_dilate_erode_2nd
#script_txt2img_adetailer_ad_mask_merge_invert_2nd
# ADetailer - 2nd tab - Inpainting
#script_txt2img_adetailer_ad_mask_blur_2nd
#script_txt2img_adetailer_ad_denoising_strength_2nd
#script_txt2img_adetailer_ad_inpaint_full_res_2nd
#script_txt2img_adetailer_ad_inpaint_full_res_padding_2nd
#script_txt2img_adetailer_ad_use_inpaint_width_height_2nd
#script_txt2img_adetailer_ad_inpaint_width_2nd
#script_txt2img_adetailer_ad_inpaint_height_2nd
#script_txt2img_adetailer_ad_use_steps_2nd
#script_txt2img_adetailer_ad_steps_2nd
#script_txt2img_adetailer_ad_use_cfg_scale_2nd
#script_txt2img_adetailer_ad_cfg_scale_2nd
#script_txt2img_adetailer_ad_restore_face_2nd
# ADetailer - 2nd tab - ControlNet
#script_txt2img_adetailer_ad_controlnet_model_2nd
#script_txt2img_adetailer_ad_controlnet_weight_2nd
#script_txt2img_adetailer_ad_controlnet_guidance_start_2nd
#script_txt2img_adetailer_ad_controlnet_guidance_end_2nd
"""

        write_text_to_file(txt2img_custom_tracked_components_default_text, CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME)
        print(f"[Config Presets] txt2img custom tracked components config file not found, created default config at {BASEDIR}/{CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME}")

    return txt2img_custom_tracked_components_ids



def load_img2img_custom_tracked_component_ids() -> list[str]:
    img2img_custom_tracked_components_ids = []
    try:
        with open(f"{BASEDIR}/{CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME}", "r") as file:
            for line in file:
                line = line.strip()
                if not line.startswith("#") and line != "":  # ignore lines that start with # or are empty
                    img2img_custom_tracked_components_ids.append(line)
                    #print(f"Added img2img custom tracked component: {line}")

    except FileNotFoundError:
        # config file not found
        # First time running the extension or it was deleted, so fill it with default values
        img2img_custom_tracked_components_ids = """# Put custom img2img tracked component IDs here. This will allow those fields to be saved as a config preset.
# Lines starting with a # are ignored.
# Component IDs can be found in the HTML (id="..."), in modules/ui.py (elem_id="..."), or in an extensions python code. IDs like "component-5890" won't work because the number at the end will change each startup.
# Entering an invalid component ID here will cause this extension to error and not load. Components that do not have a value associated with them, such as tabs and accordions, are not supported.
# Note that components on the top row of the UI cannot be added here, such as "setting_sd_model_checkpoint", "setting_sd_vae", and "setting_CLIP_stop_at_last_layers".

# Other fields:
#img2img_prompt
#img2img_neg_prompt
#img2img_mask_mode
#img2img_mask_blur
#img2img_mask_alpha
#img2img_inpainting_fill
#img2img_inpaint_full_res
#img2img_inpaint_full_res_padding
#resize_mode
#img2img_scale
#img2img_seed
#img2img_subseed_show
#img2img_subseed
#img2img_subseed_strength
#img2img_seed_resize_from_w
#img2img_seed_resize_from_h
#img2img_tiling
#img2img_batch_input_dir
#img2img_batch_output_dir
#img2img_batch_inpaint_mask_dir

# Script dropdown:
#script_list

# X/Y/Z plot (script):
#script_img2img_xyz_plot_x_type
#script_img2img_xyz_plot_y_type
#script_img2img_xyz_plot_z_type
#script_img2img_xyz_plot_x_values
#script_img2img_xyz_plot_y_values
#script_img2img_xyz_plot_z_values

# Loopback (script):
#script_loopback_loops
#script_loopback_final_denoising_strength

# SD upscale (script):
#script_sd_upscale_overlap
#script_sd_upscale_scale_factor
#script_sd_upscale_upscaler_index

# Latent Couple (extension):
#cd_img2img_divisions
#cd_img2img_positions
#cd_img2img_weights
#cd_img2img_end_at_this_step

# ControlNet (extension):
#img2img_controlnet_ControlNet-0_controlnet_enable_checkbox
#img2img_controlnet_ControlNet-0_controlnet_low_vram_checkbox
#img2img_controlnet_ControlNet-0_controlnet_pixel_perfect_checkbox
#img2img_controlnet_ControlNet-0_controlnet_preprocessor_preview_checkbox
#img2img_controlnet_ControlNet-0_controlnet_preprocessor_dropdown
#img2img_controlnet_ControlNet-0_controlnet_model_dropdown
#img2img_controlnet_ControlNet-0_controlnet_control_weight_slider
#img2img_controlnet_ControlNet-0_controlnet_start_control_step_slider
#img2img_controlnet_ControlNet-0_controlnet_ending_control_step_slider
#img2img_controlnet_ControlNet-0_controlnet_control_mode_radio
#img2img_controlnet_ControlNet-0_controlnet_resize_mode_radio
#img2img_controlnet_ControlNet-0_controlnet_automatically_send_generated_images_checkbox

#img2img_controlnet_ControlNet-1_controlnet_enable_checkbox
#img2img_controlnet_ControlNet-1_controlnet_low_vram_checkbox
#img2img_controlnet_ControlNet-1_controlnet_pixel_perfect_checkbox
#img2img_controlnet_ControlNet-1_controlnet_preprocessor_preview_checkbox
#img2img_controlnet_ControlNet-1_controlnet_preprocessor_dropdown
#img2img_controlnet_ControlNet-1_controlnet_model_dropdown
#img2img_controlnet_ControlNet-1_controlnet_control_weight_slider
#img2img_controlnet_ControlNet-1_controlnet_start_control_step_slider
#img2img_controlnet_ControlNet-1_controlnet_ending_control_step_slider
#img2img_controlnet_ControlNet-1_controlnet_control_mode_radio
#img2img_controlnet_ControlNet-1_controlnet_resize_mode_radio
#img2img_controlnet_ControlNet-1_controlnet_automatically_send_generated_images_checkbox

#img2img_controlnet_ControlNet-2_controlnet_enable_checkbox
#img2img_controlnet_ControlNet-2_controlnet_low_vram_checkbox
#img2img_controlnet_ControlNet-2_controlnet_pixel_perfect_checkbox
#img2img_controlnet_ControlNet-2_controlnet_preprocessor_preview_checkbox
#img2img_controlnet_ControlNet-2_controlnet_preprocessor_dropdown
#img2img_controlnet_ControlNet-2_controlnet_model_dropdown
#img2img_controlnet_ControlNet-2_controlnet_control_weight_slider
#img2img_controlnet_ControlNet-2_controlnet_start_control_step_slider
#img2img_controlnet_ControlNet-2_controlnet_ending_control_step_slider
#img2img_controlnet_ControlNet-2_controlnet_control_mode_radio
#img2img_controlnet_ControlNet-2_controlnet_resize_mode_radio
#img2img_controlnet_ControlNet-2_controlnet_automatically_send_generated_images_checkbox

# Tiled Diffusion (extension)
#MD-i2i-enabled
#MD-i2i-keep-input-size
#MD-i2i-method
#MD-i2i-control-tensor-cpu
#MD-i2i-latent-tile-width
#MD-i2i-latent-tile-height
#MD-i2i-latent-tile-overlap
#MD-i2i-latent-tile-batch-size
#MD-i2i-upscaler-index
#MD-i2i-upscaler-factor
# Tiled Diffusion - Noise Inversion
#MD-i2i-noise-inverse
#MD-i2i-noise-inverse-steps
#MD-i2i-noise-inverse-retouch
#MD-i2i-noise-inverse-renoise-strength
#MD-i2i-noise-inverse-renoise-kernel
# Tiled Diffusion - Region Prompt Control
#MD-i2i-enable-bbox-control
#MD-i2i-draw-background
#MD-i2i-cfg-name
# Tiled Diffusion - Region Prompt Control - Region 1
#MD-bbox-i2i-0-enable
#MD-i2i-0-blend-mode
#MD-i2i-0-feather
#MD-i2i-0-x
#MD-i2i-0-y
#MD-i2i-0-w
#MD-i2i-0-h
#MD-i2i-0-prompt
#MD-i2i-0-neg-prompt
#MD-i2i-0-seed
# Tiled Diffusion - Region Prompt Control - Region 2
#MD-bbox-i2i-1-enable
#MD-i2i-1-blend-mode
#MD-i2i-1-feather
#MD-i2i-1-x
#MD-i2i-1-y
#MD-i2i-1-w
#MD-i2i-1-h
#MD-i2i-1-prompt
#MD-i2i-1-neg-prompt
#MD-i2i-1-seed
# Tiled Diffusion - Region Prompt Control - Region 3
#MD-bbox-i2i-2-enable
#MD-i2i-2-blend-mode
#MD-i2i-2-feather
#MD-i2i-2-x
#MD-i2i-2-y
#MD-i2i-2-w
#MD-i2i-2-h
#MD-i2i-2-prompt
#MD-i2i-2-neg-prompt
#MD-i2i-2-seed
# Tiled Diffusion - Tiled VAE
#tiledvae-i2i-enable
#tiledvae-i2i-vae2gpu
#tiledvae-i2i-enc-size
#tiledvae-i2i-dec-size
#tiledvae-i2i-fastenc
#tiledvae-i2i-fastenc-colorfix
#tiledvae-i2i-fastdec

# StableSR (extension)
#SR Model does not have an ID as of June 1 2023
#StableSR-scale
#StableSR-color-fix
#StableSR-save-original
#StableSR-pure-noise

# ADetailer (extension)
#script_img2img_adetailer_ad_enable
# ADetailer - 1st tab
#script_img2img_adetailer_ad_model
#script_img2img_adetailer_ad_prompt
#script_img2img_adetailer_ad_negative_prompt
# ADetailer - 1st tab - Detection
#script_img2img_adetailer_ad_confidence
#script_img2img_adetailer_ad_mask_min_ratio
#script_img2img_adetailer_ad_mask_max_ratio
# ADetailer - 1st tab - Mask Preprocessing
#script_img2img_adetailer_ad_x_offset
#script_img2img_adetailer_ad_y_offset
#script_img2img_adetailer_ad_dilate_erode
#script_img2img_adetailer_ad_mask_merge_invert
# ADetailer - 1st tab - Inpainting
#script_img2img_adetailer_ad_mask_blur
#script_img2img_adetailer_ad_denoising_strength
#script_img2img_adetailer_ad_inpaint_full_res
#script_img2img_adetailer_ad_inpaint_full_res_padding
#script_img2img_adetailer_ad_use_inpaint_width_height
#script_img2img_adetailer_ad_inpaint_width
#script_img2img_adetailer_ad_inpaint_height
#script_img2img_adetailer_ad_use_steps
#script_img2img_adetailer_ad_steps
#script_img2img_adetailer_ad_use_cfg_scale
#script_img2img_adetailer_ad_cfg_scale
#script_img2img_adetailer_ad_restore_face
# ADetailer - 1st tab - ControlNet
#script_img2img_adetailer_ad_controlnet_model
#script_img2img_adetailer_ad_controlnet_weight
#script_img2img_adetailer_ad_controlnet_guidance_start
#script_img2img_adetailer_ad_controlnet_guidance_end
# ADetailer - 2nd tab
#script_img2img_adetailer_ad_model_2nd
#script_img2img_adetailer_ad_prompt_2nd
#script_img2img_adetailer_ad_negative_prompt_2nd
# ADetailer - 2nd tab - Detection
#script_img2img_adetailer_ad_confidence_2nd
#script_img2img_adetailer_ad_mask_min_ratio_2nd
#script_img2img_adetailer_ad_mask_max_ratio_2nd
# ADetailer - 2nd tab - Mask Preprocessing
#script_img2img_adetailer_ad_x_offset_2nd
#script_img2img_adetailer_ad_y_offset_2nd
#script_img2img_adetailer_ad_dilate_erode_2nd
#script_img2img_adetailer_ad_mask_merge_invert_2nd
# ADetailer - 2nd tab - Inpainting
#script_img2img_adetailer_ad_mask_blur_2nd
#script_img2img_adetailer_ad_denoising_strength_2nd
#script_img2img_adetailer_ad_inpaint_full_res_2nd
#script_img2img_adetailer_ad_inpaint_full_res_padding_2nd
#script_img2img_adetailer_ad_use_inpaint_width_height_2nd
#script_img2img_adetailer_ad_inpaint_width_2nd
#script_img2img_adetailer_ad_inpaint_height_2nd
#script_img2img_adetailer_ad_use_steps_2nd
#script_img2img_adetailer_ad_steps_2nd
#script_img2img_adetailer_ad_use_cfg_scale_2nd
#script_img2img_adetailer_ad_cfg_scale_2nd
#script_img2img_adetailer_ad_restore_face_2nd
# ADetailer - 2nd tab - ADetailer ControlNet
#script_img2img_adetailer_ad_controlnet_model_2nd
#script_img2img_adetailer_ad_controlnet_weight_2nd
#script_img2img_adetailer_ad_controlnet_guidance_start_2nd
#script_img2img_adetailer_ad_controlnet_guidance_end_2nd

# Ultimate SD Upscale
#ultimateupscale_target_size_type
#ultimateupscale_custom_width
#ultimateupscale_custom_height
#ultimateupscale_custom_scale
#ultimateupscale_upscaler_index
#ultimateupscale_redraw_mode
#ultimateupscale_tile_width
#ultimateupscale_tile_height
#ultimateupscale_mask_blur
#ultimateupscale_padding
#ultimateupscale_seams_fix_type
#ultimateupscale_seams_fix_denoise
#ultimateupscale_seams_fix_width
#ultimateupscale_seams_fix_mask_blur
#ultimateupscale_seams_fix_padding
#ultimateupscale_save_upscaled_image
#ultimateupscale_save_seams_fix_image
"""

        write_text_to_file(img2img_custom_tracked_components_ids, CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME)
        print(f"[Config Presets] img2img custom tracked components config file not found, created default config at {BASEDIR}/{CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME}")

    return img2img_custom_tracked_components_ids


def load_txt2img_config_file():
    try:
        with open(f"{BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}") as file:
            txt2img_config_presets = json.load(file)

    except FileNotFoundError:
        # txt2img config file not found
        # First time running the extension or it was deleted, so fill it with default values

        # Note: "txt2img_enable_hr" was changed to "txt2img_hr-checkbox" in A1111 1.6.0 (8/31/2023), but we keep it
        # as "txt2img_enable_hr" in the config file so that newer version of Config Presets will work with older
        # versions of A1111. This is handled at run time with synonyms.

        txt2img_config_presets = {
            "None": {},
            "SD 1.5 - 512x512": {
                "txt2img_width": 512,
                "txt2img_height": 512,
            },
            "SD 2.1 - 768x768": {
                "txt2img_width": 768,
                "txt2img_height": 768,
            },
            "SDXL --- 1024x1024": {
                "txt2img_width": 1024,
                "txt2img_height": 1024,
            },
            "SDXL --- 1024x1024 with Refiner": {
                "txt2img_width": 1024,
                "txt2img_height": 1024,
                "txt2img_enable-checkbox": True,
            },
            "Low quality ------ steps: 10, batch size: 8, DPM++ 2M Karras": {
                "txt2img_sampling": "DPM++ 2M Karras",
                "txt2img_steps": 10,
                #"txt2img_width": 512,
                #"txt2img_height": 512,
                "txt2img_enable_hr": False,
                "txt2img_batch_count": 1,
                "txt2img_batch_size": 8,
                #"txt2img_cfg_scale": 7,
            },
            "Medium quality - steps: 15, batch size: 4, DPM++ 2M Karras": {
                "txt2img_sampling": "DPM++ 2M Karras",
                "txt2img_steps": 15,
                #"txt2img_width": 512,
                #"txt2img_height": 512,
                "txt2img_enable_hr": False,
                "txt2img_batch_count": 1,
                "txt2img_batch_size": 4,
                #"txt2img_cfg_scale": 7,
            },
            "High quality ------ steps: 20, batch size: 4, DPM++ 2S a Karras": {
                "txt2img_sampling": "DPM++ 2S a Karras",
                "txt2img_steps": 20,
                #"txt2img_width": 512,
                #"txt2img_height": 512,
                "txt2img_enable_hr": False,
                "txt2img_batch_count": 1,
                "txt2img_batch_size": 4,
                #"txt2img_cfg_scale": 7,
            },
            "High res -------- steps: 30, DPM++ 2M Karras, [Hires fix - Upscale by: 2, Denoising: 0.4, Hires steps: 10]": {
                "txt2img_steps": 30,
                "txt2img_sampling": "DPM++ 2M Karras",
                #"txt2img_width": 512,
                #"txt2img_height": 512,
                "txt2img_enable_hr": True,
                "txt2img_hr_scale": 2,
                "txt2img_hires_steps": 10,
                "txt2img_denoising_strength": 0.4,
                #"txt2img_batch_count": 1,
                #"txt2img_batch_size": 1,
                #"txt2img_cfg_scale": 7,
            },
            "1080p ----------- 432x768 -> 1920x1080, steps: 20, DPM++ 2M Karras, [Hires fix - Upscale by: 2.5, Denoising: 0.4, Hires steps: 10]": {
                # 2x 960x536, 2.5x 768x432, 3x 640x360
                "txt2img_steps": 20,
                "txt2img_sampling": "DPM++ 2M Karras",
                "txt2img_width": 768,
                "txt2img_height": 432,
                "txt2img_enable_hr": True,
                "txt2img_hr_scale": 2.5,
                "txt2img_hires_steps": 10,
                "txt2img_denoising_strength": 0.4,
                #"txt2img_batch_count": 1,
                #"txt2img_batch_size": 1,
                #"txt2img_cfg_scale": 7,
            },
            "1440p ----------- 432x768 -> 2560x1440, steps: 25, DPM++ 2M Karras, [Hires fix - Upscale by: 3.3334, Denoising: 0.3, Hires steps: 10]": {
                # 2x 1024x720, 2.5x 1024x576, 3.3334x 768x432, 4x 640x360
                "txt2img_steps": 25,
                "txt2img_sampling": "DPM++ 2M Karras",
                "txt2img_width": 768,
                "txt2img_height": 432,
                "txt2img_enable_hr": True,
                "txt2img_hr_scale": 3.3334,
                "txt2img_hires_steps": 10,
                "txt2img_denoising_strength": 0.4,
                #"txt2img_batch_count": 1,
                #"txt2img_batch_size": 1,
                #"txt2img_cfg_scale": 7,
            },
            "4k ---------------- 432x768 -> 3840x2160, steps: 30, DPM++ 2M Karras, [Upscale by: 5, Denoising: 0.3, Hires steps: 15]": {
                # 2x 1420x1080, 2.5x 1536x864, 3x 1280x720, 5x 768x432, 6x 640x360
                "txt2img_steps": 30,
                "txt2img_sampling": "DPM++ 2M Karras",
                "txt2img_width": 768,
                "txt2img_height": 432,
                "txt2img_enable_hr": True,
                "txt2img_hr_scale": 5,
                "txt2img_hires_steps": 15,
                "txt2img_denoising_strength": 0.4,
                #"txt2img_batch_count": 1,
                #"txt2img_batch_size": 1,
                #"txt2img_cfg_scale": 7,
            },
        }

        write_json_to_file(txt2img_config_presets, CONFIG_TXT2IMG_FILE_NAME)
        print(f"[Config Presets] txt2img config file not found, created default config at {BASEDIR}/{CONFIG_TXT2IMG_FILE_NAME}")

    return txt2img_config_presets


def load_img2img_config_file():
    try:
        with open(f"{BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}") as file:
            img2img_config_presets = json.load(file)

    except FileNotFoundError:
        # img2img config file not found
        # First time running the extension or it was deleted, so fill it with default values
        img2img_config_presets = {
            "None": {},
            "Low denoising ------- denoising: 0.25, steps: 20, DPM++ 2M Karras": {
                "img2img_sampling": "DPM++ 2M Karras",
                "img2img_steps": 20,
                #"img2img_width": 512,
                #"img2img_height": 512,
                #"img2img_batch_count": 1,
                #"img2img_batch_size": 1,
                #"img2img_cfg_scale": 7,
                "img2img_denoising_strength": 0.25,
            },
            "Medium denoising -- denoising: 0.40, steps: 20, DPM++ 2M Karras": {
                "img2img_sampling": "DPM++ 2M Karras",
                "img2img_steps": 20,
                #"img2img_width": 512,
                #"img2img_height": 512,
                #"img2img_batch_count": 1,
                #"img2img_batch_size": 1,
                #"img2img_cfg_scale": 7,
                "img2img_denoising_strength": 0.40,
            },
            "High denoising ------- denoising: 0.75, steps: 30, DPM++ 2M Karras": {
                "img2img_sampling": "DPM++ 2M Karras",
                "img2img_steps": 30,
                #"img2img_width": 512,
                #"img2img_height": 512,
                #"img2img_batch_count": 1,
                #"img2img_batch_size": 1,
                #"img2img_cfg_scale": 7,
                "img2img_denoising_strength": 0.75,
            },
        }

        write_json_to_file(img2img_config_presets, CONFIG_IMG2IMG_FILE_NAME)
        print(f"[Config Presets] img2img config file not found, created default config at {BASEDIR}/{CONFIG_IMG2IMG_FILE_NAME}")

    return img2img_config_presets


# workaround function for not being able to select new dropdown values after new choices are added to the dropdown in Gradio v3.28.1 (Automatic1111 v1.1.0)
# it's possible they will fix this in Gradio v4
# see: https://github.com/Zyin055/Config-Presets/pull/41
#def get_config_preset_dropdown_choices(new_config_presets) -> list[str]:
def get_config_preset_dropdown_choices(new_config_presets: list[str]) -> list[str]:
    new_choices = []
    if len(new_config_presets) > 0:
        # if isinstance(new_config_presets, dict):
        #     new_choices.extend(new_config_presets.keys())
        # else: # List assumed.
        #     new_choices.extend(new_config_presets)
        new_choices.extend(new_config_presets)
    return new_choices


def dict_synonyms(d, lsyn):
    """Adds synonyms to keys in a given dictionary.
    
    lsyn = [(key1,key2..), (key3,key4..) ...]
    Key2 will receive the value of key1 if it exists and vice versa.
    If both key3 and key4 exist, then they'll keep their old values.
    If two keys have values and a third doesn't, then it will be assigned to one of the two randomly.
    One liner partly written by a chatbot.
    """
    d2 = {key: d[existing_key] # Get existing value.
          for syn in lsyn # Loop over synonyms.
          for key in syn # Loop over each key in the set.
          for existing_key in syn  # Find existing key to copy from.
          if existing_key in d and key not in d} # Only if the key doesn't exist already.
    d2.update(d) # Add back all existing keys.
    return d2


class Script(scripts.Script):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load custom tracked components
        txt2img_custom_tracked_components_ids = load_txt2img_custom_tracked_component_ids()
        img2img_custom_tracked_components_ids = load_img2img_custom_tracked_component_ids()


        # These are the settings from the UI that are saved for each preset
        self.txt2img_component_ids = [
            "txt2img_sampling",
            "txt2img_steps",
            "txt2img_width",
            "txt2img_height",
            "txt2img_batch_count",
            "txt2img_batch_size",
            "txt2img_restore_faces",
            "txt2img_enable_hr",        # removed in A1111 1.6.0
            "txt2img_hr-checkbox",      # added in A1111 1.6.0
            "txt2img_hr_scale",
            "txt2img_hr_upscaler",
            "txt2img_hires_steps",
            "txt2img_denoising_strength",
            "txt2img_cfg_scale",
            "txt2img_enable-checkbox",  # Refiner, added in A1111 1.6.0
            "txt2img_switch_at",        # Refiner switch at, added in A1111 1.6.0

            # IDs below are only in Vlad's SD.Next UI (they must also be added to self.txt2img_optional_ids):
            "txt2img_sampling_alt", # Equiv to txt2img_hr_upscaler
            "txt2img_steps_alt", # Equiv to txt2img_hires_steps
            "txt2img_show_batch",
            "txt2img_show_seed",
            "txt2img_show_advanced", 
            "txt2img_show_second_pass", # Replaces txt2img_enable_hr in Vlad's
        ]
        self.txt2img_component_ids += txt2img_custom_tracked_components_ids # add the custom tracked components

        self.img2img_component_ids = [
            "img2img_sampling",
            "img2img_steps",
            "img2img_width",
            "img2img_height",
            "img2img_batch_count",
            "img2img_batch_size",
            "img2img_cfg_scale",
            "img2img_denoising_strength",
            "img2img_restore_faces",
            "img2img_enable-checkbox",  # Refiner, added in A1111 1.6.0
            "img2img_switch_at",        # Refiner switch at, added in A1111 1.6.0

            # IDs below are only in Vlad's SD.Next UI (they must also be added to self.img2img_optional_ids):
            "img2img_show_seed",
            "img2img_show_resize",
            "img2img_show_batch",
            "img2img_show_denoise",
            "img2img_show_advanced",
        ]
        self.img2img_component_ids += img2img_custom_tracked_components_ids # add the custom tracked components

        # Optional IDs don't crash the extension if no associated component is found.
        # These could be legacy IDs from older versions of the Web UI/extensions, or IDs from another UI (Vlad's SD.Next).
        self.txt2img_optional_ids = [
            "txt2img_restore_faces",    # removed in A1111 1.6.0
            "txt2img_enable_hr",        # removed in A1111 1.6.0, and replaced in Vlad's SD.Next
            "txt2img_hr-checkbox",      # added in A1111 1.6.0
            "txt2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner accordion)
            "txt2img_switch_at",        # added in A1111 1.6.0 (Refiner Switch at)

            "txt2img_hires_steps",      # Replaced in Vlad's SD.Next

            # IDs below are only in Vlad's SD.Next UI:
            "txt2img_sampling_alt",
            "txt2img_steps_alt",
            "txt2img_show_batch",
            "txt2img_show_seed",
            "txt2img_show_advanced", 
            "txt2img_show_second_pass",

            # IDs below are only for extensions:
            "controlnet_control_mod_radio",
            "controlnet_control_mode_radio",
        ]
        self.img2img_optional_ids = [
            "img2img_restore_faces",    # removed in A1111 1.6.0
            "img2img_enable-checkbox",  # added in A1111 1.6.0 (Refiner accordion)
            "img2img_switch_at",        # added in A1111 1.6.0 (Refiner Switch at)

            # IDs below are only in Vlad's SD.Next UI:
            "img2img_show_seed",
            "img2img_show_resize",
            "img2img_show_batch",
            "img2img_show_denoise",
            "img2img_show_advanced",

            # IDs below are only for extensions:
            "controlnet_control_mod_radio",
            "controlnet_control_mode_radio",
        ]

        # Synonymous IDs are interchangeable at load time.
        self.synonym_ids = [
            ("txt2img_hires_steps", "txt2img_steps_alt"),                       # Vlad's SD.Next Hires fix steps
            ("txt2img_enable_hr", "txt2img_show_second_pass"),                  # Vlad's SD.Next Hires fix enable
            ("controlnet_control_mod_radio", "controlnet_control_mode_radio"),  # ControlNet component renamed on 5/26/2023 due to typo.
            ("txt2img_enable_hr", "txt2img_hr-checkbox"),                       # Automatic1111 1.6.0 changed ID for Hires fix checkbox
        ]
        
        # Mapping between component labels and the actual components in ui.py
        self.txt2img_component_map = {k: None for k in self.txt2img_component_ids}  # gets filled up in the after_component() method
        self.img2img_component_map = {k: None for k in self.img2img_component_ids}  # gets filled up in the after_component() method

        # Load txt2img and img2img config files
        self.txt2img_config_presets = load_txt2img_config_file()
        self.img2img_config_presets = load_img2img_config_file()



    def title(self):
        return "Config Presets"

    def show(self, is_img2img):
        return scripts.AlwaysVisible    # hide this script in the Scripts dropdown

    def after_component(self, component, **kwargs):
        # to generalize the code, detect if we are in txt2img tab or img2img tab, and then use the corresponding self variables
        # so we can use the same code for both tabs
        component_map = None
        component_ids = None
        config_file_name = None
        custom_tracked_components_config_file_name = None
        optional_ids = None
        synonym_ids = self.synonym_ids
        if self.is_txt2img:
            component_map = self.txt2img_component_map
            component_ids = self.txt2img_component_ids
            config_file_name = CONFIG_TXT2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_TXT2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            optional_ids = self.txt2img_optional_ids
        else:
            component_map = self.img2img_component_map
            component_ids = self.img2img_component_ids
            config_file_name = CONFIG_IMG2IMG_FILE_NAME
            custom_tracked_components_config_file_name = CONFIG_IMG2IMG_CUSTOM_TRACKED_COMPONENTS_FILE_NAME
            optional_ids = self.img2img_optional_ids

        #if component.label in self.component_map:
        if component.elem_id in component_map:
            component_map[component.elem_id] = component
            #print(f"[Config-Presets][DEBUG]: found component: {component.elem_id} {component}")

        #if component.elem_id == "script_list": #bottom of the script dropdown
        #if component.elem_id == "txt2img_style2_index": #doesn't work, need to be added after all the components we edit are loaded
        #if component.elem_id == "open_folder": #bottom of the image gallery
        #if component.elem_id == "txt2img_results" or component.elem_id == "img2img_results": #bottom of the image gallery, doesn't work
        #if component.elem_id == "txt2img_gallery_container" or component.elem_id == "img2img_gallery_container": #bottom of the image gallery, doesn't work
        if component.elem_id == "txt2img_generation_info_button" or component.elem_id == "img2img_generation_info_button": #very bottom of the txt2img/img2img image gallery

            #print("Creating dropdown values...")
            #print("key/value pairs in component_map:")

            # before we create the dropdown, we need to check if each component was found successfully to prevent errors from bricking the Web UI
            component_map = {k:v for k,v in component_map.items() if v is not None or k not in optional_ids}    # Cleanse missing optional components with optional_ids
            component_ids = [k for k in component_ids if k in component_map]

            # protect against None type components to prevent bricking the UI
            # this check needs to happen after optional_ids are accounted for
            for component_name, component in component_map.items():
                if component is None:
                    log_error(f"The {'txt2img' if self.is_txt2img else 'img2img'} component '{component_name}' could not be processed. This may be because you are running an outdated version of the Config-Presets extension, you included a component ID in the custom tracked components config file that does not exist, it no longer exists (if you updated an extension or Automatic1111), or is an invalid component (if this is the case, you need to manually edit the config file at {BASEDIR}\\{custom_tracked_components_config_file_name} or just delete it so it resets to defaults). This extension will not work until this issue is resolved.")
                    return

            # Mark components with type "index" to be transformed
            index_type_components = []
            for component in component_map.values():
                #print(component)
                if getattr(component, "type", "No type attr") == "index":
                    # print(component.elem_id)
                    index_type_components.append(component.elem_id)

            preset_values = []
            config_presets: dict[str, any] = None
            if self.is_txt2img:
                config_presets = self.txt2img_config_presets
            else:
                config_presets = self.img2img_config_presets

            preset_values: list[str] = list(config_presets.keys())
            # for dropdownValue in config_presets:
            #     preset_values.append(dropdownValue)
            #     #print(f"Config Presets: added \"{dropdownValue}\"")

            fields_checkboxgroup = gr.CheckboxGroup(choices=component_ids,
                                                    value=component_ids,    #check all checkboxes by default
                                                    label="Fields to save",
                                                    show_label=True,
                                                    interactive=True,
                                                    elem_id="script_config_preset_fields_to_save",
                                                    ).unrender() #we need to define this early on so that it can be used as an input for another function

            with gr.Column(min_width=600, elem_id="config_preset_wrapper_txt2img" if self.is_txt2img else "config_preset_wrapper_img2img"):  # pushes our stuff onto a new row at 1080p screen resolution
                with gr.Row():
                    with gr.Column(scale=8, min_width=100) as dropdown_column:


                        def config_preset_dropdown_change(dropdown_value, *components_value):
                            config_preset = config_presets[dropdown_value]
                            config_preset = dict_synonyms(config_preset, synonym_ids) # Add synonyms
                            print(f"[Config-Presets] Changed to: {dropdown_value}")

                            # update component values with user preset
                            current_components = dict(zip(component_map.keys(), components_value))
                            #print("Components before:", current_components)
                            current_components.update(config_preset)

                            # transform necessary components from index to value
                            for component_name, component_value in current_components.items():
                                #print(component_name, component_value)
                                if component_name in index_type_components and type(component_value) == int:
                                        current_components[component_name] = component_map[component_name].choices[component_value]

                                        # A1111 1.6.0 changed radio buttons values into tuples.
                                        # For example, for the "img2img_mask_mode" component it changed from:
                                        #   ['Inpaint masked', 'Inpaint not masked']
                                        #   to
                                        #   [('Inpaint masked', 'Inpaint masked'), ('Inpaint not masked', 'Inpaint not masked')]
                                        # Using a type == tuple check here will ensure compatibility with the older versions.
                                        if type(current_components[component_name]) == tuple:
                                            current_components[component_name] = current_components[component_name][0]

                            #print("Components after :", current_components)
                            
                            return list(current_components.values())

                        config_preset_dropdown = gr.Dropdown(
                            label="Config Presets",
                            #choices=preset_values,
                            choices=get_config_preset_dropdown_choices(preset_values),
                            elem_id="config_preset_txt2img_dropdown" if self.is_txt2img else "config_preset_img2img_dropdown",
                        )

                        #self.txt2img_config_preset_dropdown = config_preset_dropdown

                        try:
                            components = list(component_map.values())
                            config_preset_dropdown.change(
                                fn=config_preset_dropdown_change,
                                show_progress=False,
                                inputs=[config_preset_dropdown, *components],
                                outputs=components
                                )
                        except AttributeError:
                            print(traceback.format_exc())   # prints the exception stacktrace
                            log_critical_error("The Config-Presets extension encountered a fatal error. A component required by this extension no longer exists in the Web UI. This is most likely due to the A1111 Web UI being updated. Try updating the Config-Presets extension. If that doesn't work, please post a bug report at https://github.com/Zyin055/Config-Presets/issues and delete your extensions/Config-Presets folder until an update is published.")

                        # No longer needed after the bump to Gradio 3.23
                        # config_preset_dropdown.change(
                        #     fn=None,
                        #     inputs=[],
                        #     outputs=[],
                        #     _js="function() { config_preset_dropdown_change() }",   # JS is used to update the Hires fix row to show/hide it
                        # )
                    with gr.Column(scale=8, min_width=100, visible=False) as collapsable_column:
                        with gr.Row():
                            with gr.Column(scale=1, min_width=10):

                                def delete_selected_preset(config_preset_name):
                                    if config_preset_name in config_presets.keys():
                                        del config_presets[config_preset_name]
                                        print(f'[Config-Presets] deleted: "{config_preset_name}"')

                                        write_json_to_file(config_presets, config_file_name)

                                        preset_keys = list(config_presets.keys())
                                        return gr.Dropdown.update(value=preset_keys[len(preset_keys)-1],
                                                                  #choices=preset_values,
                                                                  choices=get_config_preset_dropdown_choices(preset_keys),
                                                                  )
                                    return gr.Dropdown.update() # do nothing if no value is selected

                                trash_button = gr.Button(
                                    value="\U0001f5d1\ufe0f", #🗑
                                    elem_id="script_config_preset_trash_button",
                                )
                                trash_button.click(
                                    fn=delete_selected_preset,
                                    inputs=[config_preset_dropdown],
                                    outputs=[config_preset_dropdown],
                                )

                            with gr.Column(scale=2, min_width=190):
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
                                    value="📂 Open config file...",
                                    elem_id="script_config_preset_open_config_file_button",
                                )
                                open_config_file_button.click(
                                    fn=lambda: open_file(f"{BASEDIR}/{config_file_name}"),
                                    inputs=[],
                                    outputs=[],
                                )

                            with gr.Column(scale=2, min_width=50):
                                cancel_button = gr.Button(
                                    value="Cancel",
                                    elem_id="script_config_preset_cancel_save_button",
                                )

                    with gr.Column(scale=1, min_width=120, visible=True) as add_remove_button_column:
                        add_remove_button = gr.Button(
                            value="Add/Remove...",
                            elem_id="script_config_preset_add_button",
                        )

                with gr.Row() as collapsable_row:
                    collapsable_row.visible = False
                    with gr.Column():
                        with gr.Row():
                            with gr.Column(scale=10, min_width=100):
                                save_textbox = gr.Textbox(
                                    label="New preset name",
                                    placeholder="Ex: Low quality",
                                    # value="My Preset",
                                    max_lines=1,
                                    elem_id="script_config_preset_save_textbox",
                                )
                            with gr.Column(scale=2, min_width=200):
                                save_button = gr.Button(
                                    # value="Create",
                                    value="💾 Save",
                                    variant="primary",
                                    elem_id="script_config_preset_save_button",
                                )

                                save_button.click(
                                    fn=save_config(config_presets, component_map, config_file_name),
                                    inputs=list(
                                        [save_textbox] + [fields_checkboxgroup] + [component_map[comp_name] for comp_name in
                                                                                   component_ids if
                                                                                   component_map[comp_name] is not None]),
                                    outputs=[config_preset_dropdown, save_textbox],
                                )

                                def add_remove_button_click(save_textbox_text: str, config_preset_dropdown_value: str):
                                    if save_textbox_text == "" or save_textbox_text is None:
                                        if config_preset_dropdown_value != "" and config_preset_dropdown_value is not None:
                                            # save textbox is empty, and we have a dropdown value selected
                                            # auto-populate the save textbox so it's easier to overwrite existing config preset
                                            return gr.Textbox.update(value=config_preset_dropdown_value)
                                    return gr.Textbox.update()


                                def expand_edit_ui():
                                    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)

                                def collapse_edit_ui():
                                    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

                                add_remove_button.click(
                                    fn=add_remove_button_click,
                                    inputs=[save_textbox, config_preset_dropdown],
                                    outputs=[save_textbox],
                                )
                                add_remove_button.click(
                                    fn=expand_edit_ui,
                                    inputs=[],
                                    outputs=[collapsable_column, collapsable_row, add_remove_button_column],
                                )

                                cancel_button.click(
                                    fn=collapse_edit_ui,
                                    inputs=[],
                                    outputs=[collapsable_column, collapsable_row, add_remove_button_column],
                                )

                        with gr.Row():
                            fields_checkboxgroup.render()

                        with gr.Row():
                            with gr.Column(scale=1):
                                open_custom_tracked_components_config_file_button = gr.Button(
                                    value="📂 Add custom fields...",
                                    elem_id="script_config_preset_open_custom_tracked_components_config",
                                )
                                open_custom_tracked_components_config_file_button.click(
                                    fn=lambda: open_file(f"{BASEDIR}/{custom_tracked_components_config_file_name}"),
                                    inputs=[],
                                    outputs=[],
                                )
                            with gr.Column(scale=2):
                                pass


    def ui(self, is_img2img):
        pass

    def run(self, p, *args):
        pass


# Save the current values on the UI to a new entry in the config file
def save_config(config_presets, component_map, config_file_name):
    #print("save_config()")
    # closure keeps path in memory, it's a hack to get around how click or change expects values to be formatted
    def func(new_setting_name, fields_to_save_list, *new_setting):
        #print(f"save_config() func() new_setting_name={new_setting_name} *new_setting={new_setting}")
        #print(f"config_presets()={config_presets}")
        #print(f"component_map()={component_map}")
        #print(f"config_file_name()={config_file_name}")

        if new_setting_name == "":
            return gr.Dropdown.update(), "" # do nothing if no label entered in textbox

        new_setting_map = {}    # dict[str, Any]    {"txt2img_steps": 10, ...}

        #print(f"component_map={component_map}")
        #print(f"new_setting={new_setting}")

        for i, component_id in enumerate(component_map.keys()):

            if component_id not in fields_to_save_list:
                #print(f"[Config-Presets] New preset '{new_setting_name}' will not include {component_id}")
                continue

            if component_map[component_id] is not None:
                new_value = new_setting[i]  # this gives the index when the component is a dropdown

                if component_id == "txt2img_sampling" or component_id == "img2img_sampling" or component_id == "hr_sampler":
                    new_setting_map[component_id] = modules.sd_samplers.samplers_map[new_value.lower()]
                else:
                    new_setting_map[component_id] = new_value

                #print(f"Saving '{component_id}' as: {new_setting_map[component_id]} ({new_value})")

        #print(f"new_setting_map = {new_setting_map}")

        config_presets.update({new_setting_name: new_setting_map})
        write_json_to_file(config_presets, config_file_name)

        # print(f"self.txt2img_config_preset_dropdown.choices before =\n{self.txt2img_config_preset_dropdown.choices}")
        # self.txt2img_config_preset_dropdown.choices = list(config_presets.keys())
        # print(f"self.txt2img_config_preset_dropdown.choices after =\n{self.txt2img_config_preset_dropdown.choices}")

        print(f"[Config-Presets] Added new preset: {new_setting_name}")
        #print(f"[Config-Presets] Restarting UI...") # done in _js
        return gr.Dropdown.update(value=new_setting_name,   # update the dropdown with the new config preset
                                  #choices=list(config_presets.keys()),
                                  choices=get_config_preset_dropdown_choices(config_presets.keys()),
                                  ), "" # clear the 'New preset name' textbox

    return func


def write_json_to_file(json_data, file_name: str):
    with open(f"{BASEDIR}/{file_name}", "w") as file:
        file.write(json.dumps(json_data, indent=4))


def write_text_to_file(text, file_name: str):
    with open(f"{BASEDIR}/{file_name}", "w") as file:
        file.write(text)


def replace_text_in_file(old: str, new: str, file_name: str):
    with open(f"{BASEDIR}/{file_name}", "r") as file:
        content = file.read()

    with open(f"{BASEDIR}/{file_name}", "w") as file:
        file.write(content.replace(old, new))


def log(text: str):
    print(f"[Config Presets] {text}")


def log_error(text: str):
    print(f"[ERROR][Config Presets] {text}")


def log_critical_error(text: str):
    print(f"[ERROR][CRITICAL][Config Presets] {text}")
