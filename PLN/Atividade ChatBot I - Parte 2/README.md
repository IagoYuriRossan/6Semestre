# Atividade ChatBot I - Parte 2

Iago Yuri Rossan — Fatec Votorantim — 6º semestre de DSM — PLN.

Base: https://github.com/jylaila/chat, copiada de `C:\chat`.

## Executar e testar manualmente

É necessário ter Node.js e npm instalados. Abra dois terminais PowerShell.

### Chatbot de regras

```powershell
cd "C:\6Semestre\PLN\Atividade ChatBot I - Parte 2\RulesBased\chatbot-node"
npm install
node server.js
```

Abra http://localhost:3000 no navegador e envie:

- `Qual o horário?` → segunda a sexta, das 8h às 18h.
- `Qual a localização?` → Centro de Votorantim.
- `Tem promoção?` → 10% de desconto.
- `Preciso de login` → orientação sobre senha.

### Chatbot de PLN

No segundo terminal:

```powershell
cd "C:\6Semestre\PLN\Atividade ChatBot I - Parte 2\PLNBased\chatbot-pln"
npm install
node server.js
```

Abra http://localhost:3001 no navegador e envie:

- `qual o preço do plano` → intenção `preco`.
- `preciso de ajuda agora` → intenção `ajuda`.
- `quero cancelar minha assinatura` → intenção `cancelamento`.
- `oi` → intenção `saudacao`.

Mantenha o terminal aberto enquanto testa. Para parar, pressione Ctrl+C. Após alterar o código, pare e execute `node server.js` novamente. No PLN, isso também retreina o classificador. `npm install` é necessário na primeira execução ou se as dependências mudarem. Também é possível iniciar com `npm start`.

Abra a página pelo endereço localhost, não diretamente pelo arquivo index.html. Caso apareça EADDRINUSE, a porta já está ocupada: encerre o servidor anterior antes de iniciar outro.

## Estrutura

Cada chatbot mantém `server.js`, `index.html`, `package.json` e `package-lock.json`, como a base. A pasta `node_modules` contém as bibliotecas instaladas pelo npm e não deve ser enviada ao GitHub. Não há arquivos de testes nem pasta de evidências; as capturas dos testes já executados permanecem incorporadas ao relatório em Word.

## Alterações

Regras de horário, localização e promoções usando if/else e includes. PLN com as novas intenções preço, ajuda e cancelamento: 17 exemplos e seis intenções, treinados no próprio server.js. Os dados são fictícios e nenhuma operação comercial é realizada. As regras dependem de palavras previstas, e o classificador pode errar em frases fora dos exemplos.
