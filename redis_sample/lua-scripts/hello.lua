
-- sudo apt-get update
-- sudo apt-get install lua-bitop
local bit = require("bit")
local ids = {}
local str = 'aaaaaaaaaaaaaaaaaa'

for i = 1, #str do
    local byte = str:byte(i)
    
    for j = 0, 7 do
        print(bit.band(byte, 2^(7-j)))
        if (bit.band(byte, 2^(7-j)) ~= 0) then
            ids[#ids + 1] = j + (i-1)*8
        end
    end
    print('aaaaaaaaaaaaaa')
end
-- print('aaaaaaaaaaaa')
-- for k, v in pairs(ids ) do
--     -- print(k, v)
--     print(v)
-- end
print('len =',string.len(str))

array = {"Lua", "Tutorial"}
for i = 0, 2 do
   print(i, array[i])
end

array = {}

for i= -2, 2 do
   array[i] = i *2
end

for i = -2,2 do
   print(array[i])
end

