const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"));
const natural = require("natural");
const classifier = new natural.BayesClassifier();

// Intenções do projeto original.
classifier.addDocument("oi", "saudacao");
classifier.addDocument("olá", "saudacao");
classifier.addDocument("bom dia", "saudacao");
classifier.addDocument("quero saber meu pedido", "pedido_status");
classifier.addDocument("meu pedido chegou", "pedido_status");
classifier.addDocument("acompanhar pedido", "pedido_status");
classifier.addDocument("obrigado", "agradecimento");
classifier.addDocument("valeu", "agradecimento");

// Novas intenções da atividade.
classifier.addDocument("qual o preço", "preco");
classifier.addDocument("quanto custa", "preco");
classifier.addDocument("qual o valor do plano", "preco");
classifier.addDocument("preciso de ajuda", "ajuda");
classifier.addDocument("quero suporte", "ajuda");
classifier.addDocument("tenho uma dúvida", "ajuda");
classifier.addDocument("quero cancelar", "cancelamento");
classifier.addDocument("cancelar minha assinatura", "cancelamento");
classifier.addDocument("solicitar cancelamento", "cancelamento");

// Ao iniciar novamente o servidor, treina com todos os exemplos.
classifier.train();

app.post("/chat", (req, res) => {
  if (typeof req.body?.message !== "string" || !req.body.message.trim()) {
    return res.status(400).json({ error: "Digite uma mensagem." });
  }
  const message = req.body.message.toLowerCase();
  const intent = classifier.classify(message);
  let reply = "Desculpe, não entendi.";

  switch (intent) {
    case "saudacao":
      reply = "Olá! Em que posso te ajudar hoje?";
      break;
    case "pedido_status":
      reply = "Para consultar seu pedido, informe o número ou e-mail da compra.";
      break;
    case "agradecimento":
      reply = "De nada! Estou sempre à disposição.";
      break;
    case "preco":
      reply = "O plano Básico custa R$ 29,90 por mês e o Premium custa R$ 59,90.";
      break;
    case "ajuda":
      reply = "Claro! Descreva sua dúvida para que eu possa ajudar.";
      break;
    case "cancelamento":
      reply = "Para solicitar o cancelamento, entre em contato com o atendimento.";
      break;
  }

  res.json({ reply, intent });
});

app.listen(3001, () => console.log("Chatbot rodando em http://localhost:3001"));
