//add tooltip by piggybacking off of javascript/hints.js
//titles["Add/Remove..."] = "[Config Presets] Add or remove a preset"

//or do it our more precise way
onUiUpdate(function() {
	//set tooltips
	gradioApp().querySelectorAll("#config_presets_open_config_file_button").forEach(el => el.setAttribute("title", "Open the config.json file for manual editing if you want to make changes that way, requires Gradio restart after editing"))
	gradioApp().querySelectorAll("#config_preset_save_textbox").forEach(el => el.setAttribute("title", "The label that will be displayed in the dropdown to the left"))
	gradioApp().querySelectorAll("#config_preset_save_button").forEach(el => el.setAttribute("title", "Saves current settings with the new preset name. This will save: Steps, Sampler, Width/Height, Highres fix, Firstpass width/height, Denoising strength, Batch size, CFG Scale."))
	gradioApp().querySelectorAll("#config_preset_add_button").forEach(el => el.setAttribute("title", "[Config Presets] Add or remove a preset"))
	gradioApp().querySelectorAll("#config_preset_cancel_save_button").forEach(el => el.setAttribute("title", "Go back"))
	gradioApp().querySelectorAll("#config_preset_trash_button").forEach(el => el.setAttribute("title", "Permanently delete selected preset"))
})

//change() event called by config_preset_dropdown in config_presets.py
function config_preset_dropdown_change() {
	//when Python changes the enable_hr checkbox in config_preset_dropdown_change() it doesn't fire off the change() JS event, so do this manually
	
	//there is a race condition between the checkbox being checked in Python, and us firing its change event in JavaScript, so wait a bit before firing the event
	setTimeout(function() { 
		//the "Highres. fix" checkbox has no easy way to identify it, so use its tooltip attribute on the neighboring element
		let highresCheckbox = gradioApp().querySelector("label > span[title='Use a two step process to partially create an image at smaller resolution, upscale, and then improve details in it without changing composition'").parentElement.firstChild
		
		let e = document.createEvent("HTMLEvents")
		e.initEvent("change", true, false)
		highresCheckbox.dispatchEvent(e)
	}, 200) //50ms is too fast
}