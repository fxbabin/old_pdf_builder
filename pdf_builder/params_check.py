import re
import warnings

def error(s, Warn=False, infile=None, line_nb=-1):
    out = "[Error]" if not Warn else "[Warning]"
    out += " {}".format(infile) if infile else ""
    out += ":{}".format(line_nb + 1) if line_nb > -1 else ""
    
    if not Warn:
        raise Exception("{} :: {}".format(out, s))
    print("{} : {}".format(out, s))

def check_bootcamp_title(title:str):
    if not title or len(title) < 3 or len(title) > 20:
        error("invalid bootcamp title length ! (length must be between 3 and 20)")
    if re.match(r'![A-Za-z ]', title):
        error("invalid bootcamp title chars ([A-Za-z ] allowed)")
    return (True)

def check_day_title(title:str):
    if not title or len(title) < 11 or len(title) > 40:
        error("invalid day title length ! (length must be between 11 and 40)")
    if re.match(r'![A-Za-z -]', title):
        error("invalid day title chars ([A-Za-z -] allowed)") 
    if re.match(r'!(^Day[0-9]{2} - .*)', title):
        error("invalid day title ! (it must be formatted as follows \"DayXX - ...\")")
    return (True)

def change_img_format(file_name:str, file_content:str):
    groups = None
    title = None
    path = None
    style = None
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)
    
    img_pattern_md = re.compile(r'[\s]*\!\[(.*)\]\((.*)\)({.*})?')
    img_pattern_html = re.compile(r'[\s]*<img.*src=[\"\']{1}(.*)[\"\']{1}.*/>')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if not img_pattern_md.match(line) and not img_pattern_html.match(line):
            out += line + "\n"
            continue

        if img_pattern_md.match(line):
            groups = img_pattern_md.findall(line)[0]
            title = groups[0]
            path = groups[1]
            style = groups[2]
        
        if img_pattern_html.match(line):
            groups = img_pattern_html.findall(line)[0]
            title = groups.split('/')[-1].split('.')[0]
            path = groups
            style = ''

        if len(title) == 0:
            error("empty image title !", Warn=True, infile=file_name, line_nb=idx)
            title = path.split('/')[-1].split('.')[0]
        if len(path) == 0:
            error("empty image path !", infile=file_name, line_nb=idx)

        if len(style) != 0 and not re.match(r'.*width=[0-9]{1,4}px.*', style):
            error("wrong image style format ! (example: '{width=250px}')", infile=file_name, line_nb=idx)
        
        path = "tmp/assets/" + path.split('/')[-1]
        out += "![{}]({}){}".format(title, path, style) + "\n"
    
    return (out)

def change_header_format(file_name:str, file_content:str):
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)
    
    code_flag = 0
    header_pattern = re.compile(r'([\s]*)([#]{1,4})[\s]+(.*)')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if re.match(r'^```.*', line):
            code_flag = 1 if code_flag == 0 else 0
        if not header_pattern.match(line):
            out += line + "\n"
            continue
        
        groups = header_pattern.findall(line)[0]
        front_space = groups[0]
        header = groups[1]
        title = groups[2]

        if code_flag:
            out += "{}{} {}\n".format(front_space, header, title)
        else:
            if len(front_space) > 0:
                error("space(s) in front of header !", Warn=True, infile=file_name, line_nb=idx)
            out += "{} {}\n".format(header, title)
    return (out)

def change_list_format(file_name:str, file_content:str):
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)
    
    code_flag = 0
    header_pattern = re.compile(r'([\s]*)([#]{1,4})[\s]+(.*)')

    return (out)
# def replace_empty_code_block_style()

# def format_equations()



