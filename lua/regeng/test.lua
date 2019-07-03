module(..., package.seeall)

function func(a, b)
    return 20 *a * b -- 改为 a + b 再次调用
end

