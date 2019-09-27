function l_sleep(n)
   os.execute("sleep " .. n)
end

i = 0

while i < 10 do
	::redo::
	i = i + 1
	if i % 2 == 1 then
		goto continue -- 条件不满足,下一个 continue
	else
		print(i)
		goto redo -- 条件满足,再来一次 redo
	end
	::continue::
end


goto room1

::room1:: do
	print("in room 1")
	local move = io.read()
	if move == "south" then goto room3
	elseif move == "east" then goto room2
	else
		print("invalid move")
		goto room1 -- stay in the same room
		sleep(1)
	end
end

::room2:: do
	print("in room 2")
	local move = io.read()
	if move == "south" then goto room4
	elseif move == "west" then goto room1
	else
		print("invalid move")
		goto room2
		sleep(1)
	end
end

::room3:: do
	print("in room 3")
	local move = io.read()
	if move == "north" then goto room1
	elseif move == "east" then goto room4
	else
		print("invalid move")
		goto room3
		sleep(1)
	end
end

::room4:: do
	print("in room 4")
	print("Congratulations, you won!")
end
