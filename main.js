const Discord = require('discord.js');
const { prefix, token } = require("./config.json");
const client = new Discord.Client({ intents: [] })

client.on('ready',  () => {
    console.log('The client is ready!');
});

client.login(token);