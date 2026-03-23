from PIL import Image, ImageDraw, ImageChops, ImageFont
import tkinter as tk
from PIL import ImageTk
from matplotlib.pylab import f
import math

dpi = 32/96
padding = 1.1
vertical_padding = 1.1
margin_watermark = (1 - (1 / vertical_padding)) / 2
text_ratio = 20

def compress(image: Image):
    print("Compressing Image")
    try:
        success = False
        while success == False:
            if image.size[0] > 10000 or image.size[1] > 10000:
                image = image.resize((round(image.size[0] / 2), round(image.size[1] / 2)))
            else:
                print("Image Compressed")
                success = True
                return image
    except Exception as e:
        print(e)

def legend(image: Image, legend_path):
    print('Adding Legend')
    try:
        legend = Image.open(legend_path)
        image_ratio = legend.size[0] / image.size[0]
        new_y = round(legend.size[1] + image.size[1] * image_ratio)
        new_size = [legend.size[0], new_y]
        final_image = Image.new(image.mode, new_size, image.getpixel((0,0)))
        new_image = image.resize((round(image.size[0] * image_ratio), round(image.size[1] * image_ratio)))
        final_image.paste(new_image)
        final_image.paste(legend, (0, new_image.size[1] + 1))
        print('Legend Added')
        return final_image
    except:
        print('Legend Failed')
        return image

class MapImageHandler:
    def __init__(self, map_image_path, station_order_dictionary, x_offset, y_offset, station_coordinates, line_coordinates):
        self.station_order = station_order_dictionary
        self.map_image = Image.open(map_image_path)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.station_coordinates = station_coordinates
        self.line_coordinates = line_coordinates
        self.path = map_image_path
        print('Initalised the map maker')
        
    def highlight_map(self, station_pairs, output_path, stations, no_compression):
        """
        Creates a white cover over the entire map except for holes where the stations and lines are
        
        Args:
            station_pairs (list): List of tuples containing station pairs and line name (station1, station2, line)
            output_path (str): Path where the modified image will be saved
        """
        # Create a copy of the original image
        modified_map = self.map_image.copy()
        
        # Create a white overlay
        overlay = Image.new('RGBA', modified_map.size, 'white')
        draw = ImageDraw.Draw(overlay)
        
        # Get unique stations from pairs
        affected_stations = set()
        for station1, station2, _ in station_pairs:
            affected_stations.add(station1)
            affected_stations.add(station2)
        
        # Create holes for stations
        for station in stations:
            if station in self.station_coordinates:
                coords = self.station_coordinates[station]
                if isinstance(coords, list):
                    for coord in coords:
                        coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coord2.append(coor)
                        coord = tuple(coord2)
                        draw.rectangle(coord, fill=(255, 255, 255, 0))
                else:
                    coord2 = []
                    for coor in coords:
                        coor = coor * dpi
                        coord2.append(coor)
                    coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
                print(f'Created hole for {station}')
            else:
                print(f'No coordinates for {station}')

        # for testing only, comment out when finished
        '''for station in self.station_coordinates:
            coords = self.station_coordinates[station]
            if isinstance(coords, list):
                for coord in coords:
                    coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coord2.append(coor)
                        coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
            else:
                coord2 = []
                for coor in coords:
                    coor = coor * dpi
                    coord2.append(coor)
                coords = tuple(coord2)
                draw.rectangle(coords, fill=(255, 255, 255, 0))
            print(f'Created hole for {station}')'''
        
        # Create holes for lines
        for station1, station2, line in station_pairs:
            if line in self.line_coordinates:
                for station_pair, coords in self.line_coordinates[line].items():
                    if (station_pair[0] == station1 and station_pair[1] == station2) or \
                       (station_pair[0] == station2 and station_pair[1] == station1):
                        if isinstance(coords, list):
                            for coord in coords:
                                coord2 = []
                                for coor in coord:
                                    coor = coor * dpi
                                    coord2.append(coor)
                                coord = tuple(coord2)
                                draw.rectangle(coord, fill=(255, 255, 255, 0))
                        else:
                            coord2 = []
                            for coor in coords:
                                coor = coor * dpi
                                coord2.append(coor)
                            coords = tuple(coord2)
                            draw.rectangle(coords, fill=(255, 255, 255, 0))
                        # print(f'Created line hole from {station1} to {station2}')
        
        def crop(image: Image):
            print("Cropping Image")
            image_rgb = image.convert("RGB")
            background = Image.new(image_rgb.mode, image_rgb.size, image_rgb.getpixel((0,0)))
            difference = ImageChops.difference(image_rgb, background)
            bbox = difference.getbbox()
            if bbox:
                print('Image Cropped')
                image_cropped = image.crop(bbox)
                image_padding = Image.new(image_cropped.mode, (round(image_cropped.size[0] * ((padding - 1) / 1.9 + 1)), round(image_cropped.size[1] * ((padding - 1) / 1.9 + 1))), (255,255,255))
                image_padding.paste(image_cropped, (round(image_cropped.size[0] * (padding - 1) / 5), round(image_cropped.size[1] * (padding - 1) / 2)))
                return image_padding
            else:
                print('Crop Failure')
                return image

        def trim(image: Image):
            print("Cropping Image")
            image_rgb = image.convert("RGB")
            background = Image.new(image_rgb.mode, image_rgb.size, image_rgb.getpixel((0,0)))
            difference = ImageChops.difference(image_rgb, background)
            bbox = difference.getbbox()
            if bbox:
                print('Image Cropped')
                image_cropped = image.crop(bbox)
                image_padding = Image.new(image_cropped.mode, (round(image_cropped.size[0] * padding), round(image_cropped.size[1] * vertical_padding)), (255,255,255))
                image_padding.paste(image_cropped, (round(image_cropped.size[0] * (padding - 1) / 2), round(image_cropped.size[1] * (padding - 1) / 2)))
                return image_padding
            else:
                print('Crop Failure')
                return image
        
        def watermark(image:Image):
            # Add watermark
            watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))
            watermark_draw = ImageDraw.Draw(watermark)
            watermark_text = "Generated by Trackpulse VIC"

            # Calculate font size with min and max bounds
            font_size = min(image.size[0] / text_ratio, round(image.size[1] * margin_watermark))

            # Use calculated font size
            font = ImageFont.truetype("arial.ttf", font_size)
            
            # Position text proportionally to image size
            margin = int(font_size * 0.8)  # Bottom margin
            watermark_draw.text(
            (margin, image.size[1] - margin - round(2 * image.size[1] * margin_watermark - font_size)), 
            watermark_text, 
            fill=(128, 128, 128, 255), 
            font=font
            )
            print('Watermarked')
            return Image.alpha_composite(image, watermark)
        
        # Composite and save
        modified_map = Image.alpha_composite(modified_map.convert('RGBA'), overlay)
        modified_map = trim(modified_map)
        # modified_map = watermark(modified_map)
        # modified_map = crop(modified_map)
        legend_path = self.path.replace("/map/","/map/legends/")
        modified_map = legend(modified_map, legend_path)
        if not no_compression:
            modified_map = compress(modified_map)
        print('Saving')
        modified_map.save(output_path)
        print('Done')
        return modified_map

