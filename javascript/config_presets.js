//add tooltip by piggybacking off of javascript/hints.js ...
//titles["Add/Remove..."] = "[Config Presets] Add or remove a preset"
//...or do it our more precise way:
onUiUpdate(function() {
	//set tooltips
	gradioApp().querySelectorAll("#script_config_preset_open_config_file_button").forEach(el => el.setAttribute("title", "Open the config .json file for manual editing if you want to make changes that way, requires Gradio restart after editing. The txt2img and img2img tabs have separate config files."))
	gradioApp().querySelectorAll("#script_config_preset_save_textbox").forEach(el => el.setAttribute("title", "The name of a new Config Preset that will be added to the dropdown above"))
	gradioApp().querySelectorAll("#script_config_preset_save_button").forEach(el => el.setAttribute("title", "Save selected fields with the new preset name. It will overwrite an existing preset with the same name."))
	gradioApp().querySelectorAll("#script_config_preset_add_button").forEach(el => el.setAttribute("title", "[Config Presets] Create or delete a preset"))
	gradioApp().querySelectorAll("#script_config_preset_cancel_save_button").forEach(el => el.setAttribute("title", "Go back"))
	gradioApp().querySelectorAll("#script_config_preset_trash_button").forEach(el => el.setAttribute("title", "Permanently delete selected preset"))
	gradioApp().querySelectorAll("#script_config_preset_fields_to_save > span").forEach(el => el.setAttribute("title", "Only selected field values will be saved with the preset. Unselected fields will be ignored."))
	gradioApp().querySelectorAll("#script_config_preset_open_custom_tracked_components_config").forEach(el => el.setAttribute("title", "Open the config file to add new fields to the above list."))
	gradioApp().querySelectorAll("#script_config_preset_reapply_button").forEach(el => el.setAttribute("title", "Reapply the selected preset"))
})
/* No longer needed after the bump to Gradio 3.23
//this function called by config_preset_dropdown in config_presets.py
function config_preset_dropdown_change() {
	//when Python changes the enable_hr checkbox in config_preset_dropdown_change() it doesn't fire off the change() JS event, so do this manually
	
	//there is a race condition between the checkbox being checked in Python, and us firing its change event in JavaScript, so wait a bit before firing the event
	setTimeout(function() { 
		let hiresFixCheckbox = gradioApp().querySelector("#txt2img_enable_hr > label").firstChild //gets the <input> element next to the "Hires. fix" <span>
		
		let e = document.createEvent("HTMLEvents")
		e.initEvent("change", true, false)
		hiresFixCheckbox.dispatchEvent(e)
		
		//console.log("hiresFixCheckbox="+hiresFixCheckbox)
		//console.log("e="+e)
	}, 200) //50ms is too fast
}
*/

function config_preset_settings_restart_gradio() {
	console.log('[Config-Presets] Restarting to apply new config preset...')
	setTimeout(function() {
		gradioApp().getElementById("settings_restart_gradio").click()
	}, 1000)
}