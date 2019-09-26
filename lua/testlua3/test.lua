function sleep(n)
   os.execute("sleep " .. n)
end

function Func ( i, f, str)
	print("func test")
	print(i)
	print(f)
	print(str)
	return 100
end

price, str = fff(6999, "nzhsoft")
print(price)
print(str)

avg,sum=FFF(1,2,3,4,5)
print("avg;",avg," sum:",sum)
