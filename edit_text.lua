obs = obslua

function script_description()
    return "Edits a text element"
end

function edit_text()
    local text_source = obs.obs_get_source_by_name("TextElement")  -- Replace "TextElement" with the actual name of your text element
    if text_source then
        local settings = obs.obs_source_get_settings(text_source)
        obs.obs_data_set_string(settings, "text", "New text here")  -- Replace "New text here" with the new text
        obs.obs_source_update(text_source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(text_source)
    end
end

edit_text()
