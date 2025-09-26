# Projeto: Persistência Poliglota com MongoDB + SQLite e Geoprocessamento em Python

## 1. Introdução
Este projeto foi desenvolvido como parte da disciplina de Banco de Dados e tem como objetivo demonstrar o uso de **persistência poliglota**, integrando diferentes tecnologias para armazenamento e consulta de dados.

O sistema utiliza:
- **SQLite** para dados tabulares (cidades/estados).
- **MongoDB** para documentos JSON com dados geográficos (locais com latitude e longitude).
- **Streamlit** para interface interativa com o usuário.
- **Geopy** para cálculo de distâncias geográficas.

---

## 2. Arquitetura do Sistema

### Estrutura de pastas:
```c
projeto_persistencia_poliglota/
│── app.py 
│── db_sqlite.py 
│── db_mongo.py 
│── geoprocessamento.py 
│── requirements.txt 
```

### Fluxo geral do sistema:
1. O usuário cadastra Estados e Cidades no SQLite.
2. O usuário cadastra Locais no MongoDB (associados a uma cidade).
3. A interface permite:
   - Listar cidades (SQLite).
   - Exibir locais do MongoDB relacionados a uma cidade do SQLite.
   - Consultar locais próximos a partir de uma coordenada informada.
4. Os resultados podem ser visualizados em tabelas e mapas.

---

## 3. Tecnologias Utilizadas
- **Python 3.11**
- **Streamlit** (frontend interativo)
- **SQLite3** (banco relacional embutido)
- **MongoDB Atlas** (banco NoSQL em nuvem)
- **PyMongo** (driver do MongoDB para Python)
- **Geopy** (cálculo de distâncias)
- **Folium / st.map()** (visualização geográfica)
- **Pandas** (manipulação de dados tabulares)

---

## 4. Exemplos de Consultas

### 4.1 Inserção de Cidade (SQLite)
```sql
INSERT INTO cidades (nome, estado_id) VALUES ("João Pessoa", 1);
{
  "nome_local": "Praça da Independência",
  "cidade": "João Pessoa",
  "descricao": "Ponto turístico central da cidade",
  "coordenadas": {
    "type": "Point",
    "coordinates": [-34.861, -7.11532]
  }
}
```
### 4.3 Consulta Integrada

Selecionando a cidade “João Pessoa” cadastrada no SQLite, o sistema exibe todos os locais relacionados no MongoDB.

### 4.4 Consulta por Proximidade

Dada uma coordenada (-7.120, -34.880) e raio de 10 km, o sistema retorna todos os locais armazenados no MongoDB dentro desse raio.

---
## 5. imagens de teste 

### 1 Cadastrar Estado e Cidade
<img width="1433" height="601" alt="image" src="https://github.com/user-attachments/assets/069a3b8c-ef4a-4031-9ca9-4779009600d9" />

### 2 Cadastrar Local
<img width="1319" height="633" alt="image" src="https://github.com/user-attachments/assets/8c0380cb-fc28-48c6-a56b-ca769b07add6" />

### 3 Consultar locais por cidade
<img width="1361" height="535" alt="image" src="https://github.com/user-attachments/assets/61ea9db8-11f9-4b20-aeb7-86927dec680f" />

### 4 Buscar locais por proximidade (a partir de uma coordenada)
<img width="1377" height="699" alt="image" src="https://github.com/user-attachments/assets/138cbeb0-9a96-4378-8220-c3e5368e945a" />
