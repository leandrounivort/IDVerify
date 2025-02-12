from openai import OpenAI
import base64
import json
import os
from dotenv import load_dotenv
from Levenshtein import distance as lev
from unidecode import unidecode

load_dotenv()
client = OpenAI()

def process_image(image_path:str, name_owner:str, lastname_owner:str) -> tuple[str,str,bool,bool]:
    '''
    Procesa la imagen extrayendo nombres y apellidos, y los compara con los provistos

    Argumentos:
        image_path (str): Ruta local a la imagen
        name_owner (str): Nombre provisto
        lastname_obner (str): Apellido provisto

    Retorna:
        JSON: Nombres obtenidos
        JSON: Apellidos obtenidos
        Bool: Resultado comparación
        Bool: Complemento resultado comparación
    '''
    base64_img = f"data:image/png;base64,{encode_image(image_path)}"
    ocr_result = get_ocr_from_image(base64_img)
    json_names = get_names_from_ocr(ocr_result)
    resultado = check_name(json_names,name_owner,lastname_owner)
    return json_names['firstname'],json_names['lastname'], resultado,not(resultado)

def encode_image(image_path):
    '''
    Codifica la imagen en base64 para ser enviado
    '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_with_misspell(image_path:str, name_owner:str, lastname_owner:str,tolerance:int) -> tuple[str,str,bool,bool]:
    '''
    Procesa la imagen extrayendo nombres y apellidos, y los compara con los provistos
    Admite un parámetro de tolerancia que indica la cantidad de caracteres en cada palabra que puede no coincidir

    Argumentos:
        image_path (str): Ruta local a la imagen
        name_owner (str): Nombre provisto
        lastname_obner (str): Apellido provisto
        tolerance (int): Cantidad de caracteres erroneos por palabra (0 es comparación exacta)

    Retorna:
        JSON: Nombres obtenidos
        JSON: Apellidos obtenidos
        Bool: Resultado comparación
        Bool: Complemento resultado comparación
    '''
    print(tolerance==None)
    base64_img = f"data:image/png;base64,{encode_image(image_path)}"
    ocr_result = get_ocr_from_image(base64_img)
    json_names = get_names_from_ocr(ocr_result)
    result = check_name_misspell(json_names,name_owner,lastname_owner,tolerance)
    return json_names['firstname'],json_names['lastname'], result,not(result)

def process_several_images(image_path:list[str], name_owner:str, lastname_owner:str) -> tuple[list[str],list[str],bool,bool]:
    '''
    Procesa una lista de imágenes extrayendo nombres y apellidos, y los compara con los provistos
    Devulve True si la comparación es exitosa para cada documento (AND)

    Argumentos:
        image_path (List[str]): Lista de rutas locales a las imágenes
        name_owner (str): Nombre provisto
        lastname_owner (str): Apellido provisto

    Retorna:
        list[JSON]: Nombres obtenidos
        list[JSON]: Apellidos obtenidos
        Bool: Resultado comparación
        Bool: Complemento resultado comparación
    '''
    names=[]
    lastname=[]
    resultado = True
    for image in image_path:
        base64_img = f"data:image/png;base64,{encode_image(image)}"
        ocr_result = get_ocr_from_image(base64_img)
        json_names = get_names_from_ocr(ocr_result)
        resultado = resultado & check_name(json_names,name_owner,lastname_owner)
        names.append(json_names['firstname'])
        lastname.append(json_names['lastname'])
    return names,lastname, resultado,not(resultado)


def get_ocr_from_image(image):
    '''
    Obtiene el texto de una imagen
    Utiliza GPT para OCR
    Devuelve en formato JSON
    TODO: En algunas ocaciones no devuelve ningún resultado
    '''    
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Return JSON document with data. Only return JSON not other text"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"{image}"}
                    }
                ],
            }
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

def get_names_from_ocr(ocr_image):
    '''
    Extrae de un texto el nombre y apellido de la persona principal en el documento.
    Devuelve en formato JSON
    TODO: Si fuera una persona jurídica, habría que cambiar el prompt y levemente las demás funciones
    '''
    prompt = "Find owner's names and lastnames in the next text):\n"
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content": "Format in JSON with keys firstname and lastname"
            },
            {
                "role": "system",
                "content": "Only the principal person"
            },
            {
                "role":"user",
            "content":prompt+ocr_image
            },    
        ],
        max_tokens=500,
        model="gpt-4o"
    )
    response = chat_completion.choices[0].message.content
    response=response.replace("```","")
    response=response.replace("json","")
    return json.loads(response)

def check_name(json_names,owner_name,owner_lastname):
    '''
    Compara los nombres obtenidos con los proporcionados
    Previo a la comparación, elimina acentos y caracteres especiales
    Compara sin tener en cuenta mayúsculas y minúsculs
    '''
    name_l = unidecode(json_names['firstname']).lower().split()
    lastname_l = unidecode(json_names['lastname']).lower().split()
    if set(unidecode(owner_name).lower().split()).issubset(set(name_l)):
        if set(unidecode(owner_lastname).lower().split()).issubset(set(lastname_l)):
            return True
    return False

def check_name_misspell(json_names,owner_name,owner_lastname,tolerance):
    '''
    Compara los nombres obtenidos con los proporcionados
    Previo a la comparación, elimina acentos y caracteres especiales
    Compara sin tener en cuenta mayúsculas y minúsculs
    Admite tener una tolerancia en cuanto a caracteres mal leídos
    '''
    name_l = unidecode(json_names['firstname']).lower().split()
    lastname_l = unidecode(json_names['lastname']).lower().split()
    owner_name_l = unidecode(owner_name).lower().split()
    owner_lastname_l = unidecode(owner_lastname).lower().split()
    result = True
    for name_o in owner_name_l:
        found = False
        for name in name_l:
            misspells = lev(name_o,name)
            if misspells<=tolerance:
                found=True
                break
        if found==False:
            result = result & False
    for lastname_o in owner_lastname_l:
        found = False
        for lastname in lastname_l:
            misspells = lev(lastname_o,lastname)
            if misspells<=tolerance:
                found=True
                break
        if found==False:
            result = result & False
    return result