import os
import json
from PIL import Image, ImageDraw

class Card:

    card_img    = None

    card_infos  = None
    card_infos_missing = []

    card_design = None

    template_folder = 'data/object_templates'

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
        if object['type'] + '.json' in os.listdir(self.template_folder):
            with open(self.template_folder + '/' + object['type'] + '.json', 'r', encoding='utf-8') as file:
                # Load json file
                template = json.loads(file.read())

                # Go through every paramter
                for template_parameter in template:
                    if template_parameter not in object or object[template_parameter] is None:
                        # Set the parameter to default value to avoid errors
                        object[template_parameter] = template[template_parameter]

        # Enable % usage
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
