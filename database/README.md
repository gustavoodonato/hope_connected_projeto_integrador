# Bancos de dados do Hope Connected (rodando na sua máquina)

O projeto usa **dois bancos**:

| Banco | O que guarda | Arquivo |
|---|---|---|
| **MySQL** (`hope_connected`) | usuários, solicitações, atendimentos e envios | `mysql/01_criar_tabelas.sql` e `mysql/02_dados_exemplo.sql` |
| **MongoDB** (`hope_connected_nosql`) | impressoras 3D e detalhes de impressão (link do STL e configurações) | `mongodb/hope_connected_nosql.js` |

> As impressoras ficam **só no MongoDB**. Não existe tabela de impressoras no MySQL.

---

## 1. Instalar (uma vez só)

- **MySQL:** baixe o *MySQL Installer* em dev.mysql.com/downloads/installer e instale o **MySQL Server 8** e o **MySQL Workbench**. Anote a senha do usuário `root` que você escolher.
- **MongoDB:** baixe o *MongoDB Community Server* e o **MongoDB Compass** em mongodb.com/try/download/community. O Compass já tem um terminal embutido (o MONGOSH), então o `mongosh` separado é opcional.

## 2. Criar o banco MySQL

**Pelo Workbench (mais fácil):**
1. Abra o Workbench e entre na conexão local (`localhost`, usuário `root`).
2. Menu **File > Open SQL Script** e escolha `mysql/01_criar_tabelas.sql`.
3. Clique no raio ⚡ (Execute). Depois repita com `mysql/02_dados_exemplo.sql`.

**Pelo terminal:**
```
mysql -u root -p
source C:/caminho/do/projeto/database/mysql/01_criar_tabelas.sql;
source C:/caminho/do/projeto/database/mysql/02_dados_exemplo.sql;
```
Use barras normais (`/`) no caminho. No PowerShell, o símbolo `<` não funciona para isso, por isso o `source`.

**Conferir:**
```sql
USE hope_connected;
SHOW TABLES;            -- 4 tabelas
SELECT * FROM usuarios; -- 3 usuários
```

## 3. Criar o banco MongoDB

1. Confirme que o MongoDB está rodando (o instalador cria o serviço *MongoDB Server*).
2. Abra o **Compass** e conecte em `mongodb://localhost:27017`.
3. Abra o **MONGOSH** (barra na parte de baixo da tela), cole **todo** o conteúdo de `mongodb/hope_connected_nosql.js` e aperte Enter.

Ou, pelo terminal, dentro da pasta `mongodb`:
```
mongosh --file hope_connected_nosql.js
```

**Conferir:** deve aparecer o banco `hope_connected_nosql` com as coleções `impressoras_3d` (3 documentos) e `detalhes_impressao` (4 documentos). O próprio script imprime essas contagens no final. No fim do arquivo há exemplos de consultas (`find`, `findOne`, `updateOne`) para copiar e testar.

## 4. Como os dois bancos se ligam

O MongoDB não confere chaves estrangeiras, então a ligação é feita pelos ids, e o **back-end** é quem precisa checar se eles existem.

| De | Para |
|---|---|
| `impressoras_3d.id_usuario_fornecedor` (Mongo) | `usuarios.id` (MySQL) |
| `detalhes_impressao.id_solicitacao` (Mongo) | `solicitacoes.id` (MySQL) |
| `atendimentos_solicitacao.id_impressora` (MySQL) | `impressoras_3d._id` (Mongo, texto de 24 caracteres) |

Em `atendimentos_solicitacao` fica também uma **cópia das especificações** da impressora (modelo, tecnologia e volume) no momento em que o fornecedor aceita o pedido.

## 5. Dados de exemplo

- Usuários (mesmos ids do mock do back-end): `123` Murilo (AACD), `456` Lucas e `789` Julio (fornecedores).
- A senha de todos é **`senha123`** (só para desenvolvimento).
- As solicitações 2 e 4 já têm atendimento, e a 4 tem envio (Correios), para testar a cadeia completa.

## 6. Começar do zero

Rode os scripts de novo. **Cuidado:** o `01_criar_tabelas.sql` apaga o banco `hope_connected` e o script do Mongo apaga as duas coleções antes de recriar. Tudo que foi cadastrado à mão se perde.

## 7. Dados para conectar o back-end (depois)

- MySQL: `localhost`, porta `3306`, usuário `root` e a senha que você definiu.
- MongoDB: `mongodb://localhost:27017`, banco `hope_connected_nosql`.

Não coloque senha no código nem no GitHub. Quando ligarem o back-end, guardem esses dados em um arquivo `.env` que esteja no `.gitignore`.

## Observações

- Os nomes das colunas do MySQL seguem as entidades do back-end (`User` e `Solicitacao`): `nome`, `email`, `senha_hash`, `phone`, `role`, `nome_peca`, `material_requerido`, `quantidade`, `prioridade`, `status` e `data_criacao`.
- O volume de impressão está em **milímetros** (`x_mm`, `y_mm`, `z_mm`).
- Os links de STL do script do Mongo são fictícios (`exemplo.com`).
