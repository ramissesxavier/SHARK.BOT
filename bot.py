import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

REACTION_EMOJI = '✅'
ROLE_NAME = 'Membro 🦈'
CANAL_VERIFICACAO_ID = 1455353717233815562

reaction_message_id = None
reaction_channel_id = None

CANAL_BOAS_VINDAS = 1408305295045820500
CANAL_ADEUS = 1455285555054247966

GIF_BOAS_VINDAS = 'https://i.imgur.com/hb3iXz3.gif'

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!')
    global reaction_message_id, reaction_channel_id
    channel = bot.get_channel(CANAL_VERIFICACAO_ID)
    if channel:
        embed = discord.Embed(title='**LIBERAR ACESSO**', color=0xc91f1f)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1455396837904224439/1457442192842035310/Lieve2.gif')
        embed.set_footer(text='🩸 Clique na reação ✅ abaixo para verificar 🩸')
        embed.timestamp = discord.utils.utcnow()
        message = await channel.send(content='||@everyone||', embed=embed)
        await message.add_reaction(REACTION_EMOJI)
        reaction_message_id = message.id
        reaction_channel_id = channel.id
        print('✅ Mensagem de verificação ativa!')

@bot.command(name='setupcargos')
@commands.has_permissions(administrator=True)
async def setup_cargos(ctx):
    global reaction_message_id, reaction_channel_id
    if ctx.channel.id != CANAL_VERIFICACAO_ID:
        await ctx.send(f'❌ Este comando só funciona no canal <#{CANAL_VERIFICACAO_ID}>!')
        return
    embed = discord.Embed(title='**LIBERAR ACESSO**', color=0xc91f1f)
    embed.set_image(url='https://cdn.discordapp.com/attachments/1455396837904224439/1457442192842035310/Lieve2.gif')
    embed.set_footer(text='🩸 Clique na reação ✅ abaixo para verificar 🩸')
    message = await ctx.send(content='||@everyone||', embed=embed)
    await message.add_reaction(REACTION_EMOJI)
    reaction_message_id = message.id
    reaction_channel_id = ctx.channel.id
    await ctx.send('✅ Sistema configurado!')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id: return
    if payload.message_id != reaction_message_id: return
    if str(payload.emoji) != REACTION_EMOJI: return
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)
    if role and member:
        try:
            await member.add_roles(role)
            dm_embed = discord.Embed(title='🦈 Verificação Concluída!', description=f'**BEM-VINDO AO SERVIDOR, {member.name}!**', color=0xc91f1f)
            dm_embed.set_image(url=GIF_BOAS_VINDAS)
            await member.send(embed=dm_embed)
        except Exception as e:
            print(f'Erro ao dar cargo: {e}')

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != reaction_message_id: return
    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = guild.get_member(payload.user_id)
    if role and member:
        try:
            await member.remove_roles(role)
        except: pass

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(CANAL_BOAS_VINDAS)
    if canal:
        embed = discord.Embed(title='Bem-vindo(a)!', description=f'Olá {member.mention}, espero que você se divirta no nosso servidor!', color=0xc91f1f)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=GIF_BOAS_VINDAS)
        embed.set_footer(text=f'ID do usuário: {member.id}')
        await canal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    canal = bot.get_channel(CANAL_ADEUS)
    if canal:
        embed = discord.Embed(title=f'Adeus {member.name}', color=0x808080)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1455396837904224439/1456025826515619840/Adeus.gif')
        await canal.send(embed=embed)

if __name__ == '__main__':
    TOKEN = os.environ.get('TOKEN')
    bot.run(TOKEN)
