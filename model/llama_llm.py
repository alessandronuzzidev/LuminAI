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
            "Por último, no uses markdown, solo texto plano. ")]
        
    def reset(self):
        self.messages = [SystemMessage(content="Eres un asistente que ayuda a los usuarios del sistema a encontrar los " +
            "archivos en los que se habla del tema que se le indica. El usuario te dirá el tema " + 
            "y tú le dirás en qué archivos del sistema se habla de ese tema. Si no se habla de ese tema en " + 
            "ningún archivo local, entonces le dirás que no se habla de ese tema en ningún archivo. " +
            "Es necesario que indiques la ruta del archivo especificado en el metadata, en path. " + 
            "Presentalo como bullet points. Debes ser escueto para que seas lo más rápido posible. " +
            "Por último, no uses markdown, solo texto plano. ")]
        
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
        formatted_prompt_str = prompt.format_messages(query=message)
        answer = self.model.invoke(formatted_prompt_str)
        return answer
    
    def generate_response(self, message_normalized, files_paths, chunk_size=1000, overlap=100):
        template_chunk = """
            Recibes un fragmento de un documento y una consulta del usuario. 
            Tu tarea es generar un resumen breve, directo y conciso, de **máximo 3 frases**, 
            enfocándote únicamente en la información del fragmento que responda a la consulta. 

            Documento (fragmento):
            {document_text}

            Consulta del usuario:
            {query}

            Respuesta:
            - Si no encuentras información que esté claramente relacionada con la consulta, responde **solo** con el token especial:
            LUMINAITOKEN1234567890
            - Si hay información parcialmente relevante pero no del todo segura, haz un resumen directo sin incluir el token.
            - Limita la respuesta a un máximo de 3 frases.
        """

        extractor = TextExtractorService()
        all_relevant_fragments = []

        def chunk_text(text, size, overlap):
            chunks = []
            start = 0
            while start < len(text):
                end = min(len(text), start + size)
                chunks.append(text[start:end])
                start += size - overlap
            return chunks
        
        already_seen = set()
        # Procesar documentos en chunks
        for file_path in files_paths:
            #print("Extrayendo texto de:", file_path)
            doc = extractor.extract_text(file_path)
            chunks = chunk_text(doc["content"], chunk_size, overlap)

            prompt_chunk = ChatPromptTemplate.from_template(template_chunk)

            for chunk in chunks:
                formatted_prompt = prompt_chunk.format_messages(
                    query=message_normalized,
                    document_text=chunk
                )
                try:
                    llm_response = self.model.invoke(formatted_prompt).strip()
                    if "LUMINAITOKEN1234567890" not in llm_response:
                        if file_path not in already_seen:
                            already_seen.add(file_path)
                            all_relevant_fragments.append((file_path, llm_response))
                except Exception as e:
                    all_relevant_fragments.append(f"[Error en {file_path}: {e}]")

        if not all_relevant_fragments:
            return "No se ha encontrado información relevante en los documentos."
        
        final_response = "He encontrado información relevante en los siguientes documentos:\n"
        for tuple_aux in all_relevant_fragments:
            _, filename = os.path.split(tuple_aux[0])
            final_response += f"- {filename} ({tuple_aux[0]}):\n {tuple_aux[1]}\n"

        return final_response
        