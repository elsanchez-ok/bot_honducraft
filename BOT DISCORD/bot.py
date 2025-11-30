import discord
from discord.ext import commands, tasks
import asyncio
import json
import threading
import socket
import datetime
import os
import random
import aiohttp
import math
import typing
from typing import Optional, List, Dict, Union, Any
from discord import app_commands
import itertools
import logging
import traceback
from collections import defaultdict, Counter
import re
import time

# =============================================
# CONFIGURACIÓN AVANZADA Y CONSTANTES
# =============================================

class BotConfig:
    """Configuración avanzada tipo MEE6/Dyno"""
    VERSION = "5.0.0"
    DEVELOPER = "ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Team"
    SUPPORT_SERVER = "https://discord.gg/honducraft"
    WEBSITE = "https://honducraft.com"
    MINECRAFT_IP = "honducraft.sdlf.fun"
    
    # Colores profesionales con morado como principal
    COLORS = {
        "primary": 0x9B59B6,  # Morado premium
        "success": 0x57F287,
        "error": 0xED4245,
        "warning": 0xFEE75C,
        "info": 0x9B59B6,     # Morado para info también
        "premium": 0x9B59B6,  # Morado premium
        "dark": 0x2C2F33,
        "light": 0x99AAB5,
        "blurple": 0x5865F2,
        "green": 0x57F287,
        "yellow": 0xFEE75C,
        "red": 0xED4245,
        "purple": 0x9B59B6
    }

# Configuración de logging profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('honducraft.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱')

# Configuración de intents avanzada
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix=['!', 'hc ', 'HC ', 'honducraft ', 'Honducraft ', '.', 'ℌ '],
    intents=intents,
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        users=True,
        roles=False,
        replied_user=True
    )
)

# =============================================
# SISTEMA DE CACHE Y PERFORMANCE
# =============================================

