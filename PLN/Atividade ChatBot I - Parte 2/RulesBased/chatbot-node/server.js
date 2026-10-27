const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"));

app.post("/chat", (req, res) => {
  if (typeof req.body?.message !== "string" || !req.body.message.trim()) {
    return res.status(400).json({ error: "Digite uma mensagem." });
  }
  const message = req.body.message.toLowerCase();
  let response = "Desculpe, não entendi sua pergunta.";

  if (message.includes("login")) {
    response = "Você pode redefinir sua senha clicando em 'Esqueci minha senha'.";
  } else if (message.includes("plano")) {
    response = "Temos planos Básico e Premium. Qual você gostaria de saber mais?";
  } else if (message.includes("atendente")) {
    response = "O atendimento com uma pessoa é apenas simulado neste exemplo.";
  } else if (message.includes("horário") || message.includes("horario")) {
    response = "Nosso atendimento é de segunda a sexta, das 8h às 18h.";
  } else if (message.includes("localização") || message.includes("localizacao") || message.includes("endereço") || message.includes("endereco")) {
    response = "Nossa loja fica no Centro de Votorantim.";
  } else if (message.includes("promoção") || message.includes("promocao") || message.includes("promoções") || message.includes("promocoes")) {
    response = "No momento, temos 10% de desconto para novos clientes.";
  }

  res.json({ reply: response });
});

app.listen(3000, () => console.log("Chatbot rodando em http://localhost:3000"));
