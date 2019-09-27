local Array = require "array"

local a = Array.new(1000)
print("a 的类型:",a) --> userdata: 0x8064d48
print("a 的大小:",Array.size(a)) --> 1000
for i = 1, 100 do
	Array.set(a,i,i%2==0) --array.set(a, i,nil/false)
end
print(Array.get(a, 10))
print(Array.get(a, 11))