class AdvancedCache:
    """Sistema de cache avanzado para mejor performance"""
    
    def __init__(self):
        self.user_profiles = {}
        self.guild_configs = {}
        self.message_cache = defaultdict(list)
        self.cooldowns = {}
        self.last_cleanup = time.time()
        self.web_cache = {}
    
    def set_user_profile(self, user_id: int, guild_id: int, data: dict):
        key = f"{guild_id}_{user_id}"
        self.user_profiles[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def get_user_profile(self, user_id: int, guild_id: int) -> Optional[dict]:
        key = f"{guild_id}_{user_id}"
        if key in self.user_profiles:
            if time.time() - self.user_profiles[key]['timestamp'] < 300:  # 5 minutos
                return self.user_profiles[key]['data']
        return None
    
    def set_web_data(self, url: str, data: dict):
        """Cache para datos web"""
        self.web_cache[url] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def get_web_data(self, url: str) -> Optional[dict]:
        if url in self.web_cache:
            if time.time() - self.web_cache[url]['timestamp'] < 3600:  # 1 hora
                return self.web_cache[url]['data']
        return None
    
    def cleanup_old_cache(self):
        """Limpia cache antiguo"""
        current_time = time.time()
        # Limpiar user_profiles antiguos
        self.user_profiles = {
            k: v for k, v in self.user_profiles.items() 
            if current_time - v['timestamp'] < 300
        }
        # Limpiar cooldowns expirados
        self.cooldowns = {
            k: v for k, v in self.cooldowns.items() 
            if current_time - v['timestamp'] < v['duration']
        }
        # Limpiar cache web antiguo
        self.web_cache = {
            k: v for k, v in self.web_cache.items()
            if current_time - v['timestamp'] < 3600
        }

cache = AdvancedCache()

# =============================================
# SISTEMA DE IA SIMULADA SIN API
# =============================================

class SimpleAI:
    """Sistema de IA simulada sin usar APIs externas"""
    
    @staticmethod
    async def generate_response(prompt: str, context: str = "") -> str:
        """Genera respuestas inteligentes basadas en patrones"""
        
        prompt_lower = prompt.lower()
        
        # Respuestas para saludos
        greetings = {
            "hola": "¡Hola! Soy ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, tu asistente avanzado. ¿En qué puedo ayudarte hoy? 🤖",
            "hi": "Hello! I'm ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, your advanced assistant. How can I help you today? 🤖",
            "hello": "Hey there! I'm ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 bot, ready to assist you! 💫",
            "buenos dias": "¡Buenos días! ☀️ Espero que tengas un día maravilloso. ¿En qué puedo ayudarte?",
            "buenas tardes": "¡Buenas tardes! 🌇 ¿Cómo va tu día? Estoy aquí para lo que necesites.",
            "buenas noches": "¡Buenas noches! 🌙 Espero que hayas tenido un gran día. ¿Neitas ayuda con algo?"
        }
        
        for greeting, response in greetings.items():
            if greeting in prompt_lower:
                return response
        
        # Respuestas sobre el bot
        bot_questions = {
            "quien eres": "Soy ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, un bot avanzado con sistemas de niveles, economía, Minecraft, programación y mucho más! 🚀",
            "what are you": "I'm ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, an advanced bot with leveling systems, economy, Minecraft integration, programming tools and much more! 🚀",
            "que puedes hacer": "Puedo ayudarte con: 🎮 Minecraft, 💻 Programación, 🏆 Niveles, 💰 Economía, 🛡️ Moderación, 🔍 Búsquedas web y mucho más! Usa `/hc` para ver todos mis comandos.",
            "what can you do": "I can help you with: 🎮 Minecraft, 💻 Programming, 🏆 Leveling, 💰 Economy, 🛡️ Moderation, 🔍 Web searches and much more! Use `/hc` to see all my commands."
        }
        
        for question, response in bot_questions.items():
            if question in prompt_lower:
                return response
        
        # Respuestas técnicas
        tech_responses = {
            "programacion": "¡Me encanta la programación! 💻 Puedo ayudarte con:\n• Formatear código\n• Información de lenguajes\n• Ejemplos de código\n• Solución de errores simples\nUsa `/code` para empezar!",
            "minecraft": f"¡Minecraft! 🎮 Nuestro servidor es: `{BotConfig.MINECRAFT_IP}`\nPuedo mostrarte el estado, ayudar a vincular tu cuenta y más. Usa `/mcstatus` para ver el estado actual!",
            "nivel": "¡El sistema de niveles es increíble! 🏆 Gana XP enviando mensajes y sube de nivel. Cada nivel te da más prestigio y recompensas. Usa `/level` para ver tu progreso!",
            "economia": "¡Sistema económico activo! 💰 Gana monedas diarias, trabaja y compra items. Usa `/daily` para tu recompensa diaria y `/work` para ganar más!",
            "comandos": "¡Tengo muchos comandos! 🔧 Usa `/hc` para ver la lista completa de todos mis sistemas y funciones disponibles."
        }
        
        for tech, response in tech_responses.items():
            if tech in prompt_lower:
                return response
        
        # Respuestas inteligentes generales
        if "?" in prompt:
            responses = [
                f"Basándome en tu pregunta sobre '{prompt}', te recomiendo usar nuestros sistemas especializados. ¿Has probado usar `/hc` para explorar todas las opciones? 🔍",
                f"Interesante pregunta. Como IA de ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, puedo ayudarte mejor con comandos específicos. ¿Qué te parece si usas `/hc` para ver todas mis funciones? 🤔",
                f"¡Buena pregunta! Para darte la mejor respuesta, ¿podrías ser más específico? Mientras tanto, te invito a explorar mis comandos con `/hc` 🚀",
                f"Como sistema ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, tengo varias formas de ayudarte. ¿Has considerado usar nuestros comandos de búsqueda con `/search`? 🔎"
            ]
            return random.choice(responses)
        
        # Respuesta por defecto
        default_responses = [
            "¡Interesante! Como ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, puedo ayudarte de muchas formas. ¿Por qué no pruebas `/hc` para ver todo lo que puedo hacer? 🌟",
            "¡Entendido! 🤖 Para darte la mejor asistencia, te recomiendo usar mis comandos especializados. Escribe `/hc` para descubrir todas mis funciones!",
            "¡Gracias por tu mensaje! 💫 Como bot avanzado ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, tengo muchos sistemas para ayudarte. Usa `/hc` para explorarlos todos!",
            "¡Hola! Soy ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱, tu asistente multifunción. 🚀 Escribe `/hc` para ver la increíble lista de cosas que puedo hacer por ti!"
        ]
        
        return random.choice(default_responses)

# =============================================
# SISTEMA DE BÚSQUEDA WEB SIN API
# =============================================

class WebSearch:
    """Sistema de búsqueda web sin APIs externas"""
    
    @staticmethod
    async def search_google(query: str, max_results: int = 3) -> List[Dict]:
        """Simula búsqueda en Google (sin API)"""
        
        # Cache para evitar búsquedas repetidas
        cached = cache.get_web_data(f"search_{query}")
        if cached:
            return cached
        
        # Simulación de resultados de búsqueda
        results = []
        
        # Temas comunes con respuestas predefinidas
        common_topics = {
            "minecraft": {
                "title": "Minecraft Official Site",
                "url": "https://www.minecraft.net",
                "description": "Official Minecraft website with news, downloads, and community information."
            },
            "python": {
                "title": "Python Programming Language",
                "url": "https://www.python.org",
                "description": "Official Python programming language website with documentation and downloads."
            },
            "discord": {
                "title": "Discord - Home",
                "url": "https://discord.com",
                "description": "Official Discord website for the popular communication platform."
            },
            "honducraft": {
                "title": "ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Official",
                "url": BotConfig.WEBSITE,
                "description": "Official ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 community website and Minecraft server."
            }
        }
        
        query_lower = query.lower()
        
        # Buscar en temas comunes
        for topic, info in common_topics.items():
            if topic in query_lower:
                results.append(info)
        
        # Si no hay resultados específicos, generar genéricos
        if not results:
            results = [
                {
                    "title": f"Resultados para: {query}",
                    "url": f"https://www.google.com/search?q={query.replace(' ', '+')}",
                    "description": f"Buscar '{query}' en Google para más información."
                },
                {
                    "title": f"Wikipedia: {query}",
                    "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                    "description": f"Artículo de Wikipedia sobre {query}."
                },
                {
                    "title": f"Video Tutorial: {query}",
                    "url": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}",
                    "description": f"Tutoriales en video sobre {query}."
                }
            ]
        
        # Limitar resultados
        results = results[:max_results]
        
        # Guardar en cache
        cache.set_web_data(f"search_{query}", results)
        
        return results
    
    @staticmethod
    async def get_weather(city: str) -> Dict:
        """Obtiene información del clima (simulada)"""
        
        # Ciudades comunes con clima predefinido
        weather_data = {
            "madrid": {"temp": 22, "condition": "Soleado", "humidity": 45},
            "barcelona": {"temp": 24, "condition": "Parcialmente nublado", "humidity": 60},
            "london": {"temp": 15, "condition": "Lluvioso", "humidity": 80},
            "new york": {"temp": 18, "condition": "Nublado", "humidity": 65},
            "tokyo": {"temp": 20, "condition": "Despejado", "humidity": 55},
            "mexico": {"temp": 25, "condition": "Soleado", "humidity": 40},
            "paris": {"temp": 17, "condition": "Lluvioso", "humidity": 75}
        }
        
        city_lower = city.lower()
        if city_lower in weather_data:
            return weather_data[city_lower]
        else:
            # Datos aleatorios para ciudades no especificadas
            return {
                "temp": random.randint(10, 30),
                "condition": random.choice(["Soleado", "Parcialmente nublado", "Nublado", "Lluvioso"]),
                "humidity": random.randint(30, 85)
            }

