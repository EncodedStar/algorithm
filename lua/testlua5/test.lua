function sleep(n)
   os.execute("sleep " .. n)
end

function Func ( i, f, str)
	print("Func test")
	print(i)
	print(f)
	print(str)
	return i * f
end

function test_c_func2()
	price, str = c_func2(1024, "hxsoft")
	print(price)
	print(str)
end

function test_printHello()
	local str = printHello()
	print(str)
end

test_printHello()
