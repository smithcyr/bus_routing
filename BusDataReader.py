import urllib, re, sched
from datetime import datetime, timedelta

data = open("C:\\Users\\Cyrus\\Desktop\\BusData",'r').read()
busstops = open("C:\\Users\\Cyrus\\Desktop\\Bus_Stops.txt",'w')
busroutes = open("C:\\Users\\Cyrus\\Desktop\\Bus_Routes.txt",'w')
routes = ['rt_7thave', 'rt_brdwy', 'rt_brdwynw', 'rt_courthill', 'rt_crosspark', 'rt_eastex', 'rt_esla', 'rt_eslp', 'rt_eventshuttle', 'rt_shuttlen', 'rt_shuttles', 'rt_lakeside', 'rt_mall', 'rt_manville', 'rt_manvillenw', 'rt_melrose', 'rt_ndodge', 'rt_ndodgenw', 'rt_oakcrst', 'rt_oakcrstnw', 'rt_plaenview', 'rt_rochester', 'rt_towncrst', 'rt_towncrstnw', 'rt_westport', 'rt_westhosp', 'rt_westwinds', 'rt_westwindsnw']

stopRegEx = re.compile('lookup\( \'(\d+)\', \'(.*?)\' \)')
stops = set(stopRegEx.findall(data))
for stop in stops:
	busstops.write(stop[0] + "," + stop[1] + '\n')
routes = dict()

stopsandtimes = open("C:\\Users\\Cyrus\\Desktop\\Stop_Log.txt",'w')

timeRegex = re.compile('<li><span>(\d+).*?</span> (.*?)</li>')
s = sched.scheduler(time.time, time.sleep)
def query_bus_sched(sc):
	for stop in stops:
		stoptimes = timeRegex.findall(urllib.urlopen("http://www.icgov.org/apps/transitMap/AJAX.times.aspx?stopNo=" + stop[0]).read())
		for route in stoptimes:
			log_entry = (stop[1],(datetime.now()+timedelta(minutes=int(route[0]))).strftime('%a, %H:%M'))
			if (not route[1] in routes):
				routes[route[1]] = set()
			routes[route[1]].add(log_entry)
			stopsandtimes.write(log_entry[0]+","+route[1]+","+log_entry[1]+"\n")
			print stop[0]+",",
	sc.enter(5100, 1, query_bus_sched, (sc,))

s.enter(4000, 1, query_bus_sched, (s,))
s.run()