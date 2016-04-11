ROUTE_SEARCH_QUERY = """
    select bus_route.* from bus_route   
 inner join bus_stop on bus_route.source_id=bus_stop.id and bus_stop.name = %s 
 inner join bus_stop bus_stop_dest on  bus_route.dest_id = bus_stop_dest.id and bus_stop_dest.name = %s 
 inner join bus_bus on bus_route.bus_id = bus_bus.id
 where timediff(bus_route.start_time, %s)>='01:00:00' 
 and abs(timediff(%s, bus_route.start_time))<240000 
 order by abs(timediff(%s, bus_route.start_time)), bus_bus.ac, bus_bus.seater;
    """


ROUTE_DETAIL_QUERY = """
select bus_route.id as id, bus_route.start_time as start_time, bus_route.journey_time as journey_time, bus_route.fair as fair, bus_route.seats_avail as seats_avail, bus_route.seats_config as seats_config, 
 bus_bus.number as bus_number, bus_bus.image as image, bus_bus.ac as ac, bus_bus.seater as seater, 
 bus_stop.name as s_name, bus_stop.city as s_city, 
 bus_stop_dest.name as d_name, bus_stop_dest.city as d_city, 
 bus_employee.name , demployee.name
 from bus_route 
 inner join bus_bus on bus_route.bus_id = bus_bus.id 
 inner join bus_stop on bus_route.source_id = bus_stop.id 
 inner join bus_stop bus_stop_dest on bus_route.dest_id = bus_stop_dest.id 
 inner join bus_employee on bus_route.driver_id = bus_employee.id 
 inner join bus_employee demployee on bus_route.conductor_id = demployee.id 
 where bus_route.id = %s
 """

USER_DETAIL_QUERY = """
select User.id as id, User.name as name, User.email as email, bus_ticket.id as tid, bus_route.source as source, bus_route.dest as destination from bus_ticket.inner join User on bus_ticket.user = User.id and User.id = %s inner join bus_route on bus_ticket.route = bus_route.id ;
"""
