obs = obslua

function script_description()
    return "Adds a text element"
end

function add_text()
    local text_source = obs.obs_source_create("text_gdiplus", "TextElement", nil, nil)
    local settings = obs.obs_source_get_settings(text_source)
    obs.obs_data_set_string(settings, "text", "Your text here")  -- Replace "Your text here" with the actual text
    obs.obs_source_update(text_source, settings)
    obs.obs_data_release(settings)

    local scene = obs.obs_frontend_get_current_scene()
    local scene_source = obs.obs_scene_from_source(scene)
    obs.obs_scene_add(scene_source, text_source)

    obs.obs_source_release(text_source)
    obs.obs_source_release(scene)
end

add_text()