class CoordinateFinder:
    def __init__(self, image_path, x_offset, y_offset, station_coordinates, line_coordinates):
        self.root = tk.Tk()
        self.original_image = Image.open(image_path)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.station_coordinates = station_coordinates
        self.line_coordinates = line_coordinates
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate scaling factor - increased zoom by using 1.5 instead of 0.8
        width_ratio = screen_width / self.original_image.width
        height_ratio = screen_height / self.original_image.height
        self.scale = min(width_ratio * 1.5, height_ratio * 1.5)  # 150% zoom
        
        # Resize image
        new_width = int(self.original_image.width * self.scale)
        new_height = int(self.original_image.height * self.scale)
        self.image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Create frame with scrollbars
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbars
        self.h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.frame, 
                              width=min(new_width, screen_width * 0.9),
                              height=min(new_height, screen_height * 0.9),
                              xscrollcommand=self.h_scrollbar.set,
                              yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Create image on canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Add mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel_y)  # Windows
        self.canvas.bind("<Shift-MouseWheel>", self.on_mousewheel_x)  # Windows with Shift
        self.canvas.bind("<Button-4>", self.on_mousewheel_y)  # Linux
        self.canvas.bind("<Button-5>", self.on_mousewheel_y)  # Linux
        self.canvas.bind("<Shift-Button-4>", self.on_mousewheel_x)  # Linux with Shift
        self.canvas.bind("<Shift-Button-5>", self.on_mousewheel_x)  # Linux with Shift
        
    def on_mousewheel_y(self, event):
        # Handle vertical scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")
            
    def on_mousewheel_x(self, event):
        # Handle horizontal scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, "units")
        else:
            self.canvas.xview_scroll(1, "units")
        
    def on_click(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.start_x = canvas_x
        self.start_y = canvas_y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, canvas_x, canvas_y, outline="red"
        )
        
    def on_release(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Convert coordinates back to original scale
        x1 = int(min(self.start_x, canvas_x) / self.scale)
        y1 = int(min(self.start_y, canvas_y) / self.scale)
        x2 = int(max(self.start_x, canvas_x) / self.scale)
        y2 = int(max(self.start_y, canvas_y) / self.scale)
        
        # Adjust coordinates
        y1_adj = round(int(max((y1 / dpi) - self.y_offset, (y2 / dpi) - self.y_offset)) / 50) * 50
        y2_adj = round(int(min((y1 / dpi) - self.y_offset, (y2 / dpi) - self.y_offset)) / 50) * 50
        x1_adj = round(int((x1 / dpi) - self.x_offset) / 50) * 50
        x2_adj = round(int((x2 / dpi) - self.x_offset) / 50) * 50
        
        print(f"Coordinates: ({x1_adj}, {y2_adj}, {x2_adj}, {y1_adj})")
        print(f"Copyable: ({x1_adj} + x_offset, {y2_adj} + y_offset, {x2_adj} + x_offset, {y1_adj} + y_offset),")
        
    def run(self):
        self.root.mainloop()

class CoordinateCorrector:
    def __init__(self, image_path, x_offset, y_offset, station_coordinates, line_coordinates):
        self.root = tk.Tk()
        self.original_image = Image.open(image_path)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.station_coordinates = station_coordinates
        self.line_coordinates = line_coordinates
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate initial scaling factor
        width_ratio = screen_width / self.original_image.width
        height_ratio = screen_height / self.original_image.height
        self.scale = min(width_ratio * 1.5, height_ratio * 1.5)  # 150% zoom
        
        # Create frame with scrollbars
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbars
        self.h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.frame, 
                              width=self.original_image.width * self.scale,
                              height=self.original_image.height * self.scale,
                              xscrollcommand=self.h_scrollbar.set,
                              yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Initialize image_on_canvas
        self.image_on_canvas = None
        
        # Resize image
        self.update_image()
        
        # Create image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.rectangles = {}
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Add mouse wheel scrolling and zooming
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind("<Shift-MouseWheel>", self.on_mousewheel_x)  # Windows with Shift
        self.canvas.bind("<Button-4>", self.on_mousewheel)  # Linux
        self.canvas.bind("<Button-5>", self.on_mousewheel)  # Linux
        self.canvas.bind("<Shift-Button-4>", self.on_mousewheel_x)  # Linux with Shift
        self.canvas.bind("<Shift-Button-5>", self.on_mousewheel_x)  # Linux with Shift
        
        # Create dropdown menus
        self.create_dropdown_menus()
        
        # Draw existing coordinates
        self.draw_existing_coordinates()
        
    def update_image(self):
        self.new_width = int(self.original_image.width * self.scale)
        self.new_height = int(self.original_image.height * self.scale)
        self.image = self.original_image.resize((self.new_width, self.new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.new_width, height=self.new_height)  # Update canvas size
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))  # Update scroll region
        if self.image_on_canvas:
            self.canvas.delete(self.image_on_canvas)  # Remove the old image
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")  # Add the new image
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
    def create_dropdown_menus(self):
        # Create a frame for the dropdown menus
        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(fill=tk.X)
        
        # Station dropdown menu
        self.station_var = tk.StringVar(self.root)
        self.station_var.set("Select Station")
        self.station_menu = tk.OptionMenu(self.dropdown_frame, self.station_var, *self.station_coordinates.keys(), command=self.on_station_select)
        self.station_menu.pack(side=tk.LEFT)
        
        # Line dropdown menu
        self.line_var = tk.StringVar(self.root)
        self.line_var.set("Select Line")
        self.line_menu = tk.OptionMenu(self.dropdown_frame, self.line_var, *self.line_coordinates.keys(), command=self.on_line_select)
        self.line_menu.pack(side=tk.LEFT)
        
        # Segment dropdown menu (initially empty)
        self.segment_var = tk.StringVar(self.root)
        self.segment_var.set("Select Segment")
        self.segment_menu = tk.OptionMenu(self.dropdown_frame, self.segment_var, "")
        self.segment_menu.pack(side=tk.LEFT)
        
    def on_station_select(self, station):
        self.draw_existing_coordinates()
        coords = self.station_coordinates[station]
        if isinstance(coords, list):
            for coord in coords:
                self.draw_rectangle(coord, outline="blue", tag=station)
        else:
            self.draw_rectangle(coords, outline="blue", tag=station)
        
    def on_line_select(self, line):
        self.draw_existing_coordinates()
        self.segment_var.set("Select Segment")
        self.segment_menu['menu'].delete(0, 'end')
        for segment in self.line_coordinates[line].keys():
            self.segment_menu['menu'].add_command(label=segment, command=tk._setit(self.segment_var, segment, self.on_segment_select))
        
    def on_segment_select(self, segment):
        self.draw_existing_coordinates()
        line = self.line_var.get()
        coords = self.line_coordinates[line][segment]
        if isinstance(coords, list):
            for coord in coords:
                self.draw_rectangle(coord, outline="green", tag=line)
        else:
            self.draw_rectangle(coords, outline="green", tag=line)
        
    def draw_existing_coordinates(self):
        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        
        # Draw station coordinates
        for station, coords in self.station_coordinates.items():
            if isinstance(coords, list):
                for coord in coords:
                    self.draw_rectangle(coord, outline="blue", tag=station)
            else:
                self.draw_rectangle(coords, outline="blue", tag=station)
        
        # Draw line coordinates
        for line, line_coords in self.line_coordinates.items():
            for station_pair, coords in line_coords.items():
                if isinstance(coords, list):
                    for coord in coords:
                        self.draw_rectangle(coord, outline="green", tag=line)
                else:
                    self.draw_rectangle(coords, outline="green", tag=line)
    
    def draw_rectangle(self, coords, outline="red", tag=None):
        scaled_coords = [coord * self.scale * dpi for coord in coords]
        rect = self.canvas.create_rectangle(*scaled_coords, outline=outline, tags=tag)
        self.rectangles[rect] = coords
        
    def on_mousewheel(self, event):
        # Handle zooming
        if event.delta > 0:
            self.scale *= 1.2  # Increase zoom factor
        else:
            self.scale /= 1.2  # Decrease zoom factor
        self.update_image()
        self.draw_existing_coordinates()
        
    def on_mousewheel_y(self, event):
        # Handle vertical scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")
            
    def on_mousewheel_x(self, event):
        # Handle horizontal scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, "units")
        else:
            self.canvas.xview_scroll(1, "units")
        
    def on_click(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.start_x = canvas_x
        self.start_y = canvas_y
        
        # Check if click is inside an existing rectangle
        overlapping = self.canvas.find_overlapping(canvas_x, canvas_y, canvas_x, canvas_y)
        if overlapping:
            self.rect = overlapping[0]
        else:
            self.rect = None
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, canvas_x, canvas_y, outline="red"
        )
        
    def on_release(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Convert coordinates back to original scale
        x1 = int(min(self.start_x, canvas_x) / self.scale)
        y1 = int(min(self.start_y, canvas_y) / self.scale)
        x2 = int(max(self.start_x, canvas_x) / self.scale)
        y2 = int(max(self.start_y, canvas_y) / self.scale)
        
        # Adjust coordinates
        y1_adj = round(int(max((y1 / dpi) - self.y_offset, (y2 / dpi) - self.y_offset)))
        y2_adj = round(int(min((y1 / dpi) - self.y_offset, (y2 / dpi) - self.y_offset)))
        x1_adj = round(int((x1 / dpi) - self.x_offset))
        x2_adj = round(int((x2 / dpi) - self.x_offset))
        
        print(f"Coordinates: ({x1_adj}, {y2_adj}, {x2_adj}, {y1_adj})")
        print(f"Copyable: ({x1_adj} + x_offset, {y2_adj} + y_offset, {x2_adj} + x_offset, {y1_adj} + y_offset),")
        
        # Update the coordinates in the dictionary
        if self.rect in self.rectangles:
            tag = self.canvas.gettags(self.rect)[0]
            if tag in self.station_coordinates:
                self.station_coordinates[tag] = (x1_adj, y1_adj, x2_adj, y2_adj)
            elif tag in self.line_coordinates:
                self.line_coordinates[tag] = (x1_adj, y1_adj, x2_adj, y2_adj)
        
    def run(self):
        self.root.mainloop()