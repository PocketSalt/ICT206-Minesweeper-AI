class Tile:

    # trying to see if static works
    correct_flag_count = 0

    def __init__(self, val: int, vis: bool):
        self.value = val
        self.visible = vis
        self.flagged = False

    def reveal(self):
        self.visible = True

        if self.value == -1:
            print("explode.")

    def toggle_flag(self):
        self.flagged = not self.flagged

        # basically, if flagged and is bomb, flag.
        if self.value == -1 and self.flagged:
            Tile.correct_flag_count += 1

        # and if you unselect, then remove
        if self.value == -1 and not self.flagged:
            Tile.correct_flag_count -= 1


    def return_value(self):
        if self.visible and not self.flagged:
            return self.value
        else:
            return -2