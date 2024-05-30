import pygame
from pathlib import Path
import os


class AssetManager:
    ASSET_PATH = Path(__file__).parent / ".." / "assets"
    cache = dict()

    @staticmethod
    def load_texture(name: str):
        hash_name = f'texture/{name}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        asset = pygame.image.load(AssetManager.ASSET_PATH / "textures" / name)
        AssetManager.cache[hash_name] = asset
        return asset

    @staticmethod
    def load_sound(name: str):
        hash_name = f'sound/{name}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        asset = pygame.mixer.Sound(AssetManager.ASSET_PATH / "audio" / name)
        AssetManager.cache[hash_name] = asset
        return asset

    @staticmethod
    def load_music(name: str):
        hash_name = f'music/{name}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        pygame.mixer.music.load(AssetManager.ASSET_PATH / "audio" / name)
        AssetManager.cache[hash_name] = True
        return True

    @staticmethod
    def load_map(name: str):
        hash_name = f'map/{name}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        with open(AssetManager.ASSET_PATH / "maps" / name) as f:
            asset = f.read()
        AssetManager.cache[hash_name] = asset
        return asset

    @staticmethod
    def load_font(name: str, size: int):
        hash_name = f'font/{name}/{size}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        asset = pygame.font.Font(AssetManager.ASSET_PATH / "fonts" / name, size)
        AssetManager.cache[hash_name] = asset
        return asset

    @staticmethod
    def load_theme(name: str):
        return AssetManager.ASSET_PATH / "themes" / name

    @staticmethod
    def load_shanty(name: str):
        return AssetManager.ASSET_PATH / "shanties" / name

    @staticmethod
    def list_shanties():
        return [f for f in os.listdir(AssetManager.ASSET_PATH / "shanties") if f.endswith(".shanty")]

    @staticmethod
    def load_cosmetic(name: str):
        hash_name = f'cosmetics/{name}'
        if hash_name in AssetManager.cache:
            return AssetManager.cache[hash_name]
        asset = pygame.image.load(AssetManager.ASSET_PATH / "textures/cosmetics" / name)
        AssetManager.cache[hash_name] = asset
        return asset

    @staticmethod
    def list_cosmetics():
        image_files = [f for f in os.listdir(AssetManager.ASSET_PATH / "textures/cosmetics") if f.endswith(".png")]
        return image_files