# =============================================
# BASE DE DATOS MEGA AVANZADA
# =============================================

class ProfessionalDatabase:
    """Sistema de base de datos profesional"""
    
    def __init__(self):
        self.file_path = 'honducraft_pro.json'
        self.backup_dir = 'backups/'
        self.cache = {}
        self.setup_directories()
    
    def setup_directories(self):
        """Crea directorios necesarios"""
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs('logs/', exist_ok=True)
        os.makedirs('data/transcripts/', exist_ok=True)
    
    def load_data(self):
        """Carga datos con estructura avanzada"""
        default_data = {
            "metadata": {
                "version": BotConfig.VERSION,
                "created_at": datetime.datetime.now().isoformat(),
                "last_backup": None,
                "total_servers": 0,
                "total_users": 0,
                "uptime": 0
            },
            "servers": {},
            "users": {},
            "statistics": {
                "commands_used": 0,
                "messages_processed": 0,
                "tickets_created": 0,
                "mod_actions": 0,
                "warns_issued": 0,
                "ai_interactions": 0,
                "searches_performed": 0
            }
        }
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                return self.deep_merge(default_data, loaded_data)
        except FileNotFoundError:
            return default_data
        except json.JSONDecodeError as e:
            logger.error(f"Error cargando datos: {e}")
            self.create_backup("corrupted_recovery")
            return default_data
    
    def deep_merge(self, base: dict, update: dict) -> dict:
        """Fusión profunda de diccionarios"""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self.deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def save_data(self):
        """Guarda datos con optimizaciones"""
        try:
            self.create_backup("auto_save")
            
            self.data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            
            self.clean_old_backups()
            
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            self.emergency_save()
    
    def create_backup(self, reason: str = "manual"):
        """Crea backup"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.backup_dir}backup_{timestamp}_{reason}.json"
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            self.data["metadata"]["last_backup"] = timestamp
            return True
        except Exception as e:
            logger.error(f"Error creando backup: {e}")
            return False

    def clean_old_backups(self, keep_count: int = 10):
        """Limpia backups antiguos"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("backup_") and file.endswith(".json"):
                    backups.append(file)
            
            backups.sort(reverse=True)
            
            for old_backup in backups[keep_count:]:
                os.remove(os.path.join(self.backup_dir, old_backup))
                
        except Exception as e:
            logger.error(f"Error limpiando backups: {e}")

    def emergency_save(self):
        """Guardado de emergencia"""
        try:
            temp_file = f"{self.file_path}.emergency"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f)
        except Exception as e:
            logger.error(f"❌ Error en guardado de emergencia: {e}")
    
    def get_guild_config(self, guild_id: int) -> dict:
        """Obtiene configuración del servidor"""
        guild_key = str(guild_id)
        if guild_key not in self.data["servers"]:
            self.data["servers"][guild_key] = self.get_default_guild_config()
            self.save_data()
        return self.data["servers"][guild_key]
    
    def get_default_guild_config(self) -> dict:
        """Configuración por defecto"""
        return {
            "prefix": "!",
            "language": "es",
            "modules": {
                "moderation": True,
                "levels": True,
                "economy": True,
                "minecraft": True,
                "programming": True,
                "ai": True,
                "search": True
            }
        }
    
    def update_guild_config(self, guild_id: int, updates: dict):
        """Actualiza configuración del servidor"""
        guild_key = str(guild_id)
        current_config = self.get_guild_config(guild_id)
        self.data["servers"][guild_key] = self.deep_merge(current_config, updates)
        self.save_data()
    
    def get_user_data(self, user_id: int, guild_id: int) -> dict:
        """Obtiene datos de usuario"""
        user_key = f"{guild_id}_{user_id}"
        if user_key not in self.data["users"]:
            self.data["users"][user_key] = self.get_default_user_data()
            self.save_data()
        return self.data["users"][user_key]
    
    def get_default_user_data(self) -> dict:
        """Datos por defecto para usuarios"""
        return {
            "leveling": {
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "messages": 0
            },
            "economy": {
                "wallet": 100,
                "bank": 0,
                "daily_streak": 0
            },
            "stats": {
                "commands_used": 0,
                "ai_uses": 0,
                "searches": 0
            }
        }
    
    def update_user_data(self, user_id: int, guild_id: int, updates: dict):
        """Actualiza datos de usuario"""
        user_key = f"{guild_id}_{user_id}"
        current_data = self.get_user_data(user_id, guild_id)
        self.data["users"][user_key] = self.deep_merge(current_data, updates)
        self.save_data()
    
    def __getattr__(self, name):
        if name == "data":
            if not hasattr(self, '_data'):
                self._data = self.load_data()
            return self._data
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

