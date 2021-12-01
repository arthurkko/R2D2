from libretranslatepy import LibreTranslateAPI

def translate(texto, origin="en", to="pt"):
    lt = LibreTranslateAPI(url="https://libretranslate.de")

    # detecta o idioma do texto
    # print(lt.detect("Hello World")) 

    # lista todos os idiomas possíveis a serem trabalhados
    # print(lt.languages())

    # tradução
    print(lt.translate(texto, origin, to))
