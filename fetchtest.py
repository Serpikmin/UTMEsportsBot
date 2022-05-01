from cgitb import html
from ctypes import sizeof
import requests
import re
from discord import Embed
from bs4 import BeautifulSoup

CHARACTER_DICTIONARY = { "Testament": ['testament', 'testa', 'test'],
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
NUMPAD_SHORTHANDS = {
        "426H": "41236H", "624H": "63214H", "248H": "21478H", "842H": "87412H",
        "268H": "23698H", "862H": "89632H", "684H": "69874H", "486H": "47896H",
        "j.426H": "j.41236H", "j.624H": "j.63214H", "j.248H": "j.21478H",
        "j.842H": "j.87412H", "j.268H": "j.23698H", "j.862H": "j.89632H",
        "j.684H": "j.69874H", "j.486H": "j.47896H"
}

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def format_frame_data(frame_data_array, character_name, image_link):
    # output = t2a(
    #     header=["input", "damage",
    #             "guard", "startup",
    #             "active", "recovery",
    #             "onBlock", "onHit",
    #             "riscGain", "riscLoss",
    #             "level", "counter",
    #             "invuln", "prorate"],
    #     body=[frame_data_array],
    #     style=PresetStyle.thin_box
    # )
    headers=["Input", "Damage",
                "Guard", "Startup",
                "Active Frames", "Recovery Frames",
                "On Block", "On Hit",
                "Risc Gain", "Risc Loss",
                "Level", "Counter Level",
                "Invuln", "Combo Proration"]
    super_headers=["Input", "Name", "Damage",
                "Guard", "Startup",
                "Active Frames", "Recovery Frames",
                "On Block", "On Hit",
                "Risc Gain", "Risc Loss",
                "Level", "Counter Level",
                "Invuln", "Combo Proration"]
    
    output_embed = Embed(title=(character_name + ' ' + frame_data_array[0]))
    embed_entries = []
    if len(frame_data_array) == 14:
        for index in range(0, len(headers)):
          embed_entries.append('**{}**: {}'.format(headers[index], frame_data_array[index]))
    else: 
        for index in range(0, len(headers)):
          embed_entries.append('**{}**: {}'.format(super_headers[index], frame_data_array[index]))

    str_value = ('\n'.join(embed_entries))
    
    output_embed.set_image(url=image_link)
    output_embed.add_field(name='Data:', value=str_value, inline=False)
    
    return output_embed

def search_charatcer(name: str, move: str):
    # '''
    # Parse the command for the character and the move.
    # '''
    # name, move = str(command).lower().split()
    move = move.upper()
    if '.' in move:
        move = move.split('.')[0].lower() + '.' + move.split('.')[1].upper()
    '''
    Find the right URL for the character on the frame_data page.
    '''
    character_name = "BLANK"
    for key in CHARACTER_DICTIONARY:
        if name in CHARACTER_DICTIONARY[key]:
            character_name = key
            break
    if move in NUMPAD_SHORTHANDS:
        move = NUMPAD_SHORTHANDS[move]

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
    html_parent = ""
    job_elements = soup.find_all("td")
    for index, job_element in enumerate(job_elements):
        if move in job_element:
            '''
            The table of values contains anywhere from 14 to 16 values, but always have a td with an attribute after
            The 16th value goes to the next move (i.e. calling 2k -> 2s)
            '''
            frame_data = [job_elements[index]]
            index+=1
            while len(job_elements[index].attrs) == 0:
                frame_data.append(job_elements[index])
                index+=1
            html_parent = frame_data[0].parent
            break

    '''
    Remove the <td> opening and closing tags from the frame data.
    '''
    for index, data in enumerate(frame_data):
        frame_data[index] = remove_html_tags(str(data))

    # get imbed image link from parent's attributes

    image_link = 'https://dustloop.com/' + html_parent.attrs['data-details'].split(' src="')[1].split('"')[0]
    
    '''
    Create the discord embed message.
    '''
    message = format_frame_data(frame_data, character_name, image_link)

    '''
    Send the discord embed message.
    '''
    return message
