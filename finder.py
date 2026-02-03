from utils.trainlogger.map.mapimage import CoordinateFinder
# from utils.trainlogger.map.station_coordinates_log_train_map_pre_munnel import x_offset, y_offset, station_coordinates
# from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import line_coordinates
from utils.trainlogger.map.station_coordinates_log_train_map_post_munnel import x_offset, y_offset, station_coordinates
from utils.trainlogger.map.line_coordinates_log_train_map_post_munnel import line_coordinates
# from utils.trainlogger.map.station_coordinates_log_sydney_tram_map import x_offset, y_offset, station_coordinates
# from utils.trainlogger.map.line_coordinates_log_sydney_tram_map import line_coordinates

# finder = CoordinateFinder("utils/trainlogger/map/time_based_variants/log_train_map_pre_munnel.png", x_offset, y_offset, station_coordinates, line_coordinates)
finder = CoordinateFinder("utils/trainlogger/map/time_based_variants/log_train_map_post_munnel.png", x_offset, y_offset, station_coordinates, line_coordinates)
# finder = CoordinateFinder("utils/trainlogger/map/log_sydney-tram_map.png", x_offset, y_offset, station_coordinates, line_coordinates)
finder.run()