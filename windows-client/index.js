const axios = require('axios');
const readline = require("readline-sync");

console.log(" ")
async function main() {
    while (true) {
        let msg = readline.question("You: ");

        let response = await axios.post('http://localhost:5005/webhooks/rest/webhook', {
            sender: 'Tarun',
            message: msg
        });

        console.log("Bestie:", response.data[0].text)
        console.log(" ")
    }
}

main();