import os

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
        self.length = 0

    def __len__(self):
        return self.length

    def __repr__(self):
        return "PhotoList(photos=%s)" % self.photos

    def show_arrows(self) -> None:
        """
        This function decides which arrows it should show depending on the current state of the list
        """
        print("\n{0} - {1}\n".format(self.length, self.index))
        if self.length == 1 and self.index == 0:
           self.left_arrow.hide()
           self.right_arrow.hide()
        elif self.length == 2 and self.index == 0:
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
        return self.photos[self.index]

    def previous_photo(self):
        """
        The previous photo in the list

        Exception:
          IndexError when you're below zero.
        """
        self.index -= 1
        return self.photos[self.index]

    def get_index(self) -> int:
        """Get the current index """
        return self.index

    def get_current_photo(self):
        return self.photos[self.index]

    def at_beginning(self) -> bool:
        """Returns whether the list is at the beginning"""
        return self.index == 0

    def is_empty(self) -> bool:
        """Returns whether the list is empty"""
        return self.length == 0

    def at_end(self) -> bool:
        """Returns whether it is at the end of the list"""
        return self.index == self.length
