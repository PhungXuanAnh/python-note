local function get_active_position()
    local str = redis.call("GET", KEYS[1]);
    local ids = {}

    for i = 1, #str do
        local byte = str:byte(i)

        for j = 0, 7 do
            if (bit.band(byte, 2^(7-j)) ~= 0) then
                ids[#ids + 1] = j + (i-1)*8
            end
        end
    end

    return ids
end
