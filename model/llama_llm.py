from langchain.schema import SystemMessage, HumanMessage
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from services.text_extractor_service import TextExtractorService
import subprocess
import os

class LlamaLLM:

    def __init__(self):
        subprocess.run(["ollama", "pull", "llama3.2"], 
                       check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        self.model = OllamaLLM(model="llama3.2")
        self.messages = [SystemMessage(content="Eres un asistente que ayuda a los usuarios del sistema a encontrar los " +
            "archivos en los que se habla del tema que se le indica. El usuario te dirá el tema " + 
            "y tú le dirás en qué archivos del sistema se habla de ese tema. Si no se habla de ese tema en " + 
            "ningún archivo local, entonces le dirás que no se habla de ese tema en ningún archivo. " +
            "Es necesario que indiques la ruta del archivo especificado en el metadata, en path. " + 
            "Presentalo como bullet points. Debes ser escueto para que seas lo más rápido posible. " +
            "Por último, no uses markdown, sino HTML. Por ejemplo, si usas ** para negrita, usa <b> en su lugar. " +
            "Si usas * para cursiva, usa <i> en su lugar. Si usas ` para código, usa <code> en su lugar. " +
            "Si usas [texto](enlace), usa <a href='enlace'>texto</a> en su lugar. ")]
        
    def reset(self):
        self.messages = [SystemMessage(content="Eres un asistente que ayuda a los usuarios del sistema a encontrar los " +
            "archivos en los que se habla del tema que se le indica. El usuario te dirá el tema " + 
            "y tú le dirás en qué archivos del sistema se habla de ese tema. Si no se habla de ese tema en " + 
            "ningún archivo local, entonces le dirás que no se habla de ese tema en ningún archivo. " +
            "Es necesario que indiques la ruta del archivo especificado en el metadata, en path. " + 
            "Presentalo como bullet points. Debes ser escueto para que seas lo más rápido posible. " +
            "Por último, no uses markdown, sino HTML. Por ejemplo, si usas ** para negrita, usa <b> en su lugar. " +
            "Si usas * para cursiva, usa <i> en su lugar. Si usas ` para código, usa <code> en su lugar. " +
            "Si usas [texto](enlace), usa <a href='enlace'>texto</a> en su lugar. ")]
        
    def send_message(self, message):
        self.messages.append(HumanMessage(content=message))
        reply = self.model.invoke(self.message)
        self.messages.append(reply)
        return reply

    def query_normalizer(self, message):
        template = """
            Eres un preprocesador de lenguaje natural.  
            Tu tarea es recibir consultas en lenguaje coloquial y transformarlas en frases limpias, breves y optimizadas para búsqueda semántica.  

            Reglas:
            - Elimina palabras irrelevantes como "documento donde se habla de", "quiero saber", "me gustaría", "encuéntrame", etc.  
            - Mantén solo las palabras clave importantes y el contexto temporal o temático.  
            - No reformules ni inventes, solo limpia.  
            - Devuelve únicamente la frase limpia, sin explicaciones ni texto adicional.

            Ejemplos:
            Entrada: "Documento donde se ahbla de barcos hundidos en el siglo XX"  
            Salida: "Barcos hundidos en el siglo XX"

            Entrada: "Quiero información sobre juicios de Nuremberg después de la Segunda Guerra Mundial"  
            Salida: "Juicios de Nuremberg Segunda Guerra Mundial"

            Entrada: "Me gustaría saber qué se dice acerca de la inteligencia artificial en la medicina moderna"  
            Salida: "Inteligencia artificial en la medicina moderna"

            Entrada: "Encuéntrame textos relacionados con la caída del Imperio Romano de Occidente"  
            Salida: "Caída del Imperio Romano de Occidente"

            Ahora procesa la siguiente consulta:
            Entrada: "{query}"
            Salida:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        formatted_prompt_str = prompt.format(query=message).lower()
        answer = self.model.invoke(formatted_prompt_str)
        return answer
    
    def generate_response(self, message_normalized, files_paths):
        template = template = """
            Recibes el texto de un documento y una consulta del usuario. Tu tarea es generar un resumen breve, 
            directo y conciso, de **máximo 5 frases**, enfocándote únicamente en la información del documento 
            que responda a la consulta. Evita frases introductorias como "El documento trata sobre..." o 
            "Claro, aquí tienes un resumen...". Ve al grano y explica el contenido relevante.

            Documento:
            {document_text}

            Consulta del usuario:
            {query}

            Respuesta:
            - Si no encuentras información que esté claramente relacionada con la consulta, responde **solo** con el token especial:
            LUMINAITOKEN1234567890
            - Si hay información parcialmente relevante pero no del todo segura, haz un resumen directo sin incluir el token.
            - Limita la respuesta a un máximo de 5 frases.
        """

        extractor = TextExtractorService()
    
        responses = []

        prompt_template = ChatPromptTemplate.from_template(template)
        
        for file_path in files_paths:
            content = extractor.extract_text(file_path)

            formatted_prompt = prompt_template.format_messages(
                query=message_normalized,
                document_text=content
            )
            
            try:
                llm_response = self.model.invoke(formatted_prompt)
                if llm_response.__contains__("LUMINAITOKEN1234567890"):
                    continue
            except Exception as e:
                llm_response = f"Error al procesar el archivo: {e}"

            _, filename = os.path.split(file_path)

            responses.append(f"<b>{filename}</b> <i>{file_path}</i>:<br>{llm_response.strip()}")       
        
        if responses == []:
            return "No se ha encontrado información relevante en los documentos."
        return "\n\n".join(responses)
        