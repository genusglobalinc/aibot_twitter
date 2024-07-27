obs = obslua

function script_description()
    return "Starts recording"
end

function start_recording()
    obs.obs_frontend_recording_start()
end

start_recording()
