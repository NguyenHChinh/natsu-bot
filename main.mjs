import DiscordJS, { Intents } from 'discord.js'
import { createRequire } from "module";
import { userInfo } from 'os';
const require = createRequire(import.meta.url);
const { prefix, token } = require("./config.json");

const client = new DiscordJS.Client({
    intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES],
})

// Ready message when bot is online
client.on('ready',  () => {
    console.log('The client is ready!');
});

// Ping function
client.on('messageCreate', (message) => {
    if (message.content == 'ping') {
        message.reply({
            content: 'pong',
        })
    }
})

client.login(token);