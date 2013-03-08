class BusRoute:
	"""Bus Route"""
	def __init__(self, name, initial_time, end_time, cycle_period = 60):
		self.stops = set()
		self.initial_time = initial_time
		self.end_time = end_time
		self.cycle_period = cycle_period
		self.name = name
	def addStop(self, stop):
		self.stops.add(stop)

class BusStop:
	"""Bus Stop"""
	def __init__(self, name, number):
		self.name = name
		self.number = number
		self.routes = dict()
	def addRoute(self, route, cycle_offset):
		self.routes[route.name] = tuple(route,cycle_offset)

bus_stops = dict()
bus_routes = dict()

# Loops through all interchange stops using the two routes
# between the two stops and returns the fastest path.
# @param time_init int 		:: current time in minutes
# @param first BusStop 		:: starting bus stop
# @param route_1 BusRoute 	:: initial bus route
# @param last BusStop 		:: ending bus stop
# @param route_2 BusRoute 	:: last bus route
# returns object OR None	:: information regarding the optimal path
def optimal_travel_time(time_init, first, route_1, last, route_2):
	best_route = None
	best_time = None
	for interchange in route_1.stops ^ route_2.stops:
		# time before the first bus
		wait_time_1 = route_1.cycle_period - ((time_init - route_1.initial_time) % route_1.cycle_period)
		if (wait_time_1 + time_init > route_1.end_time):
			continue
		# time to travel to the interchange
		travel_time_1 = interchange[route_1.name][1] - first[route_1.name][1] 
		# time to wait for the second bus
		wait_time_2 = route_2.cycle_period - ((time_init + time) - route_2.initial_time) % route_2.cycle_period)
		if (wait_time_2 + travel_time_2 + wait_time_1 + time_init > route_2.end_time):
			continue
		# time to travl to the last stop
		travel_time_2 = interchange[route_2.name][1] - last[route_2.name][1]

		if (not best_time or wait_time_1 + travel_time_1 + wait_time_2 + travel_time_2 < best_time):
			best_time = wait_time_1 + travel_time_1 + wait_time_2 + travel_time_2
			best_route = {	'first_route':route_1, 
							'last_route':route_2, 
							'first_wait':wait_time_1, 
							'first_travel':travel_time_1, 
							'last_wait':wait_time_2, 
							'last_travel':travel_time_2,
							'total_time': best_time }
	return best_route

# Loops through all combinations of travel routes between the two stops
# and returns the fastest one.
# @param time_init int 		:: current time in minutes
# @param first BusStop 		:: starting bus stop
# @param last BusStop 		:: ending bus stop
# returns list 				:: list of top ten optimal route objects
def optimal_route(first,last,time_init):
	best_route = []
	for route in first.routes:
		if (last in route.stops):
			wait_time = route.cycle_period - ((time_init - route.initial_time) % route.cycle_period)
			if (wait_time_1 + time_init > route.end_time):
				continue
			travel_time = last[route.name][1] - first[route.name][1] 
			best_route.append( {'first_route':route,
								'first_wait':wait_time,
								'first_travel':travel_time,
								'total_time':wait_time+travel_time} )
	if (not best_route):
		for route_1 in first.routes:
			for route_2 in last.routes:
				if route_1.stops ^ route_2.stops:
					best_route.append(optimal_travel_time(time_init,first,route_1,last,route_2))
	best_route.sort(key=lambda x: x['total_time'])
	return best_route[:10]