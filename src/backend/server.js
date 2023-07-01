const express = require("express")
const path = require("path")
const cors = require("cors")
const bodyParser = require("body-parser")
const axios = require("axios")

const app = express()
// app.use('/public', express.static(path.join(__dirname,'static')));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json())
app.use(cors())

app.get('/', (req, res) => {
    const options = {
        method: 'POST',
        url: 'http://127.0.0.1:5000/search',
        params: { query: 'Free' , password: 'NoobScience'},
    };
    axios.request(options).then(function (response) {
        console.log(response);
        res.send(response.data);
    }).catch(function (error) {
        console.error(error);
    });
})

console.log("Listening")
app.listen("3000")