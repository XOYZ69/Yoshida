import os
import json
import copy
import string
import textwrap
import requests

from PIL        import Image, ImageDraw, ImageFont, ImageFilter
from colorama   import Fore
from numpy      import int_, var
from tqdm       import tqdm
from io         import BytesIO

from modules.Image_math import get_alpha_calculation, get_alpha_v2_calculation
from modules.image_info import img_get_color_avg

class Card:

    true_path = __file__.split('modules')[0]

    card_img    = None

    card_infos  = None
    card_infos_missing = []

    card_design = None

    folders = {
        'template':     true_path + 'data/object_templates/',
        'card_designs': true_path + 'data/card_designs/',
        'fonts':        true_path + 'data/fonts/'
    }

    debug_level = 5

    def __init__(self, design) -> None:
        self.design_load(design)

        if 'var_border_width' not in self.card_design:
            self.card_design['var_border_width'] = 0

    def design_load(self, design_name):
        # If design is not in design folder exit here
        if design_name + '.json' not in os.listdir('data/card_designs'):
            return None
        
        card_design_path = 'data/card_designs/' + design_name + '.json'

        with open(card_design_path, 'r', encoding='utf-8') as design:
            self.card_design = json.loads(design.read())

    def create(self, card_infos=None):
        self.card_infos = self.card_design

        # Insert given information
        if card_infos != None:
            for param in card_infos:
                if param in self.card_design:
                    self.card_design[param] = card_infos[param]
        
        # Validate and fill up missing inforamtion with base information
        self.validate()

        self.card_infos = self.format_values(self.card_infos, returner=True)

        # Create the card
        self.card_img = Image.new('RGBA',
            (
                self.card_design['width'],
                self.card_design['height']
            )
        )

        # Create ImageDraw
        self.card_img_draw = ImageDraw.Draw(self.card_img)

        # Draw Card Design
        for object in self.card_design['body']:
            object = self.validate_object(object)
            self.build_object(object)
        
        self.log(Fore.LIGHTYELLOW_EX + 'Finished Building')

    def validate_object(self, object_cache):
        object = object_cache

        # Check Templates for missing parameters
        if object['type'] + '.json' in os.listdir(self.folders['template']):
            with open(self.folders['template'] + '/' + object['type'] + '.json', 'r', encoding='utf-8') as file:
                # Load json file
                self.template = json.loads(file.read())

                # Go through every paramter
                for template_parameter in self.template:
                    if template_parameter not in object or object[template_parameter] is None:
                        # Set the parameter to default value to avoid errors
                        object[template_parameter] = self.template[template_parameter]
        
        return object
    
    def build_object(self, object):

        if object['logic'] is None or object['logic'] == '':
            self.format_values(object)
        else:
            cache = object['logic'].split('#')

            if cache[0] == 'FOR':
                # Syntax: 'FOR#$var_name#int_from#int_to[#int_steps]'
                
                # Remove the $ to get the variable name
                variable = cache[1][1:]
                
                cacher_dict = {
                        'int_from': cache[2],
                        'int_to':   cache[3],
                    }

                if len(cache) > 4:
                    cacher_dict['int_steps'] = cache[4]

                cache_d = self.format_values(
                    cacher_dict,
                    returner = True
                )

                int_from  = int(cache_d['int_from'])
                int_to    = int(cache_d['int_to'])

                if len(cache) > 4:
                    int_steps = int(cache_d['int_steps'])
                else:
                    int_steps = 1

                for object[variable] in range(int_from, int_to, int_steps):
                    self.card_infos[variable] = object[variable]

                    self.format_values(copy.copy(object))
                    # self.log(Fore.LIGHTMAGENTA_EX + str(object[variable]), Fore.LIGHTYELLOW_EX + str(object))
            
            elif cache[0] == 'IF':
                pass

            elif cache[0] == 'VISIBILITY':
                if cache[1] in ['TRUE', 'true', '1', 'yes', 'YES', 'y']:
                    self.format_values(copy.copy(object))
                elif cache[1] == 'IF':
                    cache_var = cache[2][1:].split(' == ')
                    if eval("'" + self.card_design[cache_var[0]] + "' == " + cache_var[1]) == True:
                        self.format_values(copy.copy(object))

    def format_values(self, object, returner = False):
        
        # Enable custom definition usage
        for value in object:
            if isinstance(object[value], str):
                # Build formula if starts with >>
                if object[value][0:2] == '>>':
                    object[value] = object[value][2:]
                    cache_formula = ''

                    for item in object[value].split(' '):
                        cache_item = item

                        # Handle Variables defined by '$'
                        if item[0] == '$':
                            cache_item = str(self.card_design[item[1:]]) + ' '

                        # Check if the percentage is from wdith or height
                        if item[-1] == '%':
                            if value in ['x', 'width']:
                                cache_item = (float(item.replace('%', '')) / 100) * self.card_img.width
                            elif value in ['y', 'height']:
                                cache_item = (float(item.replace('%', '')) / 100) * self.card_img.height
                        elif 'w_%' in item:
                            cache_item = (float(item.replace('w_%', '')) / 100) * self.card_img.width
                        elif 'h_%' in item:
                            cache_item = (float(item.replace('h_%', '')) / 100) * self.card_img.height

                        # Reverse Pixel Definition (Can't explain it. it Works)
                        if item[0] == '!':
                            if value in ['x', 'width']:
                                cache_item = self.card_img.width - float(item.replace('!', ''))
                            elif value in ['y', 'height']:
                                cache_item = self.card_img.height - float(item.replace('!', ''))
                        elif 'w_!' in item:
                            cache_item = self.card_img.width - float(item.replace('w_!', ''))
                        elif 'h_!' in item:
                            cache_item = self.card_img.width - float(item.replace('h_!', ''))

                        cache_formula += str(cache_item) + ' '
                    
                    formula_output = eval(cache_formula)

                    # self.log(Fore.BLUE + cache_formula)
                    # self.log(Fore.YELLOW + str(formula_output))

                    object[value] = formula_output

                    # self.log(Fore.LIGHTRED_EX + '<< ' + Fore.LIGHTMAGENTA_EX + cache_formula + Fore.RESET + ' -> ' + Fore.LIGHTCYAN_EX + str(formula_output) + Fore.RESET)
                
                # String Builder
                elif object[value][0:2] == '<<':
                    cache = object[value][2:].split('&')

                    cache_out = ''

                    for string_value in cache:
                        if string_value[0] == '$':
                            cache_out += str(self.card_infos[string_value[1:]])
                        else:
                            cache_out += string_value
                    
                    object[value] = cache_out

                    self.log(Fore.LIGHTRED_EX + '<< ' + Fore.LIGHTMAGENTA_EX + str(object[value]) + Fore.RESET)
                else:
                    # Support old handling if string is not defined as a formula

                    if isinstance(object[value], str) and '%' in object[value]:
                        # Check if the percentage is from wdith or height
                        if value in ['x', 'width']:
                            object[value] = (int(object[value].replace('%', '')) / 100) * self.card_img.width
                        elif value in ['y', 'height']:
                            object[value] = (int(object[value].replace('%', '')) / 100) * self.card_img.height
                    
                    # Handle Variables defined by '$' at the beginning
                    if isinstance(object[value], str) and object[value][0] == '$':
                        object[value] = self.card_design[object[value][1:]]

                    # Reverse Pixel Definition (Can't explain it. it Works)
                    if isinstance(object[value], str) and object[value][0] == '!':
                        if value in ['x', 'width']:
                            object[value] = self.card_img.width - int(object[value].replace('!', ''))
                        elif value in ['y', 'height']:
                            object[value] = self.card_img.height - int(object[value].replace('!', ''))
                            
        if returner:
            return object
        else:
            self.place_object(object)


    def place_object(self, object):

        self.log(Fore.CYAN + 'Placing [' + object['type'] + ']' + Fore.RESET)

        # Draw Rectangles
        if object['type'] == 'rectangle':
            self.card_img_draw.rounded_rectangle(
                [
                    object['x'],
                    object['y'],
                    object['x'] + object['width'],
                    object['y'] + object['height']
                ],
                fill    = object['color'],
                radius  = object['border_radius']
            )
        
        # Draw Ellipse (also used for circles)
        if object['type'] == 'ellipse':
            self.card_img_draw.ellipse(
                [
                    object['x'],
                    object['y'],
                    object['x'] + object['width'],
                    object['y'] + object['height']
                ],
                fill    = object['color']
            )
        
        # Draw Polygon
        if object['type'] == 'polygon':
            self.card_img_draw.polygon(
                xy      = object['xy_sequence'],
                fill    = object['color'],
                outline = object['outline_color'],
                width   =  object['outline_width']
            )
        
        # Draw Text
        if object['type'] == 'text':
            if object['font'] not in os.listdir('data/fonts'):
                object['font'] = 'secrcode'
            
            text_font = ImageFont.truetype(self.folders['fonts'] + object['font'] + '/' + object['font'] + '.ttf', object['font_size'])

            # If text got a defined texbox use it instead
            if object['max_width'] is not None:
                max_width = object['max_width']
                f = 'red'
            else:
                f = 'blue'
                if object['max_width'] is None:
                    max_width = self.card_design['width'] - 2 * self.card_design['var_border_width'] - object['padding']
                else:
                    max_width = object['max_width']

            # Calculate if '\n' is needed to display text
            object['text'] = self.calculate_linebreak_old(
                text =          object['text'],
                font =          text_font,
                max_width =     max_width,
                stretch_line =  object['stretch_line']
            )
            
            self.card_img_draw.text(
                (
                    object['x'],
                    object['y']
                ),
                text    = object['text'],
                fill    = object['color'],
                font    = text_font,
                anchor  = object['anchor'],
                align   = object['align'],
                spacing = object['spacing']
            )
            
            if '\n' in object['text']:
                self.log('\\n in >> ' + object['text'])

        # Insert images
        if object['type'] == 'image':
            # Check if the desired image exists
            if 'https://' in object['image_path']:
                new_image = Image.open(BytesIO(requests.get(object['image_path']).content)).convert('RGBA')
            else:
                if not os.path.exists(object['image_path']):
                    # Correct the image_path to the default
                    object['image_path'] = self.template['image_path']
            
                # Create new image instance
                new_image = Image.open(object['image_path']).convert('RGBA')

            # Automatic Ratio Saling to full width
            if object['height'] == 'auto':
                ratio = new_image.size[0] / new_image.size[1]
                object['height'] = object['width'] * ratio

            if object['width'] == 'auto':
                ratio = new_image.size[1] / new_image.size[0]
                object['width'] = object['height'] * ratio

            new_image = new_image.resize(
                (
                    int(object['width']),
                    int(object['height'])
                ),
                resample=Image.BILINEAR
            )

            self.log(new_image.size)

            # Filters
            if object['filter'] is not None:
                filters_cache = object['filter'].split(',')
                for filter in range(len(filters_cache)):
                    if 'filter_config' not in object or len(object['filter_config']) < (filter + 1):
                        continue

                    match filters_cache[filter]:
                        case 'sharpen':
                            new_image = new_image.filter(ImageFilter.SHARPEN)
                        case 'detail':
                            new_image = new_image.filter(ImageFilter.DETAIL)
                        case 'edge':
                            new_image = new_image.filter(ImageFilter.EDGE_ENHANCE)
                        case 'find_edges':
                            new_image = new_image.filter(ImageFilter.FIND_EDGES)
                        case 'gradient':
                            match object['filter_config'][filter]['direction']:
                                case 'bottom':
                                    for x_pixel in range(new_image.size[0]):
                                        for y_pixel in range(object['filter_config'][filter]['length']):
                                            pixel_back  = self.card_img.getpixel((object['x'] + x_pixel, object['y'] + new_image.size[1] - y_pixel - 1))

                                            pixel_front = new_image.getpixel((x_pixel, new_image.size[1] - y_pixel - 1))

                                            pixel_blend_ration = y_pixel / object['filter_config'][filter]['length']

                                            pixel_blend = (
                                                int((pixel_back[0] * (1 - pixel_blend_ration)) + (pixel_front[0] * pixel_blend_ration)),
                                                int((pixel_back[1] * (1 - pixel_blend_ration)) + (pixel_front[1] * pixel_blend_ration)),
                                                int((pixel_back[2] * (1 - pixel_blend_ration)) + (pixel_front[2] * pixel_blend_ration)),
                                                int((pixel_back[3] * (1 - pixel_blend_ration)) + (pixel_front[3] * pixel_blend_ration))
                                            )

                                            new_image.putpixel(
                                                (x_pixel, new_image.size[1] - y_pixel - 1),
                                                pixel_blend)

                        case 'cut':
                            match object['filter_config'][filter]['side']:
                                case 'top':
                                    new_image = new_image.crop(
                                        (0, object['filter_config'][filter]['length'], object['width'], object['height'])
                                    )
                                    object['height'] -= object['filter_config'][filter]['length']



            # Calculate anchor positions
            new_xy = self.calculate_anchor(
                (
                    object['x'],
                    object['y']
                ),
                (
                    object['width'],
                    object['height']
                ),
                object['anchor']
            )

            for img_h in tqdm(range(int(object['height'])), desc='Placing Image [' + object['desc'] + ']'):
                for img_w in range(int(object['width'])):
                    current_pixel = new_image.getpixel((img_w, img_h))

                    match object['blend_mode']:
                        case 'basic':
                            # Basic Blend
                            current_pixel = (
                                current_pixel[0],
                                current_pixel[1],
                                current_pixel[2],
                                current_pixel[3]
                            )
                    
                        # Substract Blend
                        case 'substract':
                            current_pixel = (
                                min(
                                    self.card_img.getpixel(
                                        (new_xy[0] + img_w, new_xy[1] + img_h)
                                    )[0] - current_pixel[0],
                                    0
                                ),
                                min(
                                    self.card_img.getpixel(
                                        (new_xy[0] + img_w, new_xy[1] + img_h)
                                    )[1] - current_pixel[1],
                                    0
                                ),
                                min(
                                    self.card_img.getpixel(
                                        (new_xy[0] + img_w, new_xy[1] + img_h)
                                    )[2] - current_pixel[2],
                                    0
                                ),
                                current_pixel[3]
                            )

                    # Use alpha calculations to enable alpha matte
                    if object['use_alpha']:
                        current_pixel = get_alpha_calculation(
                            current_pixel,
                            self.card_img.getpixel((new_xy[0] + img_w, new_xy[1] + img_h))
                        )
                    elif object['use_alpha_v2']:
                        current_pixel = get_alpha_v2_calculation(
                            current_pixel,
                            self.card_img.getpixel((new_xy[0] + img_w, new_xy[1] + img_h))
                        )

                    self.card_img.putpixel(
                        (new_xy[0] + img_w, new_xy[1] + img_h),
                        current_pixel
                    )

    def validate(self):
        if self.card_infos is not None:
            for item in self.card_design:
                if str(item) not in self.card_infos:
                    self.card_infos[str(item)] = self.card_design[str(item)]
                    self.card_infos_missing.append(str(item))
            
            if self.card_infos_missing != []:
                self.log('Missing:', self.card_infos_missing)
        
        self.card_infos['var_true_path'] = self.true_path
    
    def show(self):
        if self.card_img is not None:
            self.card_img.show()

    def calculate_anchor(self, xy_tuple, wh_tuple, anchor):
        return_anchor_tuple = xy_tuple

        match anchor:
            # Anchor LT = Left Top
            case 'lt':
                # Left Top is default in pillow
                pass

            # Anchor MM = Middle Middle
            case 'mm':
                return_anchor_tuple = (
                    xy_tuple[0] - (wh_tuple[0] // 2),
                    xy_tuple[1] - (wh_tuple[1] // 2)
                )
            
            # Anchor RB = Right Bottom
            case 'rb':
                return_anchor_tuple = (
                    xy_tuple[0] - wh_tuple[0],
                    xy_tuple[1] - wh_tuple[1]
                )
            
            # Anchor RT == Right Top
            case 'rt':
                return_anchor_tuple = (
                    xy_tuple[0] - wh_tuple[0],
                    xy_tuple[1]
                )

        return_anchor_tuple = (
            int(return_anchor_tuple[0]),
            int(return_anchor_tuple[1])
        )
        
        return return_anchor_tuple
    
    def calculate_linebreak_old(self, text, font, max_width, stretch_line = False):
        
        return_text = ['']

        for item in text.split(' '):
            cache_font_width = font.getlength(return_text[-1] + ' ' + item)

            if cache_font_width > max_width:
                return_text.append(item)
            else:
                return_text[-1] += ' ' + item if return_text != [''] else item

                self.log(str(cache_font_width) + ' of ' + str(max_width) + ': ' + return_text[-1])

        true_return = ''

        for i in range(len(return_text)):
            cache = return_text[i]

            if stretch_line and i < len(return_text) - 1:
                cache = self.stretch_line(cache, font, max_width)
            
            true_return += cache

            if i < len(return_text) - 1:
                true_return += '\n'

        return true_return
    
    def calculate_linebreak(self, text, font, max_width, stretch_line = False):
        avg_char_width = sum(font.getlength(char) for char in string.ascii_letters) / len(string.ascii_letters)

        max_char_count = max_width // avg_char_width
        
        if stretch_line:
            # Wrap the text
            true_return_list = textwrap.wrap(text, width = max_char_count)

            # Build the return
            true_return = ''

            for x in true_return_list:
                true_return += self.stretch_line(x, font, max_width)

            for line in range(len(true_return_list)):
                true_return += true_return_list[line]
                if line < len(true_return_list) - 1:
                    true_return += '\n'
        else:
            true_return = textwrap.fill(text, width = max_char_count)

        self.log(Fore.RED + 'calculate_linebreak(self, ' + text + ', ' + str(font) + ', ' + str(max_width) + '\n' + Fore.CYAN + true_return + Fore.RESET)

        self.log(Fore.BLUE + 'max_char_count: ' + str(max_char_count))
        self.log(Fore.BLUE + 'avg_char_width: ' + str(avg_char_width))
        self.log(Fore.BLUE + 'max_width:      ' + str(max_width))

        return true_return

    def stretch_line(self, line, font, max_width):
        self.log('stretch_line')

        line_split = line.split(' ')

        spaces = []

        for i in range(len(line_split)):
            spaces.append(' ')

        index = 0

        cache_line = line
        cache_line_w = font.getlength(cache_line)

        while cache_line_w < max_width:
            spaces[index] += ' '

            cache_line = ''

            # Build line
            for i in range(len(line_split)):
                cache_line += line_split[i]

                if i < len(spaces) - 1:
                    cache_line += spaces[i]

            cache_line_w = font.getlength(cache_line)

            # Increase index
            index += 1

            if index >= len(spaces):
                index = 0
            
            self.log(cache_line)
            self.log(spaces)

        return cache_line
        

    
    def log(self, text, debug_level = 0):
        if debug_level > self.debug_level:
            print('Log:', text)
