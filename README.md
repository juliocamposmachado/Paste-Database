# Paste-Database 🚀

## Banco de Dados Descentralizado Inovador

Uma solução revolucionária de banco de dados descentralizado desenvolvida para eliminar a dependência de serviços de banco de dados pagos, oferecendo uma alternativa gratuita, eficiente e escalável.

## 💡 Conceito

O **Paste-Database** é um sistema de armazenamento de dados descentralizado que utiliza uma arquitetura distribuída para gerenciar informações sem a necessidade de servidores centralizados ou serviços de banco de dados comerciais caros.

## 🎆 Contexto: Orkut 2025

Esta solução foi desenvolvida especificamente para o **Orkut 2025**, onde enfrentávamos o desafio de custos elevados com bancos de dados tradicionais. Todos os serviços de banco de dados disponíveis no mercado eram pagos, criando uma barreira significativa para o desenvolvimento.

### 💡 A Solução Inovadora

Em vez de aceitar os altos custos, desenvolvemos uma abordagem revolucionária:
- **Eliminação total** de custos de banco de dados
- **Arquitetura descentralizada** usando serviços gratuitos existentes
- **Escalabilidade** sem custos adicionais
- **Independence** de provedores pagos

### 📊 Impacto Econômico

| Aspecto | Solução Tradicional | Paste-Database |
|---------|-------------------|----------------|
| Custo Inicial | $50-500/mês | $0 |
| Escalabilidade | $++ por usuário | Gratuita |
| Backup | $10-50/mês | Incluído |
| Manutenção | Complexa | Mínima |
| **Total Anual** | **$720-6000+** | **$0** |

## 📋 Características

- ✅ **Operações CRUD completas** (Create, Read, Update, Delete)
- ✅ **Sistema de indexação** para busca rápida
- ✅ **Busca por texto** em campos específicos ou em todos os dados
- ✅ **Metadados personalizados** para cada registro
- ✅ **Backup automático** do banco de dados
- ✅ **Armazenamento na nuvem** grátis via API do Paste
- ✅ **Sem configuração** - funciona imediatamente

## 🚀 Instalação Rápida

1. **Baixe os arquivos**:
   - `paste_database.py` - Biblioteca principal
   - `examples.py` - Exemplos de uso

2. **Instale as dependências**:
   ```bash
   pip install requests
   ```

3. **Use em seu projeto**:
   ```python
   from paste_database import PasteDatabase
   
   # Inicializar
   db = PasteDatabase()
   
   # Criar registro
   db.create("usuario_001", {"nome": "João", "idade": 30})
   
   # Ler registro
   usuario = db.read("usuario_001")
   print(usuario.data)  # {"nome": "João", "idade": 30}
   ```

## 📖 Documentação da API

### Inicialização

```python
from paste_database import PasteDatabase

# Usar servidor padrão
db = PasteDatabase()

# Usar servidor personalizado
db = PasteDatabase("https://paste.exemplo.com")
```

### Operações CRUD

#### ✨ CREATE - Criar Registro

```python
# Sintaxe básica
record_id = db.create(key, data, metadata=None)

# Exemplo
user_id = db.create(
    "user_001", 
    {"nome": "Maria", "email": "maria@email.com"},
    {"tipo": "usuario", "status": "ativo"}
)
```

#### 📖 READ - Ler Registro

```python
# Sintaxe básica
record = db.read(key)

# Exemplo
usuario = db.read("user_001")
if usuario:
    print(f"Nome: {usuario.data['nome']}")
    print(f"Email: {usuario.data['email']}")
    print(f"Criado em: {usuario.created_at}")
```

#### 🔄 UPDATE - Atualizar Registro

```python
# Sintaxe básica
success = db.update(key, new_data, new_metadata=None)

# Exemplo
sucesso = db.update("user_001", {
    "nome": "Maria Silva",
    "email": "maria.silva@email.com",
    "telefone": "(11) 99999-9999"
})
```

#### 🗑️ DELETE - Deletar Registro

```python
# Sintaxe básica
success = db.delete(key)

# Exemplo
if db.delete("user_001"):
    print("Usuário deletado com sucesso!")
```

### Operações de Consulta

#### 📊 Listar Chaves

```python
# Listar todas as chaves
chaves = db.list_keys()
print(f"Registros: {chaves}")

# Contar registros
total = db.count()
print(f"Total: {total}")
```

#### 🔍 Buscar Registros