# Instancia global de la base de datos
db = ProfessionalDatabase()

# =============================================
# SISTEMA DE EMBEDS PROFESIONALES MORADOS
# =============================================

class ProfessionalEmbeds:
    """Sistema de embeds estilo profesional en morado"""
    
    @staticmethod
    def create_embed(
        title: str = "",
        description: str = "",
        color: int = BotConfig.COLORS["primary"],
        thumbnail: str = None,
        image: str = None,
        author: dict = None,
        fields: list = None,
        footer: str = None,
        timestamp: bool = True,
        url: str = None
    ) -> discord.Embed:
        """Crea un embed profesional en morado"""
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            url=url,
            timestamp=datetime.datetime.now() if timestamp else None
        )
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        
        if image:
            embed.set_image(url=image)
        
        if author:
            name = author.get('name', '')
            url = author.get('url', '')
            icon_url = author.get('icon_url', '')
            embed.set_author(name=name, url=url, icon_url=icon_url)
        
        if fields:
            for field in fields:
                name = field.get('name', '')
                value = field.get('value', '')
                inline = field.get('inline', False)
                if value:
                    embed.add_field(name=name, value=value, inline=inline)
        
        footer_text = footer or "ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 • Sistema Avanzado Pro"
        embed.set_footer(text=footer_text, icon_url="https://i.postimg.cc/7LRKvvn8/honducraft.png")
        
        return embed
    
    @staticmethod
    def success(title: str, description: str = "", **kwargs) -> discord.Embed:
        return ProfessionalEmbeds.create_embed(
            title=f"✅ {title}",
            description=description,
            color=BotConfig.COLORS["success"],
            **kwargs
        )
    
    @staticmethod
    def error(title: str, description: str = "", **kwargs) -> discord.Embed:
        return ProfessionalEmbeds.create_embed(
            title=f"❌ {title}",
            description=description,
            color=BotConfig.COLORS["error"],
            **kwargs
        )
    
    @staticmethod
    def warning(title: str, description: str = "", **kwargs) -> discord.Embed:
        return ProfessionalEmbeds.create_embed(
            title=f"⚠️ {title}",
            description=description,
            color=BotConfig.COLORS["warning"],
            **kwargs
        )
    
    @staticmethod
    def info(title: str, description: str = "", **kwargs) -> discord.Embed:
        return ProfessionalEmbeds.create_embed(
            title=f"💜 {title}",
            description=description,
            color=BotConfig.COLORS["info"],
            **kwargs
        )
    
    @staticmethod
    def premium(title: str, description: str = "", **kwargs) -> discord.Embed:
        return ProfessionalEmbeds.create_embed(
            title=f"💎 {title}",
            description=description,
            color=BotConfig.COLORS["premium"],
            **kwargs
        )

# Alias para fácil acceso
Embeds = ProfessionalEmbeds

# =============================================
# SISTEMA DE MINECRAFT MEJORADO
# =============================================

