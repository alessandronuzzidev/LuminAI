from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.schema import SystemMessage, HumanMessage
import torch

from abstract_session import AbstractSession

class HFSession(AbstractSession):
    
    def __init__(self):
        super().__init__()
        # Carga el tokenizer, asegurando que apunte al archivo tokenizer.model si es necesario,
        # o que la carpeta contenga el archivo.
        # AutoTokenizer suele encontrarlo automáticamente si el archivo tokenizer.model está en la carpeta.
        # Si tienes problemas, podrías intentar especificar trust_remote_code=True
        # para algunos modelos (aunque no suele ser necesario para modelos locales de Llama 3 estándar).
        
        # También puedes intentar forzar el tipo de tokenizador si sabes cuál es (LlamaTokenizer/LlamaTokenizerFast)
        # from transformers import LlamaTokenizerFast
        # self.tokenizer = LlamaTokenizerFast.from_pretrained("./hf_models/llama3")
        
        # Sin embargo, AutoTokenizer debería ser suficiente si el archivo tokenizer.model está ahí.
        # El warning del "legacy behavior" no es un error, es solo una notificación.
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct/original", legacy=False)
        
        # Resto del código...
        self.llm = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B-Instruct/original",
            torch_dtype=torch.bfloat16, 
            device_map="auto" 
        )
        
        # Asegurarse de que el token de padding esté definido para la generación,
        # esto es importante si no lo tiene por defecto.
        if self.tokenizer.pad_token is None:
            # Para Llama 3, a menudo se usa el token EOS como PAD o se añade uno nuevo.
            # Puedes probar con tokenizer.eos_token o añadir un token nuevo.
            self.tokenizer.pad_token = self.tokenizer.eos_token 
            # Si se añade un nuevo token, se debería redimensionar el embedding de tokens del modelo
            # self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            # self.llm.resize_token_embeddings(len(self.tokenizer))
        self.llm = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B-Instruct/original",
            torch_dtype=torch.bfloat16, # O torch.float16, o torch.float32 si no tienes GPU bfloat16
            device_map="auto" # Para que transformers detecte automáticamente la mejor configuración de dispositivo
        )
        # Algunos modelos Llama3 pueden necesitar un token de relleno si no lo tienen por defecto
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.llm.resize_token_embeddings(len(self.tokenizer))
        
    def start_session(self):
        self.session_available = True
        self.messages = [
            SystemMessage(content="Responde en castellano de España exclusivamente. ")
        ]
        print("Session started.")
    
    def send_message(self, message):
        self.messages.append(HumanMessage(content=message))
        
        # Convertir el historial de mensajes a un formato que el modelo entienda
        # Llama 3 usa un formato de chat específico. 'apply_chat_template' es la forma recomendada.
        input_ids = self.tokenizer.apply_chat_template(
            [{"role": msg.type, "content": msg.content} for msg in self.messages], 
            add_generation_prompt=True, 
            return_tensors="pt"
        ).to(self.llm.device) # Mover los IDs al mismo dispositivo que el modelo

        # Definir los tokens de parada para la generación
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>") # Este es específico de Llama 3
        ]

        # Generar la respuesta
        outputs = self.llm.generate(
            input_ids,
            max_new_tokens=512, # Longitud máxima de la respuesta
            eos_token_id=terminators,
            do_sample=True,
            temperature=0,
            top_p=0.9
        )
        
        # Decodificar la respuesta
        # Asegurarse de que solo se decodifica el nuevo texto generado, no todo el historial.
        response_text = self.tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
        
        # Añadir la respuesta del modelo al historial de mensajes
        self.messages.append(SystemMessage(content=response_text))
        return response_text
    
    def get_messages(self):
        return self.messages
    
    def end_session(self):
        self.messages = None
        self.session_available = False
        print("Session ended.")
        print("Resources cleared.")
    

import sys
import os
from transformers.models.llama.modeling_llama import LlamaRMSNorm
import torch.nn as nn
nn.RMSNorm = LlamaRMSNorm

print(f"--- Diagnóstico del Entorno ---")
print(f"Ejecutable de Python: {sys.executable}")
print(f"Versión de Python: {sys.version}")
print(f"sys.path: {sys.path}") # Esto muestra dónde busca Python los módulos

try:
    import torch
    print(f"Torch instalado: True")
    print(f"Versión de Torch según el script: {torch.__version__}")
    # Esto comprobará si RMSNorm existe en *este* módulo de torch
    print(f"torch.nn.RMSNorm existe: {'RMSNorm' in dir(torch.nn)}")
    # Esta es la línea que te está dando el error y la incluimos para confirmar
    print(f"torch.nn.RMSNorm real: {torch.nn.RMSNorm}")
except ImportError:
    print("¡Torch no encontrado en este entorno!")
except AttributeError:
    print("torch.nn.RMSNorm NO existe en esta versión/instalación de Torch.")

print(f"--- Fin del Diagnóstico ---")


model = HFSession()
model.start_session()
response = model.send_message("¿Qué es la inteligencia artificial?")
print(response)
model.end_session()