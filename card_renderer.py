from PIL import Image

CARD_WIDTH = 100
CARD_HEIGHT = 150

# Slightly muted Set-like colors
COLORS = [
    (220, 50, 47),   # Red
    (38, 139, 210),  # Blue
    (133, 153, 0)    # Green
]

SHAPES = ["diamond", "squiggle", "oval"]
SHADINGS = ["solid", "striped", "open"]
NUMBERS = [1, 2, 3]


class CardRenderer:
    def __init__(self, width=CARD_WIDTH, height=CARD_HEIGHT):
        self.asset_dir = "./assets"
        self.width = width
        self.height = height

    def render_card(self, attributes):
        """Render a single Set card from assets."""
        color_idx, shape_idx, shading_idx, number_idx = attributes
        color = COLORS[color_idx]
        shape = SHAPES[shape_idx]
        shading = SHADINGS[shading_idx]
        number = NUMBERS[number_idx]

        card = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))

        # Load the base greyscale PNG
        shape_path = f"{self.asset_dir}/{shape}-{shading}.png"
        base_img = Image.open(shape_path).convert("RGBA")

        # Tint it
        colored_shape = self._tint(base_img, color)

        # Arrange shapes vertically
        spacing = self.height // (number + 1)
        for i in range(number):
            x = self.width // 2 - colored_shape.width // 2
            y = spacing * (i + 1) - colored_shape.height // 2
            card.alpha_composite(colored_shape, (x, y))

        return card

    def _tint(self, img, color):
        """
        Tint a greyscale image to the given RGB color while keeping transparency.
        Expects a grey shape on a white background.
        """
        img = img.convert("RGBA")

        # Convert to grayscale (for safety)
        grey = img.convert("L")

        # Create a color image
        colored = Image.new("RGBA", img.size, color + (255,))

        # Use the grayscale as a mask (invert if necessary)
        mask = Image.eval(grey, lambda x: 255 - x)  # white -> transparent

        # Composite tinted color through the mask
        tinted = Image.composite(colored, Image.new("RGBA", img.size, (255, 255, 255, 0)), mask)

        return tinted