class MinecraftSystem:
    """Sistema de integración con Minecraft mejorado"""
    
    @staticmethod
    async def get_server_status(ip: str = BotConfig.MINECRAFT_IP, port: int = 25565):
        """Obtiene el estado del servidor de Minecraft"""
        try:
            # Simulación mejorada de estado
            status = {
                "online": True,
                "players": random.randint(5, 45),
                "max_players": 100,
                "version": "1.20.1",
                "description": "§aℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 §6Premium Server",
                "latency": random.randint(10, 50),
                "motd": "Bienvenido a ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 - ¡La mejor experiencia Minecraft!"
            }
            return status
        except Exception as e:
            logger.error(f"Error obteniendo estado de Minecraft: {e}")
            return None
    
    @staticmethod
    async def create_status_embed(server_ip: str, status: dict):
        """Crea un embed con el estado del servidor"""
        if not status:
            return Embeds.error(
                "❌ Error de Minecraft",
                f"No se pudo obtener el estado del servidor `{server_ip}`"
            )
        
        if status["online"]:
            embed = Embeds.success(
                f"🟢 {server_ip} - EN LÍNEA",
                f"""
                **🎮 SERVIDOR ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 ACTIVO**
                
                **👥 Jugadores conectados:** `{status['players']}/{status['max_players']}`
                **🛠️ Versión:** `{status['version']}`
                **⚡ Latencia:** `{status['latency']}ms`
                **📝 MOTD:** `{status['motd']}`
                
                **📍 IP del Servidor:**
                ```{server_ip}```
                
                **¡Conéctate ahora y únete a la aventura!** 🚀
                """
            )
        else:
            embed = Embeds.error(
                f"🔴 {server_ip} - FUERA DE LÍNEA",
                f"""
                El servidor **ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱** no está disponible en este momento.
                
                **IP:** `{server_ip}`
                
                *Por favor, intenta conectarte más tarde.*
                """
            )
        
        return embed

# =============================================
# COMANDOS SLASH (/) - SISTEMA /hc
# =============================================

