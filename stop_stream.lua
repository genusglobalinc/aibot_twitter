obs = obslua

function script_description()
    return "Stops the stream"
end

function stop_stream()
    obs.obs_frontend_streaming_stop()
end

stop_stream()
