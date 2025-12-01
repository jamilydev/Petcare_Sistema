# 🐶 PetCare - Sistema de Gestão Veterinária

Sistema web desenvolvido como projeto final da disciplina de **Programação Orientada a Objetos (POO)**.

O objetivo foi criar uma aplicação completa aplicando conceitos de POO, arquitetura MVC, Padrão DAO e persistência de dados.

## 📋 Sobre o Projeto

O **PetCare** é um sistema para gerenciar uma clínica veterinária. Ele permite o cadastro de clientes e seus animais, gestão de veterinários, agendamento de consultas e controle de vacinas.

Um diferencial do projeto é o módulo de **Gamificação**, onde os donos acumulam pontos e sobem de nível conforme cuidam da saúde de seus pets.

### ✨ Funcionalidades Principais

* **Gestão de Clientes:** Cadastro, edição e exclusão de donos.
* **Gestão de Pets:** Vínculo de animais aos seus donos.
* **Corpo Clínico:** Cadastro de veterinários com especialidades e CRMV.
* **Agenda:** Agendamento de consultas vinculando Pet + Veterinário.
* **Gamificação (Dashboard):** Sistema de pontos e níveis com barra de progresso visual.
* **Segurança:** Integridade de dados (não permite excluir donos sem antes tratar os dependentes).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** Flask
* **Banco de Dados:** SQLite (com Foreign Keys)
* **Frontend:** HTML5, CSS3 (Design Responsivo)
* **Arquitetura:** MVC (Model-View-Controller) com DAO (Data Access Object)

## 📂 Estrutura do Projeto

O projeto foi estruturado seguindo boas práticas de separação de responsabilidades:

```text
projeto_petcare/
│
├── app/
│   ├── dao/             # Camada de Acesso a Dados (SQL/CRUD)
│   ├── model/           # Classes e Objetos do sistema
│   ├── routes/          # Rotas da API e Controladores Web
│   ├── static/          # Arquivos CSS e Imagens
│   ├── templates/       # Páginas HTML (Jinja2)
│   └── database/        # Arquivo do Banco de Dados SQLite
│
├── main.py              # Arquivo principal de execução
└── requirements.txt     # Dependências do projeto