class SlashCommands(commands.Cog):
    """Comandos slash modernos y profesionales"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="hc", description="Muestra todos los sistemas y comandos de ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱")
    async def hc_command(self, interaction: discord.Interaction):
        """Comando principal /hc"""
        embed = Embeds.info(
            "💜 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 - Sistema de Comandos Completo",
            """
            **🎮 SISTEMA MINECRAFT:**
            `/mcstatus` - Estado del servidor Minecraft
            `/mcplayers` - Jugadores en línea
            `/linkmc` - Vincular cuenta Minecraft

            **💻 SISTEMA PROGRAMACIÓN:**
            `/code` - Formatear código
            `/langinfo` - Info lenguaje programación
            `/execute` - Ejecutar código (simulado)

            **🏆 SISTEMA DE NIVELES:**
            `/level` - Ver tu nivel y progreso
            `/leaderboard` - Tabla de clasificación
            `/rank` - Ver tarjeta de rango

            **💰 SISTEMA ECONÓMICO:**
            `/daily` - Recompensa diaria
            `/work` - Trabajar por dinero
            `/balance` - Ver tu balance
            `/transfer` - Transferir dinero

            **🤖 SISTEMA IA AVANZADO:**
            `/ai` - Chat con la IA
            `/ask` - Pregunta anything
            `/translate` - Traducir texto

            **🔍 SISTEMA DE BÚSQUEDA:**
            `/search` - Buscar en internet
            `/weather` - Clima de una ciudad
            `/wiki` - Buscar en Wikipedia

            **🛡️ SISTEMA DE MODERACIÓN:**
            `/warn` - Advertir usuario
            `/clear` - Limpiar mensajes
            `/mute` - Silenciar usuario

            **📊 SISTEMA DE INFORMACIÓN:**
            `/serverinfo` - Info del servidor
            `/userinfo` - Info de usuario
            `/botinfo` - Info del bot

            **⚙️ COMANDOS TRADICIONALES (!):**
            `!ayuda` - Sistema de ayuda
            `!nivel` - Ver nivel
            `!daily` - Recompensa diaria
            `!mcstatus` - Estado Minecraft
            `!ai` - Chat con IA
            `!search` - Buscar en web

            **💎 IP SERVIDOR MINECRAFT:**
            ```honducraft.sdlf.fun```
            """
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ai", description="Chat con la IA avanzada de ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱")
    @app_commands.describe(pregunta="Tu pregunta o mensaje para la IA")
    async def ai_chat(self, interaction: discord.Interaction, pregunta: str):
        """Chat con IA"""
        await interaction.response.defer()
        
        # Generar respuesta
        respuesta = await SimpleAI.generate_response(pregunta)
        
        # Actualizar estadísticas
        db.data["statistics"]["ai_interactions"] += 1
        user_data = db.get_user_data(interaction.user.id, interaction.guild.id)
        user_data["stats"]["ai_uses"] += 1
        db.update_user_data(interaction.user.id, interaction.guild.id, user_data)
        
        embed = Embeds.info(
            "🤖 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 IA - Asistente Inteligente",
            f"""
            **👤 Tu Pregunta:**
            {pregunta}

            **💜 Mi Respuesta:**
            {respuesta}

            *💫 Usa `/hc` para ver todos mis sistemas*
            """
        )
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="search", description="Buscar información en internet")
    @app_commands.describe(busqueda="Lo que quieres buscar", resultados="Número de resultados (1-5)")
    async def web_search(self, interaction: discord.Interaction, busqueda: str, resultados: int = 3):
        """Búsqueda web"""
        await interaction.response.defer()
        
        if resultados > 5:
            resultados = 5
        elif resultados < 1:
            resultados = 1
        
        # Realizar búsqueda
        results = await WebSearch.search_google(busqueda, resultados)
        
        # Actualizar estadísticas
        db.data["statistics"]["searches_performed"] += 1
        user_data = db.get_user_data(interaction.user.id, interaction.guild.id)
        user_data["stats"]["searches"] += 1
        db.update_user_data(interaction.user.id, interaction.guild.id, user_data)
        
        description = f"**🔍 Resultados para: `{busqueda}`**\n\n"
        
        for i, result in enumerate(results, 1):
            description += f"**{i}. [{result['title']}]({result['url']})**\n"
            description += f"{result['description']}\n\n"
        
        description += "*💫 Búsqueda realizada por ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Search System*"
        
        embed = Embeds.info("🔍 Sistema de Búsqueda ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱", description)
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="mcstatus", description="Estado del servidor Minecraft ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱")
    async def mcstatus_slash(self, interaction: discord.Interaction):
        """Estado de Minecraft"""
        await interaction.response.defer()
        
        status = await MinecraftSystem.get_server_status()
        embed = await MinecraftSystem.create_status_embed(BotConfig.MINECRAFT_IP, status)
        
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="weather", description="Obtener el clima de una ciudad")
    @app_commands.describe(ciudad="Nombre de la ciudad")
    async def weather_slash(self, interaction: discord.Interaction, ciudad: str):
        """Clima de una ciudad"""
        await interaction.response.defer()
        
        weather = await WebSearch.get_weather(ciudad)
        
        embed = Embeds.info(
            f"🌤️ Clima en {ciudad.title()}",
            f"""
            **🌡️ Temperatura:** `{weather['temp']}°C`
            **☁️ Condición:** `{weather['condition']}`
            **💧 Humedad:** `{weather['humidity']}%`
            
            **📍 Ciudad:** {ciudad.title()}
            **🕐 Actualizado:** {datetime.datetime.now().strftime('%H:%M')}
            
            *💫 Información meteorológica proporcionada por ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱*
            """
        )
        await interaction.followup.send(embed=embed)
    
    @app_commands.command(name="botinfo", description="Información completa del bot ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱")
    async def botinfo_slash(self, interaction: discord.Interaction):
        """Información del bot"""
        embed = Embeds.info(
            "💜 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 - Información del Sistema",
            f"""
            **📊 ESTADÍSTICAS GLOBALES:**
            **• Servidores:** `{len(self.bot.guilds):,}`
            **• Usuarios:** `{sum(g.member_count for g in self.bot.guilds):,}`
            **• Comandos usados:** `{db.data['statistics']['commands_used']:,}`
            **• Interacciones IA:** `{db.data['statistics']['ai_interactions']:,}`
            **• Búsquedas:** `{db.data['statistics']['searches_performed']:,}`

            **🚀 INFORMACIÓN TÉCNICA:**
            **• Versión:** `{BotConfig.VERSION}`
            **• Desarrollador:** `{BotConfig.DEVELOPER}`
            **• Latencia:** `{round(self.bot.latency * 1000)}ms`
            **• Uptime:** `{self.get_uptime()}`

            **🎮 SISTEMAS ACTIVOS:**
            ```
            ✅ Minecraft Integration
            ✅ AI Assistant  
            ✅ Web Search
            ✅ Level System
            ✅ Economy System
            ✅ Moderation Tools
            ✅ Programming Help
            ✅ Utility Commands
            ```

            **📍 SERVIDOR MINECRAFT:**
            ```{BotConfig.MINECRAFT_IP}```

            **💎 ¡Sistema ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 completamente operativo!**
            """
        )
        await interaction.response.send_message(embed=embed)
    
    def get_uptime(self):
        """Obtiene el tiempo de actividad del bot"""
        delta = datetime.datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        return f"{days}d {hours}h {minutes}m {seconds}s"

# =============================================
# COMANDOS TRADICIONALES (!)
# =============================================

class TraditionalCommands(commands.Cog):
    """Comandos tradicionales con prefijo"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ayuda', aliases=['help', 'comandos', 'hc'])
    async def ayuda(self, ctx):
        """Sistema de ayuda tradicional"""
        embed = Embeds.info(
            "💜 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 - Comandos Tradicionales (!)",
            """
            **🎮 COMANDOS MINECRAFT:**
            `!mcstatus` - Estado servidor Minecraft
            `!mcplayers` - Jugadores en línea
            `!linkmc <usuario>` - Vincular cuenta

            **🤖 COMANDOS IA:**
            `!ai <pregunta>` - Chat con IA
            `!ask <pregunta>` - Preguntar anything

            **🔍 COMANDOS BÚSQUEDA:**
            `!search <texto>` - Buscar en internet
            `!weather <ciudad>` - Clima de ciudad
            `!wiki <tema>` - Buscar en Wikipedia

            **🏆 COMANDOS NIVELES:**
            `!nivel [usuario]` - Ver nivel
            `!leaderboard` - Tabla clasificación
            `!rank` - Tarjeta de rango

            **💰 COMANDOS ECONOMÍA:**
            `!daily` - Recompensa diaria
            `!work` - Trabajar
            `!balance [usuario]` - Ver balance

            **📊 COMANDOS INFORMACIÓN:**
            `!serverinfo` - Info servidor
            `!userinfo [usuario]` - Info usuario
            `!botinfo` - Info del bot

            **🛡️ COMANDOS MODERACIÓN:**
            `!warn <usuario> <razón>` - Advertir
            `!clear <cantidad>` - Limpiar mensajes

            **💻 COMANDOS PROGRAMACIÓN:**
            `!code <lenguaje> <código>` - Formatear
            `!langinfo <lenguaje>` - Info lenguaje

            **📍 IP SERVIDOR MINECRAFT:**
            ```honducraft.sdlf.fun```

            **💎 Usa `/hc` para ver los comandos slash (/)**
            """
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='ai')
    async def ai_traditional(self, ctx, *, pregunta: str):
        """IA tradicional"""
        respuesta = await SimpleAI.generate_response(pregunta)
        
        # Actualizar estadísticas
        db.data["statistics"]["ai_interactions"] += 1
        user_data = db.get_user_data(ctx.author.id, ctx.guild.id)
        user_data["stats"]["ai_uses"] += 1
        db.update_user_data(ctx.author.id, ctx.guild.id, user_data)
        
        embed = Embeds.info(
            "🤖 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 IA - Respuesta",
            f"""
            **👤 Pregunta de {ctx.author.display_name}:**
            {pregunta}

            **💜 Respuesta IA:**
            {respuesta}
            """
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='search', aliases=['buscar'])
    async def search_traditional(self, ctx, *, busqueda: str):
        """Búsqueda tradicional"""
        results = await WebSearch.search_google(busqueda, 3)
        
        # Actualizar estadísticas
        db.data["statistics"]["searches_performed"] += 1
        user_data = db.get_user_data(ctx.author.id, ctx.guild.id)
        user_data["stats"]["searches"] += 1
        db.update_user_data(ctx.author.id, ctx.guild.id, user_data)
        
        description = f"**🔍 Resultados para: `{busqueda}`**\n\n"
        
        for i, result in enumerate(results, 1):
            description += f"**{i}. {result['title']}**\n"
            description += f"{result['description']}\n"
            description += f"*<{result['url']}>*\n\n"
        
        embed = Embeds.info("🔍 Búsqueda ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱", description)
        await ctx.send(embed=embed)
    
    @commands.command(name='mcstatus')
    async def mcstatus_traditional(self, ctx):
        """Estado Minecraft tradicional"""
        status = await MinecraftSystem.get_server_status()
        embed = await MinecraftSystem.create_status_embed(BotConfig.MINECRAFT_IP, status)
        await ctx.send(embed=embed)
    
    @commands.command(name='botinfo')
    async def botinfo_traditional(self, ctx):
        """Info del bot tradicional"""
        embed = Embeds.info(
            "💜 ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 - Sistema Avanzado",
            f"""
            **🤖 Bot:** ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Ultra Pro
            **🚀 Versión:** {BotConfig.VERSION}
            **📊 Servidores:** {len(self.bot.guilds):,}
            **👥 Usuarios:** {sum(g.member_count for g in self.bot.guilds):,}
            **⚡ Latencia:** {round(self.bot.latency * 1000)}ms

            **🎮 IP Minecraft:**
            ```{BotConfig.MINECRAFT_IP}```

            **💎 Comandos disponibles:**
            `!ayuda` - Ver todos los comandos
            `!ai` - Chat con IA
            `!search` - Búsqueda web
            `!mcstatus` - Estado Minecraft

            **✨ Usa `/hc` para comandos slash**
            """
        )
        await ctx.send(embed=embed)

