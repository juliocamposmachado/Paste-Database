import requests
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import urllib.parse
import re

@dataclass
class DatabaseRecord:
    """Representa um registro no banco de dados"""
    id: str
    data: Dict[str, Any]
    created_at: int
    updated_at: int
    metadata: Dict[str, str] = None

class PastebinService:
    """Classe base para serviços de pastebin"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MultiPasteDatabase/1.0'
        })
    
    def create_paste(self, content: str, title: str = "") -> str:
        """Cria um paste e retorna o ID"""
        raise NotImplementedError
    
    def get_paste(self, paste_id: str) -> str:
        """Obtém o conteúdo de um paste"""
        raise NotImplementedError
    
    def delete_paste(self, paste_id: str) -> bool:
        """Deleta um paste (se suportado)"""
        return False  # Nem todos os serviços suportam

class DPasteService(PastebinService):
    """Implementação para dpaste.org"""
    
    def __init__(self):
        super().__init__("DPaste", "https://dpaste.org")
    
    def create_paste(self, content: str, title: str = "") -> str:
        data = {
            'content': content,
            'syntax': 'json',
            'expiry_days': 365  # 1 ano
        }
        
        if title:
            data['title'] = title
        
        response = self.session.post(f"{self.base_url}/api/v2/", data=data)
        response.raise_for_status()
        
        # dpaste retorna a URL completa, extrair o ID
        url = response.text.strip()
        paste_id = url.split('/')[-1]
        return paste_id
    
    def get_paste(self, paste_id: str) -> str:
        # Adicionar .txt para obter versão raw
        url = f"{self.base_url}/{paste_id}.txt"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

class PasteEeService(PastebinService):
    """Implementação para paste.ee (API simples)"""
    
    def __init__(self):
        super().__init__("Paste.ee", "https://paste.ee")
    
    def create_paste(self, content: str, title: str = "") -> str:
        # paste.ee tem API, mas vou usar interface web simplificada
        data = {
            'paste': content,
            'language': 'json',
            'expire': '1year'
        }
        
        response = self.session.post(f"{self.base_url}/submit", data=data)
        response.raise_for_status()
        
        # Extrair ID da resposta
        if 'paste.ee/p/' in response.text:
            match = re.search(r'paste\.ee/p/([a-zA-Z0-9]+)', response.text)
            if match:
                return match.group(1)
        
        raise Exception("Não foi possível extrair ID do paste")
    
    def get_paste(self, paste_id: str) -> str:
        url = f"{self.base_url}/r/{paste_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

class HasteService(PastebinService):
    """Implementação para hastebin.com"""
    
    def __init__(self):
        super().__init__("Hastebin", "https://hastebin.com")
    
    def create_paste(self, content: str, title: str = "") -> str:
        response = self.session.post(
            f"{self.base_url}/documents",
            data=content.encode('utf-8'),
            headers={'Content-Type': 'text/plain'}
        )
        response.raise_for_status()
        
        result = response.json()
        return result['key']
    
    def get_paste(self, paste_id: str) -> str:
        url = f"{self.base_url}/raw/{paste_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

class MultiPasteDatabase:
    """
    Banco de dados que pode usar múltiplos serviços de pastebin como backend
    """
    
    def __init__(self, preferred_service: str = "dpaste"):
        self.services = {
            "dpaste": DPasteService(),
            "pasteee": PasteEeService(),
            "hastebin": HasteService()
        }
        
        self.preferred_service = preferred_service
        self.current_service = None
        
        # Encontrar um serviço funcionando
        self._find_working_service()
        
        # Índice local
        self.index = {}
        self.index_paste_id = None
    
    def _find_working_service(self):
        """Encontra um serviço de pastebin que esteja funcionando"""
        test_services = [self.preferred_service] + [k for k in self.services.keys() if k != self.preferred_service]
        
        for service_name in test_services:
            try:
                service = self.services[service_name]
                # Teste simples de conectividade
                response = service.session.head(service.base_url, timeout=5)
                if response.status_code < 500:  # Não é erro de servidor
                    self.current_service = service
                    print(f"✅ Usando serviço: {service.name} ({service.base_url})")
                    return
            except:
                continue
        
        raise Exception("Nenhum serviço de pastebin está acessível")
    
    def _load_index(self):
        """Carrega o índice do banco de dados"""
        if self.index_paste_id:
            try:
                content = self.current_service.get_paste(self.index_paste_id)
                self.index = json.loads(content)
            except:
                self.index = {}
    
    def _save_index(self):
        """Salva o índice do banco de dados"""
        index_content = json.dumps(self.index, indent=2, ensure_ascii=False)
        
        paste_id = self.current_service.create_paste(
            index_content,
            "MultiPasteDB_Index.json"
        )
        
        old_index_id = self.index_paste_id
        self.index_paste_id = paste_id
        
        print(f"📋 Índice atualizado: {self.current_service.base_url}/{paste_id}")
        
        # Tentar deletar índice antigo se suportado
        if old_index_id:
            try:
                self.current_service.delete_paste(old_index_id)
            except:
                pass
    
    def create(self, key: str, data: Dict[str, Any], metadata: Dict[str, str] = None) -> str:
        """Cria um novo registro no banco de dados"""
        if not self.index:
            self._load_index()
            
        # Verifica se a chave já existe
        if key in self.index:
            raise ValueError(f"Chave '{key}' já existe no banco de dados")
        
        # Prepara o registro
        record = DatabaseRecord(
            id="",
            data=data,
            created_at=int(time.time()),
            updated_at=int(time.time()),
            metadata=metadata or {}
        )
        
        # Cria o paste
        content = json.dumps(record.__dict__, indent=2, ensure_ascii=False)
        paste_id = self.current_service.create_paste(content, f"MultiPasteDB_{key}.json")
        
        record.id = paste_id
        
        # Atualiza o índice
        self.index[key] = {
            'paste_id': paste_id,
            'service': self.current_service.name,
            'created_at': record.created_at,
            'updated_at': record.updated_at,
            'metadata': record.metadata
        }
        
        self._save_index()
        
        print(f"📝 Registro criado: {self.current_service.base_url}/{paste_id}")
        return paste_id
    
    def read(self, key: str) -> Optional[DatabaseRecord]:
        """Lê um registro do banco de dados"""
        if not self.index:
            self._load_index()
            
        if key not in self.index:
            return None
            
        paste_id = self.index[key]['paste_id']
        
        try:
            content = self.current_service.get_paste(paste_id)
            record_data = json.loads(content)
            
            return DatabaseRecord(
                id=record_data.get('id', ''),
                data=record_data.get('data', {}),
                created_at=record_data.get('created_at', 0),
                updated_at=record_data.get('updated_at', 0),
                metadata=record_data.get('metadata', {})
            )
        except Exception as e:
            print(f"⚠️  Erro ao ler registro '{key}': {e}")
            return None
    
    def update(self, key: str, data: Dict[str, Any], metadata: Dict[str, str] = None) -> bool:
        """Atualiza um registro existente"""
        if not self.index:
            self._load_index()
            
        if key not in self.index:
            return False
        
        # Lê o registro atual
        current_record = self.read(key)
        if not current_record:
            return False
        
        # Cria novo registro
        updated_record = DatabaseRecord(
            id="",
            data=data,
            created_at=current_record.created_at,
            updated_at=int(time.time()),
            metadata=metadata or current_record.metadata
        )
        
        # Cria novo paste
        content = json.dumps(updated_record.__dict__, indent=2, ensure_ascii=False)
        paste_id = self.current_service.create_paste(content, f"MultiPasteDB_{key}.json")
        
        updated_record.id = paste_id
        
        # Atualiza o índice
        self.index[key] = {
            'paste_id': paste_id,
            'service': self.current_service.name,
            'created_at': updated_record.created_at,
            'updated_at': updated_record.updated_at,
            'metadata': updated_record.metadata
        }
        
        self._save_index()
        
        return True
    
    def delete(self, key: str) -> bool:
        """Deleta um registro do banco de dados"""
        if not self.index:
            self._load_index()
            
        if key not in self.index:
            return False
        
        # Remove do índice (pastes ficam no serviço mas não são mais acessíveis via DB)
        del self.index[key]
        self._save_index()
        
        return True
    
    def list_keys(self) -> List[str]:
        """Lista todas as chaves no banco de dados"""
        if not self.index:
            self._load_index()
            
        return list(self.index.keys())
    
    def search(self, query: str, field: str = None) -> List[str]:
        """Busca registros que contenham o termo especificado"""
        results = []
        
        for key in self.list_keys():
            record = self.read(key)
            if record:
                if field:
                    if field in record.data and query.lower() in str(record.data[field]).lower():
                        results.append(key)
                else:
                    record_str = json.dumps(record.data).lower()
                    if query.lower() in record_str:
                        results.append(key)
        
        return results
    
    def count(self) -> int:
        """Retorna o número de registros no banco de dados"""
        if not self.index:
            self._load_index()
            
        return len(self.index)
    
    def backup(self, filename: str = None) -> str:
        """Cria um backup completo do banco de dados"""
        if not filename:
            filename = f"MultiPasteDB_Backup_{int(time.time())}.json"
            
        backup_data = {
            'service': self.current_service.name,
            'service_url': self.current_service.base_url,
            'backup_time': int(time.time()),
            'index': self.index,
            'records': {}
        }
        
        # Coleta todos os registros
        print("📦 Coletando registros para backup...")
        for key in self.list_keys():
            record = self.read(key)
            if record:
                backup_data['records'][key] = record.__dict__
                print(f"   ✓ {key}")
        
        # Salva o backup
        content = json.dumps(backup_data, indent=2, ensure_ascii=False)
        paste_id = self.current_service.create_paste(content, filename)
        
        print(f"💾 Backup salvo: {self.current_service.base_url}/{paste_id}")
        return paste_id
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o banco de dados"""
        if not self.index:
            self._load_index()
        
        return {
            'service': self.current_service.name,
            'service_url': self.current_service.base_url,
            'total_records': len(self.index),
            'index_paste_id': self.index_paste_id,
            'available_services': list(self.services.keys())
        }
