from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo
from nft.forms import ImageForm
from nft.models import Collection, Image as ImageModel
from django.core.files import File
import os, random, threading, time
from nft.helpers.metadata import Metadata


class GenerateNFT:
    """ Class for generating NFTs with random parameters """

    __slots__: tuple[str] = ("WIDTH", "HEIGHT", "RGB_BASE")

    def __init__(self) -> None:
        # Image sizes
        self.WIDTH = 2000
        self.HEIGHT = 2000
        # List of soft RGB colors
        self.RGB_BASE = [
            {"Cobalt blue": (2, 63, 165)}, {"Light blue-gray": (125, 135, 185)},
            {"Cadet blue Crayola": (190, 193, 212)}, {"Dull amaranth pink": (214, 188, 192)},
            {"Turkish pink": (187, 119, 132)}, {"Burgundy": (142, 6, 59)},
            {"Royal blue": (74, 111, 227)}, {"Medium magenta": (133, 149, 225)},
            {"Celadon": (172, 225, 175)}, {"Lavender pink": (247, 156, 212)},
            {"Light khaki": (240, 230, 140)}, {"Mint turquoise": (73, 126, 118)},
            {"Telemagenta": (211, 63, 106)}, {"Malachite": (11, 218, 81)},
            {"Caterpillar": (178, 236, 93)}, {"Bright purple": (205, 0, 205)},
            {"Night blue": (234, 211, 198)}, {"Yellow-orange": (237, 118, 14)},
            {"Rapeseed yellow": (243, 218, 11)}, {"Tiffany": (10, 186, 181)},
            {"Wisteria": (201, 160, 220)}, {"Mountain meadow": (48, 186, 143)},
            {"Ochre": (204, 119, 34)}, {"Thistle": (216, 191, 216)}
        ]

    @staticmethod
    def get_item(folder_name: str) -> list or None:
        """ Getting a random item from a folder """

        item_list = os.listdir(f"static/nft_options/items/{folder_name}")
        if len(item_list) > 0:
            random_choice = random.choice(item_list)
            return [random_choice, random_choice.split(".")[0]]

    @staticmethod
    def generate_text() -> list:
        """ Add text to an image """

        overlay = Image.new("RGBA", (500, 150), color=(0, 0, 0, 80))
        dr1 = ImageDraw.Draw(overlay)
        fnt = ImageFont.truetype('static/nft_options/fonts/Ubuntu-Bold.ttf', size=104)
        text = str(random.randint(100, 999)).encode("utf-8").hex()
        dr1.text(
            (14, 14),
            f'#{text}',
            font=fnt,
            fill=(255, 255, 255, 160),
        )
        return [overlay, text]

    def add_mustache(self) -> list:
        """ If successful, returns a moustache object
        Also in the 2nd argument is name of the item """

        item = self.get_item("mustache")
        if item is not None:
            return [Image.open(f"static/nft_options/items/mustache/{item[0]}").convert("RGBA"), item[1]]


    def add_subjects(self) -> list:
        """ If successful, returns an object with an image of the item
        Also in the 2nd argument is name of the item"""

        item = self.get_item("subjects")
        if item is not None:
            return [Image.open(f"static/nft_options/items/subjects/{item[0]}").convert("RGBA"), item[1]]

    def add_hat(self) -> list:
        """ If successful, returns an object with an image of a hat on it
            Also in the 2nd argument is name of the item """

        item = self.get_item("hats")
        if item is not None:
            return [Image.open(f"static/nft_options/items/hats/{item[0]}").convert("RGBA"), item[1]]

    def change_color(self, slime_image: Image):
        """ Change the color of the slime """

        # Extracting the pixels
        slime_pixels = slime_image.load()
        # Generate RGBA byte offset range
        r_byte = random.randint(0, 80)
        g_byte = random.randint(0, 80)
        b_byte = random.randint(0, 80)

        # Editing the pixels of the slime
        for w in range(self.WIDTH):
            for h in range(self.HEIGHT):
                # Get current pixel and RGBA tuple
                pixel = slime_pixels[w, h]

                if pixel != (0, 0, 0, 0):
                    # Change the color to a random range
                    # Paint only the slime object
                    slime_pixels[w, h] = (
                        pixel[0] + r_byte,
                        pixel[1] + g_byte,
                        pixel[2] + b_byte,
                        255
                    )

    def create_image(self, collection, i: str):
        """ Create image and save in db """

        # Image background
        color_dict = random.choice(self.RGB_BASE)
        background_color_name = next(iter(color_dict.keys()))
        background = next(iter(color_dict.values()))

        # Create an image object in memory
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), background)
        original_slime = Image.open("static/nft_options/original.png").convert("RGBA")

        # Generate the text and edit the slime
        overlay = self.generate_text()
        self.change_color(original_slime)

        # Adding a slime
        img.paste(original_slime, (0, 0), original_slime)

        # Add a mustache
        mustache = self.add_mustache()
        if mustache is not None:
            self.change_color(mustache[0])
            img.paste(mustache[0], (0, 0), mustache[0])
        else:
            mustache = 100

        # Adding a hat
        hat = self.add_hat()
        if hat is not None:
            self.change_color(hat[0])
            img.paste(hat[0], (0, 0), hat[0])
        else:
            hat = 100

        # Adding an item
        subject = self.add_subjects()
        if subject is not None:
            self.change_color(subject[0])
            img.paste(subject[0], (0, 0), subject[0])
        else:
            subject = 100

        # Add text with HEX value
        img.paste(overlay[0], (100, 100), overlay[0])

        # Add metadata to image
        metadata = PngInfo()
        metadata.add_text("Moustache", str(mustache[1]))
        metadata.add_text("Hat", str(hat[1]))
        metadata.add_text("Subject", str(subject[1]))
        metadata.add_text("Background", background_color_name)

        # Save the result to a shared folder
        collection_name = collection.name
        image_name = f'nft#{overlay[1]}'
        image_path = f"{image_name}.png"
        img.save(image_path, pnginfo=metadata)

        if os.path.exists(image_path):
            # Add the characteristics of each slime
            description = f'Nft {image_name} belongs to the "{collection_name}" collection\n' \
                   f"-> Items\n" \
                   f"Moustache image name: {mustache[1]}\n" \
                   f"Hat image name: {hat[1]}\n" \
                   f"Subject image name: {subject[1]}\n\n"\
                   f"-> Colors\n"\
                   f"Background: {background_color_name}"

            # Save image in db
            attributes = [
                {
                    'trait_type': 'Background',
                    'value': background_color_name
                },
                {
                    'trait_type': 'Moustache',
                    'value': mustache[1]
                },
                {
                    'trait_type': 'Hat',
                    'value': hat[1]
                },
                {
                    'trait_type': 'Subject',
                    'value': subject[1]
                }
            ]
            img = ImageModel.objects.create(
                collection_id=collection.id,
                collection_type='nft',
                name=image_name,
                description=description,
                attributes=attributes
            )
            img.image.save(image_path, File(open(image_path, 'rb')), save=True)
            img.save()
            collection.type = 'nft'
            collection.folder_name = f'collection_{collection.id}'
            collection.images.add(img)
            os.remove(image_path)
            collection.save()

        return collection

    def generate_collection(self, request, context):
        """ Generate collection """

        context = {}
        if request.method == "POST":
            form = ImageForm(request.POST or None)
            if form.is_valid():
                # save collection data
                collection = form.save()
                quantity = form.cleaned_data.get("quantity")
                threads = []
                # generate nft
                for i in range(quantity):
                    thread = threading.Thread(name="thread", target=self.create_image, args=[collection, i])
                    thread.daemon = True
                    thread.start()
                    threads.append(thread)

                # Waiting for all threads to complete
                for thread in threads:
                    thread.join()

                # set json
                set_metadata = Metadata()
                json_files = set_metadata.set_nft_metadata(collection)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> json_files", json_files)

                context.update({
                    "collection": collection
                })
        return context