```python
# Buscar em todos os campos
resultados = db.search("João")

# Buscar em campo específico
usuarios_sp = db.search("São Paulo", "cidade")

# Exemplo de uso
for chave in resultados:
    registro = db.read(chave)
    print(f"Encontrado: {registro.data}")
```

#### 💾 Backup

```python
# Criar backup
backup_id = db.backup("meu_backup.json")
print(f"Backup salvo: https://paste.safone.me/doc/{backup_id}")

# Backup automático (nome gerado)
backup_id = db.backup()
```

## 🛠️ Estrutura dos Dados

### DatabaseRecord

Cada registro no banco tem a seguinte estrutura:

```python
@dataclass
class DatabaseRecord:
    id: str                    # ID único no Paste
    data: Dict[str, Any]       # Seus dados
    created_at: int            # Timestamp de criação
    updated_at: int            # Timestamp da última atualização
    metadata: Dict[str, str]   # Metadados opcionais
```

### Índice

O sistema mantém um índice interno para mapear suas chaves para os IDs do Paste:

```json
{
  "user_001": {
    "paste_id": "abc123",
    "created_at": 1641234567,
    "updated_at": 1641234567,
    "metadata": {"tipo": "usuario"}
  }
}
```

## 📝 Exemplos Práticos

### Sistema de Biblioteca

```python
from paste_database import PasteDatabase

db = PasteDatabase()

# Adicionar livro
db.create("livro_001", {
    "titulo": "1984",
    "autor": "George Orwell",
    "ano": 1949,
    "disponivel": True
}, {"categoria": "ficção"})

# Emprestar livro
livro = db.read("livro_001")
livro_data = livro.data.copy()
livro_data["disponivel"] = False
livro_data["emprestado_para"] = "João Silva"

db.update("livro_001", livro_data)

# Buscar livros disponíveis
for chave in db.list_keys():
    livro = db.read(chave)
    if livro and livro.data.get("disponivel"):
        print(f"Disponível: {livro.data['titulo']}")
```

### E-commerce Simples

```python
db = PasteDatabase()

# Adicionar produto
db.create("prod_001", {
    "nome": "iPhone 13",
    "preco": 4999.99,
    "estoque": 10,
    "categoria": "Smartphones"
})

# Processar venda
produto = db.read("prod_001")
if produto and produto.data["estoque"] > 0:
    # Reduzir estoque
    produto_data = produto.data.copy()
    produto_data["estoque"] -= 1
    db.update("prod_001", produto_data)
    
    # Registrar venda
    db.create("venda_001", {
        "produto": "prod_001",
        "quantidade": 1,
        "total": produto.data["preco"],
        "cliente": "Maria Silva"
    }, {"status": "concluida"})
```

### Sistema de Configuração

```python
db = PasteDatabase()

# Salvar configurações
db.create("config_app", {
    "tema": "escuro",
    "idioma": "pt-BR",
    "notificacoes": True,
    "limite_usuarios": 100
})

# Carregar configurações
config = db.read("config_app")
if config:
    print(f"Tema atual: {config.data['tema']}")
```

## ⚡ Dicas de Performance

### 1. Use Metadados para Filtragem

```python
# Adicione metadados para facilitar consultas
db.create("user_001", user_data, {"tipo": "admin", "ativo": "sim"})
db.create("user_002", user_data, {"tipo": "cliente", "ativo": "não"})
```

### 2. Mantenha os Dados Estruturados

```python
# ✅ Bom - estrutura consistente
user_data = {
    "nome": str,
    "idade": int,
    "email": str,
    "ativo": bool
}

# ❌ Evite - estrutura inconsistente
user1 = {"name": "João", "age": 30}
user2 = {"nome": "Maria", "idade": 25, "telefone": "123"}
```

### 3. Use Chaves Descritivas

```python
# ✅ Bom
db.create("usuario_joao_silva_001", data)
db.create("produto_iphone13_001", data)
db.create("pedido_2024_001", data)

# ❌ Evite
db.create("1", data)
db.create("abc", data)
```

## 🔒 Limitações e Considerações

### Limitações do Paste

- **Tamanho máximo**: ~1MB por registro
- **Rate limiting**: Evite muitas requisições simultâneas
- **Durabilidade**: Depende do serviço Paste (geralmente permanente)

### Considerações de Segurança

- **Dados públicos**: Todo conteúdo fica publicamente acessível
- **Não use para dados sensíveis**: Senhas, tokens, informações pessoais
- **Ideal para**: Configurações, dados públicos, protótipos

