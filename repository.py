#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с репозиторием Ubuntu (apt)
"""

import urllib.request
import gzip
import re
from typing import Dict, List, Optional


class PackageRepository:
    """Класс для работы с репозиторием пакетов Ubuntu"""
    
    def __init__(self, repository_url: str, test_mode: bool = False):
        """
        Инициализация репозитория
        
        Args:
            repository_url: URL репозитория или путь к файлу
            test_mode: Флаг тестового режима
        """
        self.repository_url = repository_url
        self.test_mode = test_mode
        self.packages_cache = {}
        
    def fetch_packages_file(self) -> str:
        """
        Получить содержимое файла Packages из репозитория
        
        Returns:
            str: Содержимое файла Packages
        """
        if self.test_mode:
            return self._read_local_file(self.repository_url)
        else:
            return self._fetch_from_url(self.repository_url)
    
    def _read_local_file(self, filepath: str) -> str:
        """Чтение локального тестового файла"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Тестовый файл не найден: {filepath}")
        except Exception as e:
            raise Exception(f"Ошибка чтения файла: {e}")
    
    def _fetch_from_url(self, url: str) -> str:
        """Загрузка файла Packages из URL"""
        try:
            packages_url = self._construct_packages_url(url)
            print(f"Загрузка данных из: {packages_url}")
            
            with urllib.request.urlopen(packages_url, timeout=30) as response:
                compressed_data = response.read()
            
            decompressed_data = gzip.decompress(compressed_data)
            return decompressed_data.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Ошибка загрузки репозитория: {e}")
    
    def _construct_packages_url(self, base_url: str) -> str:
        """Построить URL к файлу Packages.gz"""
        if base_url.endswith('/'):
            base_url = base_url.rstrip('/')
        
        return f"{base_url}/dists/jammy/main/binary-amd64/Packages.gz"
    
    def parse_packages(self, packages_data: str) -> Dict[str, Dict]:
        """
        Парсинг файла Packages в структуру данных
        
        Args:
            packages_data: Содержимое файла Packages
            
        Returns:
            Dict: Словарь с информацией о пакетах
        """
        packages = {}
        current_package = {}
        current_field = None
        
        for line in packages_data.split('\n'):
            if line.strip() == '':
                if current_package and 'Package' in current_package:
                    pkg_name = current_package['Package']
                    packages[pkg_name] = current_package
                current_package = {}
                current_field = None
                continue
            
            if line.startswith(' '):
                if current_field:
                    current_package[current_field] += '\n' + line.strip()
                continue
            
            if ':' in line:
                field, value = line.split(':', 1)
                field = field.strip()
                value = value.strip()
                current_package[field] = value
                current_field = field
        
        return packages
    
    def get_package_info(self, package_name: str) -> Optional[Dict]:
        """
        Получить информацию о конкретном пакете
        
        Args:
            package_name: Имя пакета
            
        Returns:
            Dict или None: Информация о пакете
        """
        if not self.packages_cache:
            packages_data = self.fetch_packages_file()
            self.packages_cache = self.parse_packages(packages_data)
        
        return self.packages_cache.get(package_name)
    
    def get_dependencies(self, package_name: str) -> List[str]:
        """
        Получить список зависимостей для пакета
        
        Args:
            package_name: Имя пакета
            
        Returns:
            List[str]: Список имён зависимых пакетов
        """
        package_info = self.get_package_info(package_name)
        
        if not package_info:
            return []
        
        depends_str = package_info.get('Depends', '')
        
        if not depends_str:
            return []
        
        dependencies = []
        
        for dep in depends_str.split(','):
            dep = dep.strip()
            dep = re.sub(r'\s*\([^)]*\)', '', dep)
            
            if '|' in dep:
                dep = dep.split('|')[0].strip()
            
            if dep:
                dependencies.append(dep)
        
        return dependencies
    
    def get_all_packages(self) -> List[str]:
        """
        Получить список всех доступных пакетов
        
        Returns:
            List[str]: Список имён пакетов
        """
        if not self.packages_cache:
            packages_data = self.fetch_packages_file()
            self.packages_cache = self.parse_packages(packages_data)
        
        return list(self.packages_cache.keys())
