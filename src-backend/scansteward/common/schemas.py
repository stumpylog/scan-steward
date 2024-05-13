from pydantic import conlist

# TODO: This doesn't appear to work well?
IntListWithItemsType = conlist(int, min_length=1)