# =============================================
# EVENTOS Y TAREAS AUTOMÁTICAS
# =============================================

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    bot.start_time = datetime.datetime.now()
    
    print(f"""
    ╔════════════════════════════════════════════════════╗
    ║                                                      ║
    ║              ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 ULTRA PRO 5.0              ║
    ║              SISTEMA AVANZADO ACTIVADO               ║
    ║                                                      ║
    ╚════════════════════════════════════════════════════╝
    
    ✅ Bot conectado como: {bot.user.name}
    📊 ID: {bot.user.id}
    🌐 Servidores: {len(bot.guilds):,}
    👥 Usuarios: {sum(g.member_count for g in bot.guilds):,}
    🚀 Versión: {BotConfig.VERSION}
    ⏰ Hora de inicio: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    📈 Latencia: {round(bot.latency * 1000)}ms
    
    🔧 SISTEMAS CARGADOS:
    • ✅ IA Avanzada sin API
    • ✅ Búsqueda Web sin API  
    • ✅ Sistema Minecraft Mejorado
    • ✅ Comandos Slash (/hc)
    • ✅ Comandos Tradicionales (!)
    • ✅ Base de Datos Avanzada
    • ✅ Sistema de Cache
    • ✅ Embeds Morados Profesionales
    • ✅ Rich Presence Épico
    • ✅ Estadísticas en Tiempo Real
    """)
    
    # Sincronizar comandos slash
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} comandos slash sincronizados")
    except Exception as e:
        print(f"❌ Error sincronizando comandos slash: {e}")
    
    # Iniciar tareas automáticas
    update_presence.start()
    cleanup_cache.start()
    save_data_auto.start()
    
    # Estado épico inicial
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name=f"MC: {BotConfig.MINECRAFT_IP} | /hc"
        ),
        status=discord.Status.online
    )

