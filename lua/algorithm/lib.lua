local splitTable = function(p,s) -- 分隔函数
	local rt= {}
	string.gsub(s, '[^'..p..']+', function(w) table.insert(rt, w) end )
	return rt
end  

function print_r ( t ) --打印表 
	local print_r_cache={}
	local function sub_print_r(t,indent)
		if (print_r_cache[tostring(t)]) then
			print(indent.."*"..tostring(t))
		else
			print_r_cache[tostring(t)]=true
			if (type(t)=="table") then
				for pos,val in pairs(t) do
					if (type(val)=="table") then
						print(indent.."["..pos.."] => "..tostring(t).." {")
						sub_print_r(val,indent..string.rep(" ",string.len(pos)+8))
						print(indent..string.rep(" ",string.len(pos)+6).."}")
					elseif (type(val)=="string") then
						print(indent.."["..pos..'] => "'..val..'"')
					else
						print(indent.."["..pos.."] => "..tostring(val))
					end
				end
			else
				print(indent..tostring(t))
			end
		end
	end
	if (type(t)=="table") then
		print(tostring(t).." {")
		sub_print_r(t,"  ")
		print("}")
	else
		sub_print_r(t,"  ")
	end
	print()
end

function SpecifyProbability(RandomTable, ProbabilityTable)--比例筛选
	if RandomTable == nil or ProbabilityTable == nil then
		return
	end
	local price = 0
	local pricetable ={}
	for _,v in ipairs(ProbabilityTable) do
		price = v + price
		table.insert(pricetable,price)
	end
	local m_random = math.random(1,price)
	for i,v in ipairs(pricetable) do
		if m_random <= v then
			return RandomTable[i]
		end
	end
end    

local TimerTable = {}
function fsm_timeout(Name,Timeout_sec)
	if Name == nil then 
		return false 
	end        

	if Timeout_sec == nil then
		Timeout_sec = 0
	end        

	local now_time = API_GetTimeMS()
	local end_time = TimerTable[Name]
	if end_time == nil then
		TimerTable[Name] = now_time + Timeout_sec*1000
		return false 
	end        

	if now_time < end_time then
		return false
	else       
		TimerTable[Name] = nil
		return true
	end       
end 

local loo = splitTable(",","1,2,3,4,5,6,7,8")

print_r(loo)
