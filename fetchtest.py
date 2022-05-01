import requests
import re
from bs4 import BeautifulSoup
from table2ascii import table2ascii as t2a, PresetStyle


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def format_frame_data(frame_data_array):
    output = t2a(
        header=["input", "damage",
                "guard", "startup",
                "active", "recovery",
                "onBlock", "onHit",
                "riscGain", "riscLoss",
                "level", "counter",
                "invuln", "prorate"],
        body=[frame_data_array],
        style=PresetStyle.thin_box
    )
    return output

def main(command: str):
    '''
    Parse the command for the character and the move.
    '''
    name, move = str(command).lower().split()
    move = move.upper()
    if '.' in move:
        move = move.split('.')[0].lower() + '.' + move.split('.')[1].upper()
    character_dictionary = { "Testament": ['testament', 'testa', 'test'],
                   "Jack-O": ['jack-o', 'jacko', 'jack'],
                   "Nagoriyuki": ['nago', 'nagoriyuki'],
                   "Millia_Rage": ['millia', 'millia-rage'],
                   "Chipp_Zanuff": ['chipp-zanuff', 'chipp', 'chip'],
                   "Sol_Badguy": ['sol', 'sol-badguy'],
                   "Ky_Kiske": ['ky-kiske', 'ky', 'kiske', 'kyle'],
                   "May": ['may'],
                   "Zato-1": ['zato', 'zato1', 'zato-1', 'zato-one', 'zato=1'],
                   "I-No": ['ino', 'i-no'],
                   "Happy_Chaos": ['happy-chaos', 'chaos', 'happy'],
                   "Baiken": ['baiken'],
                   "Anji_Mito": ['anji', 'anji-mito'],
                   "Leo_Whitefang": ['monkey', 'leo', 'leo-whitefang'],
                   "Faust": ['faust'],
                   "Axl_Low": ['axl', 'axl-low'],
                   "Potemkin": ['pot', 'potemkin'],
                   "Ramlethal_Valentine": ['ram', 'ramlethal',
                                           'ramlethal-valentine'],
                   "Giovanna": ['gio', 'giovanna'],
                   "Goldlewis_Dickinson": ['gl', 'gld,' 'gold', 'goldlewis',
                                           'goldlewis-dickinson']}
    '''
    Find the right URL for the character on the frame_data page.
    '''
    character_name = "BLANK"
    for key in character_dictionary:
        if name in character_dictionary[key]:
            character_name = key
            break

    if character_name != "BLANK":
        #perform https request
        URL = "https://dustloop.com/wiki/index.php?title=GGST/"
        URL += character_name
        URL += "/Frame_Data"
    else:
        raise NameError

    '''
    Send the request to the URL.
    '''
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    '''
    all frame_data is stored in a table. However, the individual pieces of data
    are stored in <td> tags. With 14 pieces of data per row/move.
    '''

    frame_data = []
    job_elements = soup.find_all("td")
    for index, job_element in enumerate(job_elements):
        if move in job_element:
            '''
            The table of values only contain 14 values.
            The 16th value goes to the next move (i.e. calling 2k -> 2s)
            '''
            frame_data = job_elements[index: index + 14]
            break

    '''
    Remove the <td> opening and closing tags from the frame data.
    '''
    for index, data in enumerate(frame_data):
        frame_data[index] = remove_html_tags(str(data))

    '''
    Create the discord embed message.
    '''
    message = format_frame_data(frame_data)


    '''
    Send the discord embed message.
    '''
    return message
