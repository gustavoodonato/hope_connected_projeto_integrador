const protocolo = 'http://'
const baseURL = 'localhost:3000'
const nomesEndpoint = '/hope'

async function getImpressoras() {
    const URLCompleta = `${protocolo}${baseURL}${nomesEndpoint}`
    const impressoras = (await axios.get(URLCompleta)).data

    let tabela = document.querySelector('.impressoras')
    let corpoTabela = tabela.getElementsByTagName('tbody')[0]
    for (let impressora of impressoras) {
        //insertRow(0) para adicionar sempre na primeira linha
        //se quiser adicionar na última, chame insertRow sem argumentos
        let linha = corpoTabela.insertRow()

        let cellImpressora = linha.insertCell(0)
        let cellMaterial = linha.insertCell(1)
        
        cellImpressora.innerHTML = impressora.impressora
        cellMaterial.innerHTML = impressora.material
    }
}

async function buscaDados() {
    try{
        const response = await fetch('http://127.0.0');
        const data = await response.json()
        console.log(data.mensagem)
    } catch (erro) {
        console.error('Erro de Requisição: ', erro)
    }
}

async function newImpressora(){
    //constrói a URL completa
    const URLCompleta = `${protocolo}${baseURL}${nomesEndpoint}`
    //pega os inputs que contém os valores que o usuário digitou
    let impressoraInput = document.querySelector('#impressoraInput')
    let materialInput = document.querySelector('#materialInput')
    //pega os valores digitados pelo usuário
    let impressora = impressoraInput.value
    let material = materialInput.value
    if (impressora && material){
        //limpa os campos que o usuário digitou
        impressoraInput.value = ""
        materialInput.value = ""
        //envia os dados ao servidor (back end)
        const impressoras = (await axios.post(URLCompleta, {impressora, material})).data
        //limpa a tabela para preenchê-la com a coleção nova, atualizada
        let tabela = document.querySelector('.impressoras')
        let corpoTabela = tabela.getElementsByTagName('tbody')[0]
        corpoTabela.innerHTML = ""

        for (let impressora of impressoras) {
            let linha = corpoTabela.insertRow()
            
            let cellImpressora = linha.insertCell(0)
            let cellMaterial = linha.insertCell(1)

            cellImpressora.innerHTML = impressora.impressora
            cellMaterial.innerHTML = impressora.material
        }
    }
    else{
        let alert = document.querySelector('.alert')
        alert.classList.add('show')
        alert.classList.remove('d-none')
        setTimeout(() => {
            alert.classList.remove('show')
            alert.classList.add('d-none')
        }, 2000)
    }
}