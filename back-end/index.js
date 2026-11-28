const express = require("express")
const app = express()
app.use(express.json())

let impressoras = [
    {
        impressora: "Creative Sla 3000",
        material: "FODA"
    }
]

// GET: CONSULTA.
app.get("/hope", (req, res)=>{
    res.send(impressoras)
})

// POST: CADASTRO.
app.post("/hope", (req, res) => {
    const impressoraPost = req.body.impressora
    const materialPost = req.body.material

    // MONTAGEM DE OBJETO NOVO
    const impressoraNew = {impressora: impressoraPost, material: materialPost}

    // Adiciona o novo objeto no final da lista
    impressoras.push(impressoraNew)
    res.json(impressoras)
})

app.listen(3000, ()=>console.log("RODANDO!"))