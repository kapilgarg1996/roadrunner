ROUTE_SEARCH_QUERY = """
    select Route.* from Route   
 inner join Stop on Route.SOURCE=Stop.ID and Stop.NAME = %s 
 inner join Stop Stop_Dest on  Route.DEST = Stop_Dest.ID and Stop_Dest.NAME = %s 
 inner join Bus on Route.BUS = Bus.ID
 where timediff(Route.START_TIME, %s)>='01:00:00' 
 and abs(timediff(%s, Route.START_TIME))<240000 
 order by abs(timediff(%s, Route.START_TIME)), Bus.AC, Bus.SEATER;
    """


ROUTE_DETAIL_QUERY = """
select Route.ID as id, Route.START_TIME as start_time, Route.JOURNEY_TIME as journey_time, Route.FAIR as fair, Route.SEATS_AVAIL as seats_avail, Route.SEATS_CONFIG as seats_config, 
 Bus.NUMBER as bus_number, Bus.IMAGE as image, 
 Stop.NAME as s_name, Stop.CITY as s_city, 
 Stop_dest.NAME as d_name, Stop_dest.CITY as d_city, 
 Employee.NAME as driver, DEmployee.NAME as conductor 
 from Route 
 inner join Bus on Route.BUS = Bus.ID 
 inner join Stop on Route.SOURCE = Stop.ID 
 inner join Stop Stop_dest on Route.DEST = Stop_dest.ID 
 inner join Employee on Route.DRIVER = Employee.ID 
 inner join Employee DEmployee on Route.CONDUCTOR = DEmployee.ID 
 where Route.ID = %s
 """

USER_DETAIL_QUERY = """
select User.ID as id, User.NAME as name, User.EMAIL as email, Ticket.ID as tid, Route.SOURCE as source, Route.DEST as destination from Ticket inner join User on Ticket.USER = User.ID and User.ID = %s inner join Route on Ticket.ROUTE = Route.ID ;
"""
