obs = obslua

function script_description()
    return "Moves a scene element to the top right"
end

function move_element_top_right()
    local source = obs.obs_get_source_by_name("ElementName")  -- Replace "ElementName" with the actual name of your element
    if source then
        local settings = obs.obs_source_get_settings(source)
        obs.obs_data_set_int(settings, "alignment", 6)  -- Top right alignment
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    end
end

move_element_top_right()
