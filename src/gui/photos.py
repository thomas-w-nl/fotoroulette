import os

from src.common import log


class PhotoList:
    """
    A simple class to keep track of the photos being sent by the hardware with an index
    The index allows us to disable different arrows depending on the amount and position of
    the photos.

    Args:
       photos: The amount of photos to start with

    Exception:
       IndexError
    """

    def __init__(self, builder, photos=[]):
        self.photos = []
        self.left_arrow = builder.get_object("LeftArrow")
        self.right_arrow = builder.get_object("RightArrow")
        self.index = 0
        self.length = -1

    def __len__(self):
        return self.length

    def __repr__(self):
        return "PhotoList(photos=%s)" % self.photos

    def _show_arrows(self) -> None:
        """
        This function decides which arrows it should show depending on the current state of the list
        """
        if self.length == 0 and self.index == 0:
           self.left_arrow.hide()
           self.right_arrow.hide()
        elif self.index == 0:
           self.left_arrow.hide()
           self.right_arrow.show()
        elif self.index == self.length:
            self.left_arrow.show()
            self.right_arrow.hide()
        else:
            self.left_arrow.show()
            self.right_arrow.show()

    def append(self, photo):
        """
        Add a photo to the list

        Args:
           photo: The photo you want to add
        """
        self.photos.append(photo)
        self.length += 1

    def clear(self):
        """
        Clear the list
        """
        self.photos.clear()
        self.index = 0

    def to_start(self):
        self.index = 0

    def next_photo(self):
        """
        Go to the next photo in the list

        Exception:
          IndexError when you you've already reached the max
        """
        self.index += 1

        if self.index > self.length:
            raise IndexError

        photo = self.photos[self.index]
        self._show_arrows()
        return photo

    def previous_photo(self):
        """
        The previous photo in the list

        Exception:
          IndexError when you're below zero.
        """
        self.index -= 1
        if self.index < 0:
            raise IndexError

        photo = self.photos[self.index]
        self._show_arrows()
        return photo

    def get_index(self) -> int:
        """Get the current index """
        return self.index

    def get_current_photo(self):
        return self.photos[self.index]

    def is_empty(self) -> bool:
        """Returns whether the list is empty"""
        return self.length == -1
