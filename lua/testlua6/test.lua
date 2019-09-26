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
	print("--test_Hello--")
	local str = printHello()
	print(str)
end

function test_foo()
	print("--test_foo--")
	local a = foo(10)
	print(a)
end

function test_add()
	print("--test_add--")
	local num = add(1,2,3,4,5)
	print(num)
end

test_printHello()
test_foo()
test_add()

