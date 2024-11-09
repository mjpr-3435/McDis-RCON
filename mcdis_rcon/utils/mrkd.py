sct = {
        "c:black"         : "§0",
        "c:dark_blue"     : "§1",
        "c:dark_green"    : "§2",
        "c:dark_aqua"     : "§3",
        "c:dark_red"      : "§4",
        "c:dark_purple"   : "§5",
        "c:gold"          : "§6",
        "c:gray"          : "§7",
        "c:dark_gray"     : "§8",
        "c:blue"          : "§9",
        "c:green"         : "§a",
        "c:aqua"          : "§b",
        "c:red"           : "§c",
        "c:light_purple"  : "§d",
        "c:yellow"        : "§e",
        "c:white"         : "§f",
        "f:obfuscated"    : "§k",
        "f:bold"          : "§l",
        "f:strikethrough" : "§m",
        "f:underline"     : "§n",
        "f:italic"        : "§o",
        "f:reset"         : "§r"
}

def extras(extras: list, *, text: str = '', color: str = 'gray'):
    extras = ', '.join(extras)
    return f'{{"text": "{text}", "color" : "{color}", "extra": [{extras}]}}' 

def hover(text: str, *, color: str = 'gray', hoover: str):
    return f'{{"text" : "{text}", "color" : "{color}", "hoverEvent" : {{"action": "show_text", "value": "{hoover}"}}}}'

def hover_and_suggest(text: str, *, color: str = 'gray', suggest: str, hoover: str):
    return f'{{"text" : "{text}", "color" : "{color}", "clickEvent": {{"action": "suggest_command" , "value": "{suggest}"}}, "hoverEvent" : {{"action": "show_text", "value": "{hoover}"}}}}'

def hover_and_run(text: str, *, color: str = 'gray', command: str, hoover: str):
    return f'{{"text" : "{text}", "color" : "{color}", "clickEvent": {{"action": "run_command" , "value": "{command}"}}, "hoverEvent" : {{"action": "show_text", "value": "{hoover}"}}}}'