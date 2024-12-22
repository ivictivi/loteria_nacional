import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def comprobar_loteria(numero, importe=20):
    """
    Comprueba el premio de la Lotería de Navidad para un número específico
    
    Args:
        numero (str): Número de lotería a consultar
        importe (int): Importe jugado en euros (por defecto 20€)
        
    Returns:
        dict: Diccionario con la información del premio
    """
    # URL base de la consulta
    url = "https://www.elmundo.es/loterias/loteria-navidad/comprobar-loteria.html?nlot=37876&importe=20"
    
    # Headers más completos para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Referer': 'https://www.elmundo.es',
        'DNT': '1'
    }
    
    # Parámetros de la consulta
    # params = {
    #     'nlot': str(numero).zfill(5),  # Aseguramos que el número tenga 5 dígitos
    #     'importe': str(importe)
    # }
    
    try:
        # Realizar la petición
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print(sop
        # Intentar encontrar diferentes elementos que puedan contener la información del premio
        premio_elements = [
            soup.find('div', {'class': 'premio'}),
            soup.find('span', {'class': 'premio'}),
            soup.find('div', {'class': 'resultado'}),
            soup.find('div', {'id': 'resultado-loteria'})
        ]
        
        premio_element = next((el for el in premio_elements if el is not None), None)
        
        if premio_element:
            premio = premio_element.get_text().strip()
            
            resultado = {
                'numero': numero,
                'importe_jugado': importe,
                'premio': premio,
                'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'success'
            }
            
            # Intentar extraer el importe del premio si está disponible
            try:
                importe_premio = float(premio.replace('€', '').replace('.', '').replace(',', '.').strip())
                resultado['importe_premio'] = importe_premio
            except (ValueError, AttributeError):
                pass
                
            return resultado
        else:
            return {
                'status': 'no_premio',
                'message': 'No se ha encontrado premio para este número',
                'numero': numero,
                'importe_jugado': importe,
                'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'Error al realizar la consulta: {str(e)}',
            'numero': numero,
            'fecha_consulta': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Ejemplo de uso
if __name__ == "__main__":
    numero_loteria = "37876"
    importe = 20
    
    resultado = comprobar_loteria(numero_loteria, importe)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))