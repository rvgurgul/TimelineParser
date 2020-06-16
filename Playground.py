from EventGroups import search_events
from ParallelParser import debug
from Classes.TimeRange import TimeRange

search_events("brief")

# toby ignore purloin crash
# debug("0mo3ecbwRHezaEft5e_5jA")



# debug("0A3GmdjWQtKmLUtiZAj7oQ")
debug("4TexJlU8TuOpiGadyMgTAQ")


# 0xetXvqoQRuar06rWGH_1Q
# 17ezXaIVQcCtk23yKQGMww
# 1sVjwTcdTHm2csf4h5EJEA
# 27_3emywRVWXeYGoMUWwNw
# 2hho-RzLQ3SZLE8JhapMEw
# 2rTN3mURShOe4c0HM0nQow
# 2UPMuC1TQEG-bqKSVgLyrw
# 2V12nwXoSN6e5R10321ldw
# 32Ov5HYPReCTYobwGEpetQ
# 3h4v3iX_SXK-4OC4eI5F5A
# 3zktEukfT0eErRRAccrAfA
# 47Ii6TnbQ_KjQv0Wd-WCSA
# 4j7Wmb1gSx6bak7mtAVwmg
# 4RykVUv5SROhbxRG2DM1nA



ran = TimeRange(-50, 75)
print(ran)
print(-100 in ran)
print(0 in ran)
print(100 in ran)
print(ran.is_inverted())
print(ran.to_list())
print(ran.to_list(5))
print(ran.to_list(50))
print(ran.to_list(67))

ranii = TimeRange(60, -25)
print(ranii)
print(-100 in ranii)
print(0 in ranii)
print(100 in ranii)
print(ranii.is_inverted())
print(ranii.to_list())
print(ranii.to_list(5))
print(ranii.to_list(50))
print(ranii.to_list(67))