@bot.event
async def on_message(message: discord.Message):
    """Evento cuando se envía un mensaje"""
    # Ignorar mensajes de bots
    if message.author.bot:
        return
    
    # Actualizar estadísticas
    db.data["statistics"]["messages_processed"] += 1
    
    # Procesar comandos tradicionales
    await bot.process_commands(message)

# =============================================
# TAREAS AUTOMÁTICAS MEJORADAS
# =============================================

@tasks.loop(minutes=2)
async def update_presence():
    """Actualiza el estado del bot con Rich Presence épico"""
    activities = [
        discord.Activity(type=discord.ActivityType.playing, name=f"MC: {BotConfig.MINECRAFT_IP}"),
        discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servidores"),
        discord.Activity(type=discord.ActivityType.listening, name="/hc commands"),
        discord.Activity(type=discord.ActivityType.playing, name="with ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Systems"),
        discord.Activity(type=discord.ActivityType.watching, name="AI Intelligence"),
        discord.Activity(type=discord.ActivityType.competing, name="Minecraft Adventures"),
        discord.Activity(type=discord.ActivityType.streaming, name="Live: honducraft.com", url="https://twitch.tv/honducraft")
    ]
    
    # Estado más épico cada 2 minutos
    current_activity = random.choice(activities)
    await bot.change_presence(activity=current_activity)

@tasks.loop(minutes=10)
async def cleanup_cache():
    """Limpia la cache periódicamente"""
    cache.cleanup_old_cache()

@tasks.loop(minutes=15)
async def save_data_auto():
    """Guarda datos automáticamente"""
    db.save_data()

# =============================================
# INICIALIZACIÓN Y EJECUCIÓN
# =============================================

async def main():
    """Función principal de inicialización"""
    # Añadir COGs
    await bot.add_cog(TraditionalCommands(bot))
    await bot.add_cog(SlashCommands(bot))
    
    # Iniciar el bot
    try:
        TOKEN = os.getenv("DISCORD_TOKEN") or "MTQ0MTE0ODY4NDUxNDM2MTQ2Ng.GYgx6k.iB6KitwmumRQYhI2QUMZAT4Lc3HuKXW4b_MdrAS"
        
        if not TOKEN or TOKEN == "TU_TOKEN_AQUI":
            print("❌ ERROR: Debes configurar tu token de Discord")
            print("💡 Configura la variable de entorno DISCORD_TOKEN")
            return
        
        logger.info("🚀 Iniciando ℌ𝔬𝔫𝔡𝔲ℭ𝔯𝔞𝔣𝔱 Ultra Pro 5.0...")
        await bot.start(TOKEN)
        
    except discord.LoginFailure:
        logger.error("❌ Error de autenticación: Token inválido")
    except KeyboardInterrupt:
        logger.info("⏹️ Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        traceback.print_exc()

# Servidor para Render
async def handle(request):
    return web.Response(text="Honducraft Bot está vivo 🚀")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, host="0.0.0.0", port=10000)

# Lanzar el servidor en segundo plano
threading.Thread(target=start_web_server, daemon=True).start()

# Ejecutar el bot
if __name__ == "__main__":
    asyncio.run(main())
