class Displayable(object):
    max_display_level = 1
    def display(self, level, *args, **kwargs):
        if level <= self.max_display_level:
            print(*args, **kwargs)