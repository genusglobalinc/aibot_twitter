obs = obslua

function script_description()
    return "Centers a scene element"
end

function center_element()
    local source = obs.obs_get_source_by_name("ElementName")  -- Replace "ElementName" with the actual name of your element
    if source then
        local settings = obs.obs_source_get_settings(source)
        obs.obs_data_set_int(settings, "alignment", 5)  -- Center alignment
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
    end
end

center_element()