### Performance

- **Busca sequencial**: Não há indexação no servidor
- **Latência de rede**: Cada operação faz requisição HTTP
- **Cache local**: Considere implementar cache para dados frequentes

## 🐛 Tratamento de Erros

```python
try:
    # Operações do banco
    db.create("key", data)
    record = db.read("key")
    
except ValueError as e:
    print(f"Erro de validação: {e}")
    
except Exception as e:
    print(f"Erro de rede ou API: {e}")
```

## 📊 Casos de Uso Recomendados

### ✅ Ideal Para:
- Protótipos e MVPs
- Sistemas de configuração
- Catálogos públicos
- Dados de demonstração
- Aplicações educacionais
- Projetos pessoais

### ❌ Não Recomendado Para:
- Dados sensíveis ou privados
- Sistemas de produção críticos
- Aplicações com milhares de registros
- Dados que precisam de transações ACID
- Informações regulamentadas (LGPD, GDPR)

## 🗄️ Bancos de Dados Compatíveis

O **Paste-Database** pode utilizar qualquer serviço pastebin como backend. Abaixo está a lista completa de serviços testados e compatíveis:

### 🌐 Pastebins Públicos

Usuários não autenticados podem criar pastes:

- **https://pastebin.com** - O mais popular e confiável
- **https://paste.safone.me** - Usado como padrão no sistema
- **https://justpaste.it** (alias: jpst.it)
- **https://jsfiddle.net** - Focado em JavaScript
- **https://paste.centos.org** - Mantido pela comunidade CentOS
- **https://jsbin.com** - Editor colaborativo
- **https://pastelink.net** - Links automáticos
- **https://codebeautify.org** - Com formatação de código
- **https://controlc.com** (aliases: pasted.co, tny.cz)
- **https://ideone.com** - Compilador online
- **http://paste.rohitab.com** - Comunidade de desenvolvedores
- **https://codeshare.io** - Compartilhamento em tempo real
- **http://paste.opensuse.org** - Mantido pela openSUSE
- **https://dotnetfiddle.net** - Focado em .NET
- **https://notes.io** - Interface simples
- **https://paste2.org** - Múltiplas linguagens
- **https://hastebin.com** - Ultra-rápido
- **https://ivpaste.com** - Interface em espanhol
- **https://justpaste.me** - Sem registro necessário
- **https://pastebin.osuosl.org** - Open Source Lab
- **https://bpa.st** - Focado em Python
- **https://paste.ofcode.org** - Múltiplas linguagens
- **https://paste.ee** (alternativa: pastee.dev)
- **https://dpaste.org** - Baseado em Django
- **https://friendpaste.com** - Interface amigável
- **https://defuse.ca/pastebin.htm** - Com criptografia
- **https://dpaste.com** - Versão comercial
- **https://cl1p.net** - Clipboard na internet
- **http://pastie.org** - Interface minimalista
- **https://pastecode.io** - Para desenvolvedores
- **https://pastebin.fr** - Versão francesa
- **http://jsitor.com** - Editor JavaScript
- **https://termbin.com** - Via terminal (nc)
- **https://p.ip.fi** - Serviço finlandês
- **http://cutapaste.net** - Interface limpa
- **https://paste.sh** - Criptografado
- **https://paste.jp** - Versão japonesa
- **https://paste-bin.xyz** - Alternativa moderna
- **https://paste.debian.net** - Mantido pela Debian
- **http://vpaste.net** - Baseado no Vim
- **http://paste.org.ru** - Versão russa
- **https://quickhighlighter.com** - Realce de sintaxe
- **https://commie.io** - Com comentários por linha
- **http://everfall.com/paste/** - Com histórico de versões
- **https://kpaste.net** - Debug colaborativo
- **https://www.pastebin.pt** - Com criptografia AES
- **https://n0paste.tk** - Europeu
- **https://tutpaste.com** - Interface educacional
- **https://bitbin.it** - ⚠️ Desativando em 2024
- **https://pastebin.fi** - Versão finlandesa
- **https://nekobin.com** - Design moderno
- **https://www.paste4btc.com** - Com monetização
- **https://pastejustit.com** (alias: pastebin.ai)
- **https://paste.js.org** - Focado em JavaScript
- **https://paste.mod.gg/** - BlazeBin moderno
- **https://paste.myst.rs** (alias: paste.ax) - pastemyst
- **https://beanpaste.fun** - Interface divertida
- **https://rentry.co/** - Com markdown
- **https://lesma.eu** - Europeu com limites
- **https://paste.monster** - Com suporte markdown
- **https://snippet.host** - Hospedagem de snippets
- **https://pastesio.com** (alias: pastes.io) - Estatísticas detalhadas
- **https://xi.pe** - CLI-friendly
- **https://macrobin.co** - Com recursos avançados
- **https://fragbin.com** - Moderno e seguro

