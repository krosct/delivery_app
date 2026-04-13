# 🎨 ADR arc42 — Design System para App de Delivery

| Status | Accepted |
| --- | --- |
| Date | 2026-04-13 |
| Author | Matheus Borges |
| Context | Padronização de UI/UX para app de delivery |
| Decision Type | Arquitetural / Design System |

---

# 1. Contexto

O sistema de delivery será desenvolvido por múltiplos integrantes e potencialmente com apoio de agentes de AI.

Sem um padrão claro de design:
- Interfaces ficam inconsistentes
- UX se torna confusa
- A velocidade de desenvolvimento cai
- A qualidade visual varia entre features

---

# 2. Problema

Como garantir que:

- Todas as telas sigam um padrão consistente
- Qualquer dev (ou AI) consiga criar telas de alta qualidade
- O sistema mantenha coerência visual e funcional
- O design seja simples (nível projeto acadêmico), mas profissional

---

# 3. Decisão

Adotar um **Design System simplificado e rígido**, inspirado em padrões de apps reais de delivery (ex: iFood, Uber Eats), baseado em:

- Hierarquia visual forte
- Cores funcionais (status-driven)
- Componentização consistente
- UX orientado a ação rápida

---

# 4. Princípios de Design

## 4.1 Clareza > Estética

- Interface deve ser óbvia
- Usuário deve saber o que fazer em menos de 3 segundos

---

## 4.2 Ação Principal Sempre Destacada

- Cada tela deve ter **uma ação dominante**
- Exemplo:
  - "Aceitar pedido"
  - "Atribuir entregador"

---

## 4.3 Feedback Imediato

- Toda ação gera resposta visual:
  - loading
  - sucesso
  - erro

---

## 4.4 Mobile-first

- Layout deve funcionar em telas pequenas
- Desktop é adaptação, não prioridade

---

## 4.5 Consistência > Criatividade

- Não inventar novos padrões por feature
- Reutilizar componentes sempre

---

# 5. Paleta de Cores

## 5.1 Cores Primárias

| Uso | Cor | Código |
| --- | --- | --- |
| Primary Action | Verde | #22C55E |
| Secondary | Azul | #3B82F6 |
| Background | Branco | #FFFFFF |
| Surface | Cinza claro | #F9FAFB |

---

## 5.2 Cores de Status

| Status | Cor | Uso |
| --- | --- | --- |
| Disponível | Verde | Entregador livre |
| Ocupado | Amarelo | Em entrega |
| Offline | Cinza | Indisponível |
| Erro | Vermelho | Falhas |

---

## 5.3 Regras de Uso

- Nunca usar mais de **3 cores fortes na mesma tela**
- Verde sempre representa **ação positiva**
- Vermelho apenas para erro

---

# 6. Tipografia

## 6.1 Fonte

- Padrão: `Inter` ou `System UI`

---

## 6.2 Hierarquia

| Elemento | Tamanho | Peso |
| --- | --- | --- |
| Título | 20-24px | Bold |
| Subtítulo | 16-18px | Medium |
| Texto | 14-16px | Regular |
| Label | 12px | Medium |

---

## 6.3 Regras

- Máximo de 3 tamanhos por tela
- Evitar textos longos
- Priorizar leitura rápida

---

# 7. Componentes Base

## 7.1 Botões

### Tipos

#### Primary Button

- Cor: Verde
- Uso: ação principal

```css
background: #22C55E;
color: white;
border-radius: 8px;
padding: 12px;
```

Secondary Button
Cor: Azul
Uso: ações secundárias
Disabled Button
Cor: Cinza
Sem interação
7.2 Cards
Usados para:
pedidos
entregadores
Estrutura
título
subtítulo
status
ação
7.3 Inputs
borda leve
foco com cor azul
erro com borda vermelha
7.4 Badges
Usados para status:
verde → disponível
amarelo → ocupado
cinza → offline
8. Layout Padrão
8.1 Estrutura Base
Header
↓
Content
↓
Primary Action (fixa ou no final)
8.2 Lista (Pattern principal)
Usado em:
pedidos
entregadores
Cada item:
[Nome]
[Detalhes]
[Status Badge]
[Ação]
9. Fluxos Padrão
9.1 Fluxo: Atribuir Entregador
Usuário abre pedido
Sistema sugere entregadores
Usuário seleciona
Confirma ação
Feedback imediato
9.2 Fluxo: Cadastro de Entregador
Preencher dados
Validar campos
Salvar
Feedback de sucesso
9.3 Fluxo: Reatribuição
Entregador falha
Sistema notifica
Pedido volta para lista
Nova atribuição
10. Estados de Interface
10.1 Loading
Skeleton ou spinner
Nunca tela vazia
10.2 Empty State
Mensagem clara:
"Nenhum entregador disponível"
10.3 Error State
Mensagem + ação:
"Tentar novamente"
11. Regras Estritas
11.1 NÃO FAZER
❌ Criar botão com cor aleatória
❌ Misturar padrões de layout
❌ Criar fluxo sem feedback
❌ Usar mais de 2 ações primárias
11.2 SEMPRE FAZER
✅ Usar componentes padrão
✅ Manter hierarquia visual
✅ Garantir feedback imediato
✅ Seguir cores de status
12. Integração com AI
12.1 Regras para agentes de AI
Ao gerar UI:
Sempre usar:
Primary Button verde
Cards para listas
Badge para status
12.2 Prompt interno padrão
Toda geração de UI deve considerar:
Mobile-first
Ação principal destacada
Feedback visual
Layout simples
13. Trade-offs
Escolha	Benefício	Custo
Simplicidade	Fácil implementação	Menos flexibilidade
Poucas cores	Consistência	Menos liberdade visual
Componentização	Reuso	Setup inicial maior
14. Consequências
Positivas
Alta consistência
Fácil onboarding
Melhor UX
Compatível com AI
Negativas
Menos liberdade criativa
Pode parecer “simples demais”
15. Conclusão
Este design system não busca ser complexo.
Ele busca ser:
Claro, consistente e rápido de implementar
E principalmente:
Ser fácil o suficiente para qualquer dev (ou AI) seguir sem errar