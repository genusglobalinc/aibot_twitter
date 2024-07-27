obs = obslua

function script_description()
    return "Starts the stream"
end

function start_stream()
    obs.obs_frontend_streaming_start()
end

start_stream()
