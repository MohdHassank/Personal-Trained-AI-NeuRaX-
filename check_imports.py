import importlib
mods = ['PyQt5','groq','AppOpener','pywhatkit','bs4','PIL','rich','requests','keyboard','cohere','googlesearch','selenium','mtranslate','pygame','edge_tts','webdriver_manager','dotenv']
for mod in mods:
    try:
        importlib.import_module(mod)
        print(mod, 'OK')
    except Exception as e:
        print(mod, 'MISSING', e)
