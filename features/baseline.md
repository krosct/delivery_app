# Baseline: BDD, TDD e Engenharia de Software no Delivery App

Este documento estabelece as diretrizes definitivas e melhores práticas para a confecção, manutenção e automação de arquivos `.feature` no projeto Delivery App, assegurando a qualidade e a rastreabilidade dos requisitos.

## 1. Princípios do BDD (Behavior-Driven Development)

O BDD visa aproximar a linguagem de negócio da linguagem técnica. No Delivery App, a principal ferramenta para isso é o Gherkin.

### 1.1. Estrutura do Arquivo `.feature`
- **Nomeação:** O arquivo deve descrever a funcionalidade de forma sucinta, usando `snake_case` ou `kebab-case` (ex: `cadastro_restaurante.feature`).
- **Idioma:** Todos os arquivos `.feature` devem ser escritos em português (`# language: pt`).
- **Contexto:** Use a palavra-chave `Contexto:` (`Background:`) para passos que se repetem em todos os cenários daquela feature, evitando redundância.

### 1.2. Escrita de Cenários
- **Clareza e Objetividade:** Cada cenário deve focar em um único comportamento ou regra de negócio.
- **Fórmula Given-When-Then (Dado-Quando-Então):**
  - **Dado (Given):** Estabelece o estado inicial (pré-condições).
  - **Quando (When):** Descreve a ação principal do usuário ou evento do sistema.
  - **Então (Then):** Descreve o resultado esperado (pós-condições), que deve ser testável e verificável.
  - **E / Mas (And / But):** Utilizados para adicionar mais passos de estado, ação ou resultado, mantendo o cenário legível.

**Exemplo Prático:**
```gherkin
# language: pt
Funcionalidade: Cancelamento de Pedido
  Como um cliente
  Eu quero poder cancelar meu pedido
  Para não receber um item que não desejo mais

  Cenário: Cancelamento antes do preparo
    Dado que o pedido "123" está no status "Aguardando Confirmação"
    Quando eu solicito o cancelamento do pedido "123"
    Então o pedido "123" deve mudar para o status "Cancelado"
    E eu devo receber uma notificação de sucesso
```

## 2. Princípios do TDD (Test-Driven Development)

O TDD guia o design de software através de testes. A integração TDD + BDD (muitas vezes chamada de ATDD) funciona da seguinte maneira no projeto:

1. **Red:** Escreva o cenário Gherkin (BDD) e a automação do passo (Step Definition). O teste deve falhar pois a funcionalidade não existe.
2. **Green:** Implemente o código da aplicação (Frontend/Backend) apenas o suficiente para fazer o teste passar.
3. **Refactor:** Melhore o código escrito (design patterns, clean code) mantendo o teste passando.

## 3. Diretrizes de Engenharia de Software e Manutenção

### 3.1. Organização de Diretórios
- Os arquivos `.feature` devem ser alocados dentro de `features/<dominio>/`.
- O código de automação dos passos (Step Definitions) deve espelhar essa estrutura, ex: `tests/steps/<dominio>/`.

### 3.2. Granularidade e Reusabilidade
- **Evite passos muito técnicos:** Não acople a UI no BDD. Em vez de "Dado que eu clico no botão com id 'btn-submit'", prefira "Quando eu envio o formulário de cadastro".
- **Reaproveite Steps:** Escreva steps genéricos parametrizados para maximizar o reúso (ex: `Dado que o usuário "{string}" está logado`).

### 3.3. Versionamento e Revisão
- Os arquivos `.feature` são documentação viva. Qualquer alteração em regra de negócio deve obrigatoriamente iniciar pela atualização da feature.
- Pull Requests devem conter as features e seus respectivos testes passando.

## 4. Padrões de Aceite

Um artefato só é considerado "Pronto" (Definition of Done) se:
1. Possui arquivo `.feature` documentado.
2. Os cenários cobrem caminhos felizes e de erro (Edge Cases).
3. A automação dos cenários passa com sucesso no pipeline de CI/CD.
4. Segue estritamente as regras de negócio definidas na Tabela de Responsabilidade.