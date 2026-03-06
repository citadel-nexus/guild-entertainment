import  GuildClient  from '@citadel-guilds/sdk';

const guild = new GuildClient({
  name: 'entertainment',
  natsPrefix: 'citadel.ent',
  port: 8400,
});

guild.start();
