# coding: utf-8
import datetime
def month_gen(date=datetime.date.today(), count=6):
	month = []
	month.append(datetime.date(year=date.year, month=date.month, day=1))
	for i in range(1, count):
		temp = month[i-1] -datetime.timedelta(days=5)
		month.append(datetime.date(year=temp.year, month=temp.month, day=1))
	return month

if __name__ == '__main__':
	l=month_gen()
	print l

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip