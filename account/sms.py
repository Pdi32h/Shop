import ghasedakpack

sms = ghasedakpack.Ghasedak("8d2e3992e8d776fd625943f77a9946b682e9b148ee316bd87365caa2905232d3")
sms.verification({'receptor': '09185348720', 'type': '1', 'template': 'pdi', 'param1': '1234'})
