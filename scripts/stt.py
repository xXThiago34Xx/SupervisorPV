import speech_recognition as sr
import pyttsx3
import pyautogui

# Inicializar reconocimiento de voz y síntesis de texto a voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def escuchar_numero():
    with sr.Microphone() as source:
        print("Por favor, di un número...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Reconocer el audio usando Google Speech Recognition
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"Escuché: {texto}")

            # Intentar convertir el texto a número
            if texto.isdigit():
                numero = int(texto)
                print(f"El número reconocido es: {numero}")
                return numero
            else:
                print("No entendí un número. Inténtalo de nuevo.")
                engine.say("Repítelo..")
                engine.runAndWait()
                return None

        except sr.UnknownValueError:
            print("No entendí lo que dijiste. Por favor, repítelo.")
            engine.say("Repítelo.")
            engine.runAndWait()

        except sr.RequestError as e:
            print(f"Error al comunicarse con el servicio de reconocimiento de voz: {e}")
            engine.say("Error al comunicarse con el servicio de reconocimiento de voz.")
            engine.runAndWait()

while True:
    numero = None
    while numero is None:
        # Escuchar hasta que se reconozca un número correctamente
        numero = escuchar_numero()
    
    # Simular la escritura del número (como si fuera pegado)
    pyautogui.write(str(numero))
    print(f"Pegando número: {numero}")
    
    # Después de pegar el número, reinicia el proceso para escuchar otro número
    print("Reiniciando para escuchar otro número...\n")
