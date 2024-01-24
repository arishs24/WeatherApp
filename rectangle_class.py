import pygame

class Rectangle:
    # Initialize the Rectangle object with the provided parameters
    def __init__(self, x, y, width, height, color):
        # Set the x-coordinate of the top-left corner of the rectangle
        self.x = x

        # Set the y-coordinate of the top-left corner of the rectangle
        self.y = y

        # Set the width of the rectangle
        self.width = width

        # Set the height of the rectangle
        self.height = height

        # Set the color of the rectangle
        self.color = color


    def draw(self, screen):
        """
        Draw the rectangle on the specified screen.

        Parameters:
        - screen: The Pygame surface object representing the screen.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def get_x(self):
        """
        Get the x-coordinate of the rectangle's top-left corner.

        Returns:
        - The x-coordinate of the rectangle.
        """
        return self.x

    def get_y(self):
        """
        Get the y-coordinate of the rectangle's top-left corner.

        Returns:
        - The y-coordinate of the rectangle.
        """
        return self.y

    def get_width(self):
        """
        Get the width of the rectangle.

        Returns:
        - The width of the rectangle.
        """
        return self.width

    def get_height(self):
        """
        Get the height of the rectangle.

        Returns:
        - The height of the rectangle.
        """
        return self.height