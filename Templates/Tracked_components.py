# Any line of text changed here will be added as a new line at the bottom of the user's *-custom-tracked-components.txt
# config file (this means we cannot change the informational header at the top).
# All entries here should be commented out with a # so that they are not enabled by default.
txt2img_template_tracked_components_ids = [
    '''# Put custom txt2img tracked component IDs here. This will allow those fields to be saved as a config preset.
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
script_txt2img_adetailer_ad_enable
# ADetailer - 1st tab
#script_txt2img_adetailer_ad_model
#script_txt2img_adetailer_ad_prompt
#script_txt2img_adetailer_ad_negative_prompt
# ADetailer - 1st tab - Detection
#script_txt2img_adetailer_ad_confidence
script_txt2img_adetailer_ad_mask_min_ratio
#script_txt2img_adetailer_ad_mask_max_ratio
# ADetailer - 1st tab - Mask Preprocessing
#script_txt2img_adetailer_ad_x_offset
#script_txt2img_adetailer_ad_y_offset
#script_txt2img_adetailer_ad_dilate_erode
#script_txt2img_adetailer_ad_mask_merge_invert
# ADetailer - 1st tab - Inpainting
#script_txt2img_adetailer_ad_mask_blur
script_txt2img_adetailer_ad_denoising_strength
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
script_txt2img_adetailer_ad_controlnet_model
script_txt2img_adetailer_ad_controlnet_weight
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

# Animated Diff (extension)
#txt2img-ad-motion-module
#txt2img-ad-enable
#txt2img-ad-video-length
#txt2img-ad-fps
#txt2img-ad-loop-number
#txt2img-ad-closed-loop
#txt2img-ad-batch-size
#txt2img-ad-stride
#txt2img-ad-overlap
#txt2img-ad-save-format
#txt2img-ad-reverse
#txt2img-ad-interp-choice
#txt2img-ad-interp-x
#txt2img-ad-video-path
#txt2img-ad-latent-power
#txt2img-ad-latent-scale
#txt2img-ad-latent-power-last
#txt2img-ad-latent-scale-last'''
]

img2img_template_tracked_components_ids = [
    '''# Put custom img2img tracked component IDs here. This will allow those fields to be saved as a config preset.
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
script_list

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
img2img_controlnet_ControlNet-0_controlnet_enable_checkbox
#img2img_controlnet_ControlNet-0_controlnet_low_vram_checkbox
img2img_controlnet_ControlNet-0_controlnet_pixel_perfect_checkbox
#img2img_controlnet_ControlNet-0_controlnet_preprocessor_preview_checkbox
img2img_controlnet_ControlNet-0_controlnet_preprocessor_dropdown
img2img_controlnet_ControlNet-0_controlnet_model_dropdown
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

# Ultimate SD Upscaler (extension)
#ultimateupscale_upscaler_index
#ultimateupscale_tile_width
#ultimateupscale_custom_scale
#ultimateupscale_seams_fix_type
#ultimateupscale_seams_fix_denoise
#ultimateupscale_target_size_type
#ultimateupscale_custom_width
#ultimateupscale_custom_height
#ultimateupscale_redraw_mode
#ultimateupscale_tile_height
#ultimateupscale_mask_blur
#ultimateupscale_padding
#ultimateupscale_seams_fix_width
#ultimateupscale_seams_fix_mask_blur
#ultimateupscale_seams_fix_padding
#ultimateupscale_save_upscaled_image
#ultimateupscale_save_seams_fix_image

# Animated Diff (extension)
#img2img-ad-motion-module
#img2img-ad-enable
#img2img-ad-video-length
#img2img-ad-fps
#img2img-ad-loop-number
#img2img-ad-closed-loop
#img2img-ad-batch-size
#img2img-ad-stride
#img2img-ad-overlap
#img2img-ad-save-format
#img2img-ad-reverse
#img2img-ad-interp-choice
#img2img-ad-interp-x
#img2img-ad-video-path
#img2img-ad-latent-power
#img2img-ad-latent-scale
#img2img-ad-latent-power-last
#img2img-ad-latent-scale-last'''
]
