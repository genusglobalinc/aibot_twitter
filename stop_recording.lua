obs = obslua

function script_description()
    return "Stops recording"
end

function stop_recording()
    obs.obs_frontend_recording_stop()
end

stop_recording()
