import os
import json

from PIL import Image, ImageDraw, ImageFont

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

    def __init__(self, design) -> None:
        self.design_load(design)

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
            self.place_object(object)

    def place_object(self, object):

        # Check Templates for missing parameters
        if object['type'] + '.json' in os.listdir(self.folders['template']):
            with open(self.folders['template'] + '/' + object['type'] + '.json', 'r', encoding='utf-8') as file:
                # Load json file
                template = json.loads(file.read())

                # Go through every paramter
                for template_parameter in template:
                    if template_parameter not in object or object[template_parameter] is None:
                        # Set the parameter to default value to avoid errors
                        object[template_parameter] = template[template_parameter]

        # Enable custom definition usage
        for value in object:
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
        
        # Draw Text
        if object['type'] == 'text':
            if object['font'] not in os.listdir('data/fonts'):
                object['font'] = 'secrcode'
            
            text_font = ImageFont.truetype(self.folders['fonts'] + object['font'] + '/' + object['font'] + '.ttf', object['font_size'])

            # Calculate if '\n' is needed to display text
            object['text'] = self.calculate_linebreak(
                text =          object['text'],
                font =          text_font,
                max_width =     self.card_design['width'] - 2 * self.card_design['var_border_width'] - object['padding']
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

        # Insert images
        if object['type'] == 'image':
            # Check if the desired image exists
            if not os.path.exists(object['image_path']):
                # Correct the image_path to the default
                object['image_path'] = template['image_path']
            
            # Create new image instance
            new_image = Image.open(object['image_path'])

            new_image = new_image.resize(
                (
                    int(object['width']),
                    int(object['height'])
                )
            )

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

            self.card_img.paste(
                new_image,
                (
                    new_xy[0],
                    new_xy[1]
                )
            )

    def validate(self):
        if self.card_infos is not None:
            for item in self.card_design:
                if str(item) not in self.card_infos:
                    self.card_infos[str(item)] = self.card_design[str(item)]
                    self.card_infos_missing.append(str(item))
            
            if self.card_infos_missing != []:
                print('Missing:', self.card_infos_missing)
    
    def show(self):
        if self.card_img is not None:
            self.card_img.show()

    def calculate_anchor(self, xy_tuple, wh_tuple, anchor):
        return_anchor_tuple = xy_tuple

        # Anchor LT = Left Top
        if anchor == 'lt':
            # Left Top is default in pillow
            pass

        # Anchor MM = Middle Middle
        if anchor == 'mm':
            return_anchor_tuple = (
                xy_tuple[0] - (wh_tuple[0] // 2),
                xy_tuple[1] - (wh_tuple[1] // 2)
            )
        
        # Anchor RB = Right Bottom
        if anchor == 'rb':
            return_anchor_tuple = (
                xy_tuple[0] - wh_tuple[0],
                xy_tuple[1] - wh_tuple[1]
            )
        
        # Anchor RT == Right Top
        if anchor == 'rt':
            return_anchor_tuple = (
                xy_tuple[0] - wh_tuple[0],
                xy_tuple[1]
            )

        return_anchor_tuple = (
            int(return_anchor_tuple[0]),
            int(return_anchor_tuple[1])
        )
        
        return return_anchor_tuple
    
    def calculate_linebreak(self, text, font, max_width):
        
        return_text = ['']

        for item in text.split(' '):
            cache_font_width, cache_font_height = font.getsize(return_text[-1] + ' ' + item)

            if cache_font_width > max_width:
                return_text.append(item)
            else:
                return_text[-1] += ' ' + item

        true_return = ''

        for i in range(len(return_text)):
            true_return += return_text[i]

            if i < len(return_text) - 1:
                true_return += '\n'

        return true_return
