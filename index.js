const { Client, Events, GatewayIntentBits } = require('discord.js');
const dotenv = require('dotenv');

try {
    dotenv.config({ path: '.env' });
}
catch (error) {
    console.err('No se pudo leer el fichero .env');
    process.exit(1);
}
const token = process.env.TOKEN;

const client = new Client({ intents: GatewayIntentBits.Guilds });

client.once(Events.ClientReady, c => {
    console.log(`Listo! Usuario: ${c.user.tag}`);
});

client.login(token);