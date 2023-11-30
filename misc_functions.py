def pause(skip=False):
    if skip is False:
        input("(Press ENTER to continue)")
    #A simple function that waits for the user to press enter.
    #I made it because I was tired of repeating it over and over.

def multi_replace(text, replacement, *args):
    if len(args) >= 1:
        for item in args:
            text = text.replace(item, replacement)
    else:
        print("(multi_replace): Error: No arguments have been given!")
    return text