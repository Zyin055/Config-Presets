//add tooltip by piggybacking off of javascript/hints.js
//titles["Edit..."] = "[Config Presets] open config.json"

//or do it our more precise way
onUiUpdate(function() {
	//set tooltips
	gradioApp().querySelectorAll("#config_presets_open_config_file_button").forEach(el => el.setAttribute("title", "[Config Presets] open config.json, requires Gradio restart after editing"))
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