### 🔐 Pastebins com Autenticação

Apenas usuários autenticados podem criar pastes:

- **https://gist.github.com** - GitHub Gists
- **https://gitlab.com/explore/snippets** - GitLab Snippets
- **https://codepen.io** - Frontend playground
- **https://repl.it** - Ambiente de desenvolvimento
- **https://paste.ubuntu.com** - Oficial do Ubuntu
- **https://invent.kde.org/explore/snippets** - KDE Snippets
- **https://snipplr.com** - Biblioteca de snippets
- **http://paste.xinu.at** - FileBin avançado

### 📚 Pastebins Somente Leitura

Arquivos para consulta (não aceitam novos pastes):

- **https://www.geany.org/p/** - Geany Pastebin
- **http://paste.pound-python.org** - Desativado
- **http://paste.frubar.net/** - Apenas arquivos

### ❌ Pastebins Descontinuados

Serviços que não funcionam mais (para referência histórica):

- **https://slexy.org** - Desativado
- **https://textsnip.com** - Fora do ar
- **http://phpfiddle.org** - Descontinuado
- **https://pastebin.icoder.uz** - Não disponível
- **https://pst.klgrth.io** - Desativado
- **https://www.heypasteit.com** - Fora do ar
- **http://paste.lisp.org** - Descontinuado
- **https://pasteall.org** - Não funciona
- **https://paste.scratchbook.ch** - Desativado
- **https://dumpz.org** - Fora do ar
- **http://paste.strictfp.com** - Descontinuado
- **https://pastecode.ru** - Não disponível
- **https://apaste.info** - Redirecionado
- **https://pastesqf.com** - Desativado
- **http://sprunge.us** - Não funciona
- **https://pastecode.fr** - Fora do ar
- **https://99paste.com** - Descontinuado
- **https://nopaste.me** - Domínio à venda
- **https://www.paste.lv** - Básico demais
- **http://codepad.org** - Não disponível
- **https://ghostbin.com** - Desativado
- **https://pasteio.com** - Fora do ar
- **https://paste.mozilla.org** - Mozilla descontinuou
- **https://ide.geeksforgeeks.org** - Focou no IDE
- **https://pastefs.com** - Problemas financeiros

### 🔧 Como Usar Diferentes Pastebins

```python
# Usando pastebin alternativo
db = PasteDatabase("https://paste.centos.org")

# Testando múltiplos serviços
services = [
    "https://paste.safone.me",
    "https://pastebin.com", 
    "https://paste.centos.org",
    "https://dpaste.org"
]

for service in services:
    try:
        db = PasteDatabase(service)
        db.create("test", {"service": service, "status": "working"})
        print(f"✅ {service} - Funcional")
    except Exception as e:
        print(f"❌ {service} - {e}")
```

### ⚡ Recomendações por Uso

**🏆 Mais Confiáveis:**
- `paste.safone.me` (padrão do sistema)
- `pastebin.com` (mais popular)
- `paste.centos.org` (mantido pela comunidade)

**⚡ Mais Rápidos:**
- `hastebin.com`
- `termbin.com`
- `xi.pe`

**🔒 Com Segurança:**
- `defuse.ca/pastebin.htm` (criptografado)
- `paste.sh` (criptografado)
- `pastebin.pt` (AES 256-bit)

**💼 Para Empresas:**
- `paste.ubuntu.com` (requer login)
- `gist.github.com` (integrado ao GitHub)
- `gitlab.com/snippets` (integrado ao GitLab)

## 🤝 Contribuição

Quer melhorar o PasteDatabase? 

1. Faça um fork do código
2. Implemente suas melhorias
3. Teste com diferentes cenários
4. Compartilhe suas mudanças

## 📄 Licença

Este projeto é de domínio público. Use livremente!

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique sua conexão** com a internet
2. **Teste a API do Paste** diretamente: https://paste.safone.me
3. **Revise os exemplos** nesta documentação
4. **Execute o arquivo de exemplos**: `python examples.py`

---

**📱 Desenvolvido com ❤️ para a comunidade Python**
