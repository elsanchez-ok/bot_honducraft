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
    VERSION = "4.1.0"
    DEVELOPER = "Honducraft Team"
    SUPPORT_SERVER = "https://discord.gg/honducraft"
    WEBSITE = "https://honducraft.com"
    
    # Colores profesionales
    COLORS = {
        "primary": 0x5865F2,
        "success": 0x57F287,
        "error": 0xED4245,
        "warning": 0xFEE75C,
        "info": 0x3498DB,
        "premium": 0x9B59B6,
        "dark": 0x2C2F33,
        "light": 0x99AAB5,
        "blurple": 0x5865F2,
        "green": 0x57F287,
        "yellow": 0xFEE75C,
        "red": 0xED4245
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

logger = logging.getLogger('HonducraftPro')

# Configuración de intents avanzada
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix=['!', 'hc ', 'HC ', 'honducraft ', 'Honducraft ', '.'],
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

cache = AdvancedCache()

# =============================================
# BASE DE DATOS MEGA AVANZADA (CORREGIDA)
# =============================================

class ProfessionalDatabase:
    """Sistema de base de datos profesional con todas las características"""
    
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
        """Carga datos con estructura mega avanzada"""
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
                "messages_deleted": 0,
                "users_joined": 0,
                "users_left": 0,
                "roles_assigned": 0,
                "reactions_added": 0,
                "level_ups": 0,
                "economy_transactions": 0,
                "music_plays": 0
            },
            "analytics": {
                "daily_commands": {},
                "popular_commands": {},
                "user_activity": {},
                "guild_growth": {}
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
            # Crear backup
            self.create_backup("auto_save")
            
            # Actualizar metadata
            self.data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
            self.data["metadata"]["data_size"] = len(str(self.data))
            
            # Guardar con compresión
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            
            # Limpiar backups antiguos
            self.clean_old_backups()
            
            logger.info("Datos guardados exitosamente")
            
        except Exception as e:
            logger.error(f"Error guardando datos: {e}")
            self.emergency_save()
    
    def create_backup(self, reason: str = "manual"):
        """Crea backup con compresión"""
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
        """Limpia backups antiguos - MÉTODO AÑADIDO"""
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
        """Guardado de emergencia - MÉTODO AÑADIDO"""
        try:
            temp_file = f"{self.file_path}.emergency"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f)
            logger.info("✅ Guardado de emergencia exitoso")
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
        """Configuración por defecto para servidores nuevos"""
        return {
            "prefix": "!",
            "language": "es",
            "modules": {
                "moderation": True,
                "welcome": True,
                "levels": True,
                "economy": True,
                "music": False,
                "tickets": True,
                "logging": True,
                "automod": True,
                "fun": True,
                "utility": True,
                "minecraft": True,
                "programming": True
            },
            "channels": {
                "welcome": None,
                "goodbye": None,
                "logs": None,
                "mod_logs": None,
                "level_up": None,
                "suggestions": None,
                "tickets_category": None,
                "minecraft": None,
                "programming": None
            },
            "roles": {
                "muted": None,
                "auto_roles": [],
                "bot_roles": [],
                "level_roles": {},
                "staff_roles": [],
                "admin_roles": [],
                "programmer_roles": [],
                "minecraft_roles": []
            },
            "automod": {
                "enabled": True,
                "anti_spam": True,
                "anti_raid": True,
                "anti_invites": True,
                "anti_links": False,
                "max_warns": 3,
                "filter_words": [],
                "whitelisted_links": [],
                "whitelisted_roles": [],
                "ignored_channels": []
            },
            "leveling": {
                "enabled": True,
                "announce_level_up": True,
                "xp_per_message": 15,
                "xp_cooldown": 60,
                "message_multiplier": 1.0,
                "role_multipliers": {},
                "channel_multipliers": {}
            },
            "economy": {
                "enabled": True,
                "currency_name": "coins",
                "currency_symbol": "🪙",
                "daily_amount": 100,
                "work_amount_min": 50,
                "work_amount_max": 150,
                "starting_balance": 100
            },
            "tickets": {
                "enabled": True,
                "support_roles": [],
                "categories": {
                    "support": {"emoji": "💼", "name": "Soporte"},
                    "report": {"emoji": "🚨", "name": "Reporte"},
                    "suggestion": {"emoji": "💡", "name": "Sugerencia"}
                }
            },
            "welcome": {
                "enabled": True,
                "message": "¡Bienvenido {user.mention} a {server.name}!",
                "goodbye_message": "¡{user.name} ha dejado el servidor!",
                "embed_color": BotConfig.COLORS["primary"],
                "send_dm": True,
                "dm_message": "¡Gracias por unirte a {server.name}!"
            },
            "logging": {
                "enabled": True,
                "events": [
                    "message_delete", "message_edit", "member_join", 
                    "member_leave", "role_changes", "channel_updates",
                    "member_bans", "member_unbans", "voice_changes"
                ]
            },
            "minecraft": {
                "server_ip": None,
                "server_port": 25565,
                "status_channel": None,
                "auto_status": False
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
        """Datos por defecto para usuarios nuevos"""
        return {
            "leveling": {
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "messages": 0,
                "voice_time": 0,
                "last_message": None,
                "rank_card": "default"
            },
            "economy": {
                "wallet": 100,
                "bank": 0,
                "daily_streak": 0,
                "last_daily": None,
                "last_work": None,
                "inventory": {},
                "job": None
            },
            "moderation": {
                "warns": [],
                "mutes": 0,
                "kicks": 0,
                "bans": 0
            },
            "preferences": {
                "timezone": "UTC",
                "notifications": True,
                "privacy_mode": False
            },
            "stats": {
                "commands_used": 0,
                "messages_sent": 0,
                "reactions_added": 0,
                "joined_at": datetime.datetime.now().isoformat()
            },
            "minecraft": {
                "minecraft_username": None,
                "linked_at": None,
                "server_stats": {}
            },
            "programming": {
                "languages": [],
                "projects": [],
                "experience_level": "beginner"
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
# SISTEMA DE EMBEDS PROFESIONALES
# =============================================

class ProfessionalEmbeds:
    """Sistema de embeds estilo MEE6/Dyno"""
    
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
        """Crea un embed profesional"""
        
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
                if value:  # Solo añadir field si tiene valor
                    embed.add_field(name=name, value=value, inline=inline)
        
        footer_text = footer or "Honducraft Pro • Sistema Avanzado"
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
            title=f"ℹ️ {title}",
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
# SISTEMA DE NIVELES Y ECONOMÍA MEGA AVANZADO
# =============================================

class AdvancedLeveling:
    """Sistema de niveles profesional como MEE6"""
    
    @staticmethod
    def calculate_level(xp: int) -> int:
        """Calcula nivel basado en XP (fórmula MEE6-like)"""
        return max(1, int((xp / 100) ** 0.5))
    
    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """Calcula XP necesario para un nivel"""
        return int(100 * (level ** 2))
    
    @staticmethod
    def create_progress_bar(current: int, maximum: int, length: int = 20) -> str:
        """Crea una barra de progreso"""
        progress = min(current / maximum, 1.0)
        filled = int(progress * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"`[{bar}]` {progress:.1%}"
    
    @staticmethod
    async def add_xp(user: discord.Member, message: discord.Message):
        """Añade XP por mensaje"""
        guild_config = db.get_guild_config(user.guild.id)
        
        if not guild_config["modules"]["levels"]:
            return
        
        # Verificar cooldown
        user_data = db.get_user_data(user.id, user.guild.id)
        last_message = user_data["leveling"]["last_message"]
        
        if last_message:
            last_msg_time = datetime.datetime.fromisoformat(last_message)
            cooldown = guild_config["leveling"]["xp_cooldown"]
            if (datetime.datetime.now() - last_msg_time).seconds < cooldown:
                return
        
        # Calcular XP ganado
        base_xp = guild_config["leveling"]["xp_per_message"]
        multiplier = guild_config["leveling"]["message_multiplier"]
        
        # Multiplicadores por rol
        for role in user.roles:
            role_multiplier = guild_config["leveling"]["role_multipliers"].get(str(role.id), 1.0)
            multiplier *= role_multiplier
        
        # Multiplicador por canal
        channel_multiplier = guild_config["leveling"]["channel_multipliers"].get(str(message.channel.id), 1.0)
        multiplier *= channel_multiplier
        
        xp_earned = int(base_xp * multiplier)
        
        # Actualizar datos
        user_data["leveling"]["xp"] += xp_earned
        user_data["leveling"]["total_xp"] += xp_earned
        user_data["leveling"]["messages"] += 1
        user_data["leveling"]["last_message"] = datetime.datetime.now().isoformat()
        
        # Verificar subida de nivel
        old_level = user_data["leveling"]["level"]
        new_level = AdvancedLeveling.calculate_level(user_data["leveling"]["total_xp"])
        
        if new_level > old_level:
            user_data["leveling"]["level"] = new_level
            await AdvancedLeveling.handle_level_up(user, old_level, new_level, user_data)
        
        db.update_user_data(user.id, user.guild.id, user_data)
    
    @staticmethod
    async def handle_level_up(user: discord.Member, old_level: int, new_level: int, user_data: dict):
        """Maneja subidas de nivel"""
        guild_config = db.get_guild_config(user.guild.id)
        
        # Asignar roles de nivel
        level_roles = guild_config["roles"]["level_roles"]
        for level, role_id in level_roles.items():
            if new_level >= int(level):
                role = user.guild.get_role(role_id)
                if role and role not in user.roles:
                    try:
                        await user.add_roles(role, reason=f"Level {new_level} role")
                    except:
                        pass
        
        # Anunciar level up
        if guild_config["leveling"]["announce_level_up"]:
            channel_id = guild_config["channels"]["level_up"]
            channel = user.guild.get_channel(channel_id) if channel_id else None
            
            if not channel:
                channel = user.guild.system_channel
            
            if channel:
                embed = Embeds.success(
                    "🎉 ¡Subida de Nivel!",
                    f"""
                    **¡Felicidades {user.mention}!** 🎊
                    
                    **Has subido al nivel {new_level}!** 🏆
                    **• Nivel anterior:** {old_level}
                    **• XP total:** {user_data['leveling']['total_xp']:,}
                    **• Mensajes:** {user_data['leveling']['messages']:,}
                    
                    *¡Sigue activo para ganar más niveles!*
                    """
                )
                embed.set_thumbnail(url=user.display_avatar.url)
                await channel.send(embed=embed)
        
        # Actualizar estadísticas
        db.data["statistics"]["level_ups"] += 1
        db.save_data()

class AdvancedEconomy:
    """Sistema de economía avanzado"""
    
    @staticmethod
    async def daily_reward(user: discord.Member):
        """Recompensa diaria"""
        guild_config = db.get_guild_config(user.guild.id)
        
        if not guild_config["modules"]["economy"]:
            return None
        
        user_data = db.get_user_data(user.id, user.guild.id)
        now = datetime.datetime.now()
        
        # Verificar si ya reclamó hoy
        last_daily = user_data["economy"]["last_daily"]
        if last_daily:
            last_daily_date = datetime.datetime.fromisoformat(last_daily)
            if last_daily_date.date() == now.date():
                return False  # Ya reclamó hoy
        
        # Calcular recompensa
        base_amount = guild_config["economy"]["daily_amount"]
        streak = user_data["economy"]["daily_streak"]
        
        # Bono por racha
        streak_bonus = min(streak * 10, 100)  # Máximo 100 de bono
        total_amount = base_amount + streak_bonus
        
        # Actualizar datos
        user_data["economy"]["wallet"] += total_amount
        user_data["economy"]["daily_streak"] += 1
        user_data["economy"]["last_daily"] = now.isoformat()
        
        db.update_user_data(user.id, user.guild.id, user_data)
        
        return {
            "amount": total_amount,
            "streak": user_data["economy"]["daily_streak"],
            "bonus": streak_bonus
        }
    
    @staticmethod
    async def work(user: discord.Member):
        """Sistema de trabajo"""
        guild_config = db.get_guild_config(user.guild.id)
        
        if not guild_config["modules"]["economy"]:
            return None
        
        user_data = db.get_user_data(user.id, user.guild.id)
        now = datetime.datetime.now()
        
        # Verificar cooldown (6 horas)
        last_work = user_data["economy"]["last_work"]
        if last_work:
            last_work_time = datetime.datetime.fromisoformat(last_work)
            if (now - last_work_time).seconds < 21600:  # 6 horas
                time_left = 21600 - (now - last_work_time).seconds
                return {"cooldown": time_left}
        
        # Calcular ganancias
        min_amount = guild_config["economy"]["work_amount_min"]
        max_amount = guild_config["economy"]["work_amount_max"]
        earnings = random.randint(min_amount, max_amount)
        
        # Bono por trabajo
        job = user_data["economy"]["job"]
        if job:
            job_bonus = {
                "programmer": 1.2,
                "designer": 1.1,
                "moderator": 1.15
            }.get(job, 1.0)
            earnings = int(earnings * job_bonus)
        
        # Actualizar datos
        user_data["economy"]["wallet"] += earnings
        user_data["economy"]["last_work"] = now.isoformat()
        
        db.update_user_data(user.id, user.guild.id, user_data)
        
        return {
            "amount": earnings,
            "job": job
        }

# =============================================
# SISTEMA DE MINECRAFT
# =============================================

class MinecraftSystem:
    """Sistema de integración con Minecraft"""
    
    @staticmethod
    async def get_server_status(ip: str, port: int = 25565):
        """Obtiene el estado de un servidor de Minecraft"""
        try:
            # Simulación de estado (en una implementación real usarías mcstatus)
            status = {
                "online": random.choice([True, False]),
                "players": random.randint(0, 50),
                "max_players": 100,
                "version": "1.20.1",
                "description": "§aHonducraft Minecraft Server",
                "latency": random.randint(10, 100)
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
                f"🟢 {server_ip} - En Línea",
                f"""
                **📊 Estado del Servidor:**
                **• Jugadores:** {status['players']}/{status['max_players']}
                **• Versión:** {status['version']}
                **• Latencia:** {status['latency']}ms
                **• Descripción:** {status['description']}
                
                **¡El servidor está funcionando correctamente!**
                """
            )
        else:
            embed = Embeds.error(
                f"🔴 {server_ip} - Fuera de Línea",
                "El servidor de Minecraft no está disponible en este momento."
            )
        
        return embed

# =============================================
# SISTEMA DE PROGRAMACIÓN
# =============================================

class ProgrammingSystem:
    """Sistema de utilidades para programadores"""
    
    @staticmethod
    def format_code(code: str, language: str = "python") -> str:
        """Formatea código para Discord"""
        return f"```{language}\n{code}\n```"
    
    @staticmethod
    async def execute_python_code(code: str):
        """Ejecuta código Python de forma segura (simulado)"""
        # En una implementación real usarías un sandbox
        return {
            "output": "Ejecución simulada - En producción usar sandbox",
            "success": True,
            "execution_time": random.randint(1, 100)
        }
    
    @staticmethod
    def get_language_info(language: str):
        """Obtiene información sobre un lenguaje de programación"""
        languages = {
            "python": {
                "name": "Python",
                "year": 1991,
                "creator": "Guido van Rossum",
                "paradigm": "Multi-paradigma",
                "description": "Lenguaje de programación interpretado, multiparadigma y de alto nivel."
            },
            "javascript": {
                "name": "JavaScript",
                "year": 1995,
                "creator": "Brendan Eich",
                "paradigm": "Multi-paradigma",
                "description": "Lenguaje de programación interpretado, dialecto del estándar ECMAScript."
            },
            "java": {
                "name": "Java",
                "year": 1995,
                "creator": "James Gosling",
                "paradigm": "Orientado a objetos",
                "description": "Lenguaje de programación de propósito general, concurrente y orientado a objetos."
            }
        }
        
        return languages.get(language.lower())

# =============================================
# COMANDOS TRADICIONALES (PREFIJO)
# =============================================

class TraditionalCommands(commands.Cog):
    """Comandos tradicionales con prefijo que funcionan inmediatamente"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ayuda', aliases=['help', 'comandos'])
    async def ayuda(self, ctx):
        """Comando de ayuda tradicional"""
        embed = Embeds.info(
            "🤖 Honducraft Pro - Comandos Disponibles",
            """
            **¡Usa `!` antes de cada comando!**
            
            **📊 INFORMACIÓN:**
            `!ayuda` - Muestra este mensaje
            `!botinfo` - Información del bot
            `!serverinfo` - Información del servidor
            `!userinfo` - Información de un usuario
            
            **🏆 SISTEMA DE NIVELES:**
            `!nivel` - Ver tu nivel
            `!leaderboard` - Tabla de clasificación
            
            **💰 ECONOMÍA:**
            `!daily` - Reclamar recompensa diaria
            `!work` - Trabajar para ganar dinero
            `!balance` - Ver tu balance
            
            **🎮 DIVERSIÓN:**
            `!meme` - Generar meme aleatorio
            `!8ball` - Pregunta a la bola mágica
            
            **🔧 UTILIDAD:**
            `!ping` - Ver latencia del bot
            `!avatar` - Ver avatar de usuario
            
            **🛡️ MODERACIÓN:**
            `!warn` - Advertir a un usuario
            `!clear` - Limpiar mensajes
            
            **🎮 MINECRAFT:**
            `!mcstatus` - Estado servidor Minecraft
            `!linkmc` - Vincular cuenta Minecraft
            
            **💻 PROGRAMACIÓN:**
            `!code` - Formatear código
            `!langinfo` - Info lenguaje programación
            
            *Los comandos slash (/) pueden tardar hasta 1 hora en aparecer.*
            """
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='botinfo', aliases=['info', 'bot'])
    async def botinfo(self, ctx):
        """Información del bot"""
        embed = Embeds.info(
            "🤖 Honducraft Pro - Información",
            f"""
            **📊 ESTADÍSTICAS:**
            **• Servidores:** {len(self.bot.guilds):,}
            **• Usuarios:** {sum(g.member_count for g in self.bot.guilds):,}
            **• Latencia:** {round(self.bot.latency * 1000)}ms
            **• Uptime:** {self.get_uptime()}
            
            **🔧 INFORMACIÓN:**
            **• Versión:** {BotConfig.VERSION}
            **• Desarrollador:** {BotConfig.DEVELOPER}
            **• Soporte:** {BotConfig.SUPPORT_SERVER}
            
            **📈 ESTADÍSTICAS GLOBALES:**
            **• Mensajes procesados:** {db.data['statistics']['messages_processed']:,}
            **• Comandos usados:** {db.data['statistics']['commands_used']:,}
            **• Niveles subidos:** {db.data['statistics']['level_ups']:,}
            """
        )
        await ctx.send(embed=embed)
    
    def get_uptime(self):
        """Obtiene el tiempo de actividad del bot"""
        delta = datetime.datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    @commands.command(name='serverinfo', aliases=['server', 'servidor'])
    async def serverinfo(self, ctx):
        """Información del servidor"""
        guild = ctx.guild
        
        embed = Embeds.info(
            f"🌐 {guild.name} - Información",
            f"""
            **📊 ESTADÍSTICAS:**
            **• Miembros:** {guild.member_count:,}
            **• Canales:** {len(guild.channels):,}
            **• Roles:** {len(guild.roles):,}
            **• Emojis:** {len(guild.emojis):,}
            **• Boosts:** {guild.premium_subscription_count}
            
            **📅 INFORMACIÓN:**
            **• Creado:** <t:{int(guild.created_at.timestamp())}:R>
            **• Dueño:** {guild.owner.mention}
            **• ID:** `{guild.id}`
            """
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', aliases=['user', 'usuario'])
    async def userinfo(self, ctx, usuario: discord.Member = None):
        """Información de usuario"""
        usuario = usuario or ctx.author
        
        user_data = db.get_user_data(usuario.id, ctx.guild.id)
        
        embed = Embeds.info(
            f"👤 {usuario.display_name} - Información",
            f"""
            **📊 INFORMACIÓN GENERAL:**
            **• Nombre:** {usuario.display_name}
            **• ID:** `{usuario.id}`
            **• Cuenta creada:** <t:{int(usuario.created_at.timestamp())}:R>
            **• Se unió:** <t:{int(usuario.joined_at.timestamp())}:R>
            **• Roles:** {len(usuario.roles) - 1}
            
            **🏆 SISTEMA DE NIVELES:**
            **• Nivel:** {user_data['leveling']['level']}
            **• XP:** {user_data['leveling']['xp']:,}
            **• XP Total:** {user_data['leveling']['total_xp']:,}
            **• Mensajes:** {user_data['leveling']['messages']:,}
            
            **💰 ECONOMÍA:**
            **• Balance:** {user_data['economy']['wallet']:,} 🪙
            **• Racha diaria:** {user_data['economy']['daily_streak']} días
            """
        )
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='nivel', aliases=['level', 'rank'])
    async def nivel(self, ctx, usuario: discord.Member = None):
        """Ver nivel de usuario"""
        usuario = usuario or ctx.author
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["levels"]:
            await ctx.send(embed=Embeds.error("El sistema de niveles está desactivado."))
            return
        
        user_data = db.get_user_data(usuario.id, ctx.guild.id)
        level_data = user_data["leveling"]
        
        # Calcular ranking
        all_users = []
        for user_key, data in db.data["users"].items():
            if user_key.endswith(f"_{ctx.guild.id}"):
                all_users.append((user_key, data["leveling"]["total_xp"]))
        
        all_users.sort(key=lambda x: x[1], reverse=True)
        rank = next((i + 1 for i, (key, _) in enumerate(all_users) if key == f"{ctx.guild.id}_{usuario.id}"), 1)
        
        # Calcular XP necesario
        xp_needed = AdvancedLeveling.calculate_xp_for_level(level_data['level'] + 1)
        
        embed = Embeds.premium(
            f"🏆 Nivel de {usuario.display_name}",
            f"""
            **Nivel:** `{level_data['level']}`
            **XP:** `{level_data['xp']:,}` / `{xp_needed:,}`
            **XP Total:** `{level_data['total_xp']:,}`
            **Mensajes:** `{level_data['messages']:,}`
            **Ranking:** `#{rank}` de `{len(all_users)}`
            
            **Progreso:**
            {AdvancedLeveling.create_progress_bar(level_data['xp'], xp_needed)}
            """
        )
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['top', 'lb'])
    async def leaderboard(self, ctx):
        """Leaderboard de niveles"""
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["levels"]:
            await ctx.send(embed=Embeds.error("El sistema de niveles está desactivado."))
            return
        
        # Obtener top 10 usuarios
        users = []
        for user_key, data in db.data["users"].items():
            if user_key.endswith(f"_{ctx.guild.id}"):
                user_id = int(user_key.split('_')[1])
                user = ctx.guild.get_member(user_id)
                if user:
                    users.append((user, data["leveling"]))
        
        users.sort(key=lambda x: x[1]["total_xp"], reverse=True)
        top_10 = users[:10]
        
        description = ""
        for i, (user, data) in enumerate(top_10):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"`{i+1}.`"
            description += f"{medal} **{user.display_name}** - Nivel {data['level']} | {data['total_xp']:,} XP\n"
        
        embed = Embeds.premium(
            "🏅 Leaderboard de Niveles",
            description or "No hay datos suficientes para mostrar el leaderboard."
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='daily', aliases=['diario'])
    async def daily(self, ctx):
        """Recompensa diaria"""
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["economy"]:
            await ctx.send(embed=Embeds.error("El sistema económico está desactivado."))
            return
        
        result = await AdvancedEconomy.daily_reward(ctx.author)
        
        if result is None:
            await ctx.send(embed=Embeds.error("Error al procesar la recompensa diaria."))
        elif result is False:
            await ctx.send(embed=Embeds.warning("Ya reclamaste tu recompensa diaria hoy."))
        else:
            currency_symbol = guild_config["economy"]["currency_symbol"]
            embed = Embeds.success(
                "🎁 Recompensa Diaria Reclamada",
                f"""
                **¡Recompensa diaria reclamada!** 🎊
                
                **Monedas ganadas:** {currency_symbol} **{result['amount']:,}**
                **Racha actual:** {result['streak']} días
                **Bono por racha:** {currency_symbol} {result['bonus']}
                
                *Vuelve mañana para seguir tu racha.*
                """
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='work', aliases=['trabajar'])
    async def work(self, ctx):
        """Trabajar para ganar dinero"""
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["economy"]:
            await ctx.send(embed=Embeds.error("El sistema económico está desactivado."))
            return
        
        result = await AdvancedEconomy.work(ctx.author)
        
        if result is None:
            await ctx.send(embed=Embeds.error("Error al procesar el trabajo."))
        elif "cooldown" in result:
            hours = result["cooldown"] // 3600
            minutes = (result["cooldown"] % 3600) // 60
            await ctx.send(embed=Embeds.warning(f"⏰ Puedes trabajar nuevamente en **{hours}h {minutes}m**."))
        else:
            currency_symbol = guild_config["economy"]["currency_symbol"]
            job_info = f" (**{result['job']}**)" if result['job'] else ""
            embed = Embeds.success(
                "💼 Trabajo Completado",
                f"""
                **¡Trabajo completado!** {job_info}
                
                **Ganancias:** {currency_symbol} **{result['amount']:,}**
                
                *Puedes trabajar nuevamente en 6 horas.*
                """
            )
            await ctx.send(embed=embed)
    
    @commands.command(name='balance', aliases=['bal', 'dinero'])
    async def balance(self, ctx, usuario: discord.Member = None):
        """Ver balance"""
        usuario = usuario or ctx.author
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["economy"]:
            await ctx.send(embed=Embeds.error("El sistema económico está desactivado."))
            return
        
        user_data = db.get_user_data(usuario.id, ctx.guild.id)
        economy_data = user_data["economy"]
        currency_symbol = guild_config["economy"]["currency_symbol"]
        
        embed = Embeds.info(
            f"💰 Balance de {usuario.display_name}",
            f"""
            **💼 Cartera:** {currency_symbol} **{economy_data['wallet']:,}**
            **🏦 Banco:** {currency_symbol} **{economy_data['bank']:,}**
            **💰 Total:** {currency_symbol} **{economy_data['wallet'] + economy_data['bank']:,}**
            
            **📊 Estadísticas:**
            **📅 Racha diaria:** {economy_data['daily_streak']} días
            **💼 Trabajo:** {economy_data['job'] or 'Desempleado'}
            """
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Ver latencia del bot"""
        embed = Embeds.info(
            "🏓 Pong!",
            f"**Latencia:** {round(self.bot.latency * 1000)}ms"
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', aliases=['av', 'pfp'])
    async def avatar(self, ctx, usuario: discord.Member = None):
        """Ver avatar de usuario"""
        usuario = usuario or ctx.author
        
        embed = Embeds.info(
            f"🖼️ Avatar de {usuario.display_name}",
            f"[Descargar avatar]({usuario.display_avatar.url})"
        )
        embed.set_image(url=usuario.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='meme')
    async def meme(self, ctx):
        """Generar meme aleatorio"""
        memes = [
            "https://i.imgur.com/8Q7Y9qJ.png",
            "https://i.imgur.com/3Q7Y9qJ.png",
            "https://i.imgur.com/5Q7Y9qJ.png"
        ]
        embed = Embeds.info("😂 Meme Aleatorio", "¡Disfruta de este meme!")
        embed.set_image(url=random.choice(memes))
        await ctx.send(embed=embed)
    
    @commands.command(name='8ball', aliases=['bola'])
    async def eight_ball(self, ctx, *, pregunta: str):
        """Bola mágica 8-ball"""
        responses = [
            "Sí, definitivamente.", "Es cierto.", "Sin duda.",
            "Sí, definitivamente.", "Puedes confiar en ello.",
            "Como yo lo veo, sí.", "Lo más probable.", "Perspectiva buena.",
            "Sí.", "Las señales apuntan a que sí.",
            "Respuesta confusa, intenta otra vez.", "Pregunta de nuevo más tarde.",
            "Mejor no te lo digo ahora.", "No puedo predecirlo ahora.",
            "Concéntrate y pregunta otra vez.",
            "No cuentes con ello.", "Mi respuesta es no.",
            "Mis fuentes dicen que no.", "Perspectiva no tan buena.", "Muy dudoso."
        ]
        
        embed = Embeds.info(
            "🎱 Bola Mágica 8-Ball",
            f"""
            **Pregunta:** {pregunta}
            **Respuesta:** {random.choice(responses)}
            """
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='mcstatus', aliases=['minecraft'])
    async def mcstatus(self, ctx, ip: str = None):
        """Estado del servidor de Minecraft"""
        guild_config = db.get_guild_config(ctx.guild.id)
        
        if not guild_config["modules"]["minecraft"]:
            await ctx.send(embed=Embeds.error("El sistema de Minecraft está desactivado."))
            return
        
        server_ip = ip or guild_config["minecraft"]["server_ip"]
        if not server_ip:
            await ctx.send(embed=Embeds.error("No hay servidor de Minecraft configurado. Usa `!mcstatus <ip>`"))
            return
        
        # Mostrar mensaje de carga
        loading_msg = await ctx.send("🔄 Obteniendo estado del servidor...")
        
        # Obtener estado
        status = await MinecraftSystem.get_server_status(server_ip)
        embed = await MinecraftSystem.create_status_embed(server_ip, status)
        
        await loading_msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name='linkmc')
    async def linkmc(self, ctx, username: str):
        """Vincular cuenta de Minecraft"""
        user_data = db.get_user_data(ctx.author.id, ctx.guild.id)
        user_data["minecraft"]["minecraft_username"] = username
        user_data["minecraft"]["linked_at"] = datetime.datetime.now().isoformat()
        
        db.update_user_data(ctx.author.id, ctx.guild.id, user_data)
        
        embed = Embeds.success(
            "✅ Cuenta Vinculada",
            f"""
            **¡Cuenta de Minecraft vinculada exitosamente!**
            
            **Usuario:** {username}
            **Vinculado:** <t:{int(datetime.datetime.now().timestamp())}:R>
            
            *Tu cuenta de Minecraft ha sido vinculada a tu perfil de Discord.*
            """
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='code')
    async def code(self, ctx, lenguaje: str, *, codigo: str):
        """Formatear código"""
        formatted_code = ProgrammingSystem.format_code(codigo, lenguaje)
        
        if len(formatted_code) > 2000:
            await ctx.send(embed=Embeds.error("El código es demasiado largo para enviar."))
            return
        
        embed = Embeds.info(
            f"💻 Código {lenguaje.upper()}",
            formatted_code
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='langinfo')
    async def langinfo(self, ctx, lenguaje: str):
        """Información sobre lenguaje de programación"""
        info = ProgrammingSystem.get_language_info(lenguaje)
        
        if not info:
            await ctx.send(embed=Embeds.error(f"No se encontró información sobre `{lenguaje}`"))
            return
        
        embed = Embeds.info(
            f"📚 {info['name']} - Información",
            f"""
            **📅 Año de creación:** {info['year']}
            **👨‍💻 Creador:** {info['creator']}
            **🔧 Paradigma:** {info['paradigm']}
            **📖 Descripción:** {info['description']}
            """
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='clear', aliases=['limpiar'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, cantidad: int = 10):
        """Limpiar mensajes"""
        if cantidad > 100:
            await ctx.send(embed=Embeds.error("No puedes eliminar más de 100 mensajes a la vez."))
            return
        
        deleted = await ctx.channel.purge(limit=cantidad + 1)  # +1 para incluir el comando
        
        embed = Embeds.success(
            "🗑️ Mensajes Eliminados",
            f"Se han eliminado **{len(deleted) - 1}** mensajes."
        )
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()
    
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, usuario: discord.Member, *, razon: str = "No especificada"):
        """Advertir a un usuario"""
        user_data = db.get_user_data(usuario.id, ctx.guild.id)
        
        warn_data = {
            "moderator": ctx.author.id,
            "reason": razon,
            "timestamp": datetime.datetime.now().isoformat(),
            "warn_id": len(user_data["moderation"]["warns"]) + 1
        }
        
        user_data["moderation"]["warns"].append(warn_data)
        db.update_user_data(usuario.id, ctx.guild.id, user_data)
        
        embed = Embeds.warning(
            "⚠️ Usuario Advertido",
            f"""
            **Usuario:** {usuario.mention}
            **Moderador:** {ctx.author.mention}
            **Razón:** {razon}
            **Advertencia:** #{len(user_data["moderation"]["warns"])}
            
            *El usuario ha sido advertido correctamente.*
            """
        )
        await ctx.send(embed=embed)

# =============================================
# COMANDOS SLASH (/) - INTERACCIÓN MODERNA
# =============================================

class SlashCommands(commands.Cog):
    """Comandos slash modernos y profesionales"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Muestra todos los comandos disponibles")
    async def help_slash(self, interaction: discord.Interaction):
        """Comando de ayuda slash"""
        embed = Embeds.info(
            "🤖 Honducraft Pro - Comandos Slash",
            """
            **¡Usa `/` para acceder a estos comandos!**
            
            **📊 INFORMACIÓN:**
            `/help` - Muestra este mensaje
            `/botinfo` - Información del bot
            `/serverinfo` - Información del servidor
            `/userinfo` - Información de un usuario
            
            **🏆 SISTEMA DE NIVELES:**
            `/level` - Ver tu nivel
            `/leaderboard` - Tabla de clasificación
            
            **💰 ECONOMÍA:**
            `/daily` - Reclamar recompensa diaria
            `/work` - Trabajar para ganar dinero
            `/balance` - Ver tu balance
            
            **🎮 DIVERSIÓN:**
            `/meme` - Generar meme aleatorio
            `/8ball` - Pregunta a la bola mágica
            
            **🔧 UTILIDAD:**
            `/ping` - Ver latencia del bot
            `/avatar` - Ver avatar de usuario
            
            **🎮 MINECRAFT:**
            `/mcstatus` - Estado servidor Minecraft
            `/linkmc` - Vincular cuenta Minecraft
            
            **💻 PROGRAMACIÓN:**
            `/code` - Formatear código
            `/langinfo` - Info lenguaje programación
            """
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="botinfo", description="Muestra información del bot")
    async def botinfo_slash(self, interaction: discord.Interaction):
        """Información del bot (slash)"""
        embed = Embeds.info(
            "🤖 Honducraft Pro - Información",
            f"""
            **📊 ESTADÍSTICAS:**
            **• Servidores:** {len(self.bot.guilds):,}
            **• Usuarios:** {sum(g.member_count for g in self.bot.guilds):,}
            **• Latencia:** {round(self.bot.latency * 1000)}ms
            **• Uptime:** {self.get_uptime()}
            
            **🔧 INFORMACIÓN:**
            **• Versión:** {BotConfig.VERSION}
            **• Desarrollador:** {BotConfig.DEVELOPER}
            **• Soporte:** {BotConfig.SUPPORT_SERVER}
            """
        )
        await interaction.response.send_message(embed=embed)
    
    def get_uptime(self):
        """Obtiene el tiempo de actividad del bot"""
        delta = datetime.datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    @app_commands.command(name="serverinfo", description="Muestra información del servidor")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        """Información del servidor (slash)"""
        guild = interaction.guild
        
        embed = Embeds.info(
            f"🌐 {guild.name} - Información",
            f"""
            **📊 ESTADÍSTICAS:**
            **• Miembros:** {guild.member_count:,}
            **• Canales:** {len(guild.channels):,}
            **• Roles:** {len(guild.roles):,}
            **• Emojis:** {len(guild.emojis):,}
            **• Boosts:** {guild.premium_subscription_count}
            
            **📅 INFORMACIÓN:**
            **• Creado:** <t:{int(guild.created_at.timestamp())}:R>
            **• Dueño:** {guild.owner.mention}
            """
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo", description="Muestra información de un usuario")
    @app_commands.describe(usuario="El usuario del que quieres información")
    async def userinfo_slash(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Información de usuario (slash)"""
        usuario = usuario or interaction.user
        
        user_data = db.get_user_data(usuario.id, interaction.guild.id)
        
        embed = Embeds.info(
            f"👤 {usuario.display_name} - Información",
            f"""
            **📊 INFORMACIÓN GENERAL:**
            **• Nombre:** {usuario.display_name}
            **• ID:** `{usuario.id}`
            **• Cuenta creada:** <t:{int(usuario.created_at.timestamp())}:R>
            **• Se unió:** <t:{int(usuario.joined_at.timestamp())}:R>
            **• Roles:** {len(usuario.roles) - 1}
            
            **🏆 SISTEMA DE NIVELES:**
            **• Nivel:** {user_data['leveling']['level']}
            **• XP:** {user_data['leveling']['xp']:,}
            **• XP Total:** {user_data['leveling']['total_xp']:,}
            """
        )
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="level", description="Muestra tu nivel y progreso")
    @app_commands.describe(usuario="El usuario del que quieres ver el nivel")
    async def level_slash(self, interaction: discord.Interaction, usuario: discord.Member = None):
        """Ver nivel (slash)"""
        usuario = usuario or interaction.user
        guild_config = db.get_guild_config(interaction.guild.id)
        
        if not guild_config["modules"]["levels"]:
            await interaction.response.send_message(embed=Embeds.error("El sistema de niveles está desactivado."))
            return
        
        user_data = db.get_user_data(usuario.id, interaction.guild.id)
        level_data = user_data["leveling"]
        
        # Calcular XP necesario
        xp_needed = AdvancedLeveling.calculate_xp_for_level(level_data['level'] + 1)
        
        embed = Embeds.premium(
            f"🏆 Nivel de {usuario.display_name}",
            f"""
            **Nivel:** `{level_data['level']}`
            **XP:** `{level_data['xp']:,}` / `{xp_needed:,}`
            **XP Total:** `{level_data['total_xp']:,}`
            **Mensajes:** `{level_data['messages']:,}`
            
            **Progreso:**
            {AdvancedLeveling.create_progress_bar(level_data['xp'], xp_needed)}
            """
        )
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="daily", description="Reclama tu recompensa diaria")
    async def daily_slash(self, interaction: discord.Interaction):
        """Recompensa diaria (slash)"""
        guild_config = db.get_guild_config(interaction.guild.id)
        
        if not guild_config["modules"]["economy"]:
            await interaction.response.send_message(embed=Embeds.error("El sistema económico está desactivado."))
            return
        
        result = await AdvancedEconomy.daily_reward(interaction.user)
        
        if result is None:
            await interaction.response.send_message(embed=Embeds.error("Error al procesar la recompensa diaria."))
        elif result is False:
            await interaction.response.send_message(embed=Embeds.warning("Ya reclamaste tu recompensa diaria hoy."))
        else:
            currency_symbol = guild_config["economy"]["currency_symbol"]
            embed = Embeds.success(
                "🎁 Recompensa Diaria Reclamada",
                f"""
                **¡Recompensa diaria reclamada!** 🎊
                
                **Monedas ganadas:** {currency_symbol} **{result['amount']:,}**
                **Racha actual:** {result['streak']} días
                **Bono por racha:** {currency_symbol} {result['bonus']}
                
                *Vuelve mañana para seguir tu racha.*
                """
            )
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="mcstatus", description="Muestra el estado del servidor de Minecraft")
    @app_commands.describe(ip="La IP del servidor (opcional si está configurada)")
    async def mcstatus_slash(self, interaction: discord.Interaction, ip: str = None):
        """Estado de Minecraft (slash)"""
        guild_config = db.get_guild_config(interaction.guild.id)
        
        if not guild_config["modules"]["minecraft"]:
            await interaction.response.send_message(embed=Embeds.error("El sistema de Minecraft está desactivado."))
            return
        
        server_ip = ip or guild_config["minecraft"]["server_ip"]
        if not server_ip:
            await interaction.response.send_message(embed=Embeds.error("No hay servidor de Minecraft configurado. Usa `/mcstatus <ip>`"))
            return
        
        await interaction.response.defer()
        
        # Obtener estado
        status = await MinecraftSystem.get_server_status(server_ip)
        embed = await MinecraftSystem.create_status_embed(server_ip, status)
        
        await interaction.followup.send(embed=embed)

# =============================================
# EVENTOS Y TAREAS AUTOMÁTICAS
# =============================================

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    bot.start_time = datetime.datetime.now()
    
    print(f"""
    ╔════════════════════════════════════════════════════╗
    ║              HONDUCRAFT ULTRA PRO 4.1              ║
    ║              BOT PROFESIONAL AVANZADO              ║
    ╚════════════════════════════════════════════════════╝
    
    ✅ Bot conectado como: {bot.user.name}
    📊 ID: {bot.user.id}
    🌐 Servidores: {len(bot.guilds):,}
    👥 Usuarios: {sum(g.member_count for g in bot.guilds):,}
    🚀 Versión: {BotConfig.VERSION}
    ⏰ Hora de inicio: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    📈 Latencia: {round(bot.latency * 1000)}ms
    
    🔧 Sistemas cargados:
    • ✅ Base de datos profesional
    • ✅ Sistema de moderación avanzado
    • ✅ Niveles y economía
    • ✅ Comandos tradicionales (!)
    • ✅ Comandos slash (/)
    • ✅ Sistema de Minecraft
    • ✅ Sistema de programación
    • ✅ Sistema de cache y performance
    • ✅ Logging y analytics
    • ✅ Tareas automáticas
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
    
    # Cambiar estado
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servidores | /help"
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
    
    # Sistema de niveles
    guild_config = db.get_guild_config(message.guild.id)
    if guild_config["modules"]["levels"]:
        await AdvancedLeveling.add_xp(message.author, message)
    
    # Procesar comandos tradicionales
    await bot.process_commands(message)

@bot.event
async def on_member_join(member: discord.Member):
    """Evento cuando un miembro se une al servidor"""
    guild_config = db.get_guild_config(member.guild.id)
    
    if guild_config["modules"]["welcome"] and guild_config["welcome"]["enabled"]:
        channel_id = guild_config["channels"]["welcome"]
        channel = member.guild.get_channel(channel_id) if channel_id else member.guild.system_channel
        
        if channel:
            welcome_message = guild_config["welcome"]["message"].format(
                user=member,
                server=member.guild
            )
            
            embed = Embeds.success(
                "👋 ¡Bienvenido/a!",
                welcome_message,
                color=guild_config["welcome"]["embed_color"]
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            
            await channel.send(embed=embed)
        
        # Mensaje por DM
        if guild_config["welcome"]["send_dm"]:
            try:
                dm_message = guild_config["welcome"]["dm_message"].format(
                    user=member,
                    server=member.guild
                )
                await member.send(dm_message)
            except:
                pass  # El usuario tiene los DMs cerrados

# =============================================
# TAREAS AUTOMÁTICAS
# =============================================

@tasks.loop(minutes=5)
async def update_presence():
    """Actualiza el estado del bot periódicamente"""
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servidores"),
        discord.Activity(type=discord.ActivityType.listening, name="/help"),
        discord.Activity(type=discord.ActivityType.playing, name=f"con {sum(g.member_count for g in bot.guilds):,} usuarios"),
        discord.Activity(type=discord.ActivityType.watching, name="Honducraft Pro"),
        discord.Activity(type=discord.ActivityType.competing, name="Minecraft & Programación")
    ]
    await bot.change_presence(activity=random.choice(activities))

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
            print("💡 Configura la variable de entorno DISCORD_TOKEN o reemplaza el token en el código")
            return
        
        logger.info("🚀 Iniciando Honducraft Ultra Pro 4.1...")
        await bot.start(TOKEN)
        
    except discord.LoginFailure:
        logger.error("❌ Error de autenticación: Token inválido")
    except KeyboardInterrupt:
        logger.info("⏹️ Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        traceback.print_exc()

# Truco para Render: servidor falso en puerto 10000
def fake_server():
    s = socket.socket()
    s.bind(('0.0.0.0', 10000))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        conn.close()

threading.Thread(target=fake_server, daemon=True).start()

# Ejecutar el bot
if __name__ == "__main__":
    asyncio.run(main())
