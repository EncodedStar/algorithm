local func = require "func"

function SelectFunc(select)
	func.hello(select)
	if select == 1 then
		func.hello()
	else
		func.world()
	end
	return 1
end
