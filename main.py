import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import Dispatcher, filters
from decouple import config
import os, platform
from datetime import datetime,timezone,timedelta
import json

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
API_TOKEN = config('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

autorizados = [1021953062,846901510]

def ping(host):
    if  platform.system().lower()=="windows":
        ping_str = "-n 5"
    else:
        ping_str = "-c 5"
    resposta = os.system("ping " + ping_str + " " + host + " >>c:\\Users\\TI\\Desktop\\Cordeiro\\Rod\\dev\\projeto\\bot_akta\\ping.txt")
    return host,resposta == 0

def gravar(dado):
    data = datetime.now().astimezone(timezone(timedelta(hours=-3)))
    dia = f"{data.year}-{str(data.month).zfill(2)}-{str(data.day).zfill(2)}"
    hora = f"{str(data.hour).zfill(2)}:{str(data.minute).zfill(2)}"
    with open('horario.json','r') as f:
        arquivo = json.load(f)
        try:
            info = arquivo[dia]
            info[dado] = hora
        except:
            arquivo[dia] = {}
            info = arquivo[dia]
            info[dado] = hora
        file = open('horario.json','w')
        file.write(json.dumps(arquivo))
        return f"{dado} em {dia} ás {hora}"

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Akta On!\nEste robo é para informações da Akta. Comandos:\n - /con: retorna testes de pings de alguns ips chave;\n - /ping - pinga o ip específicado e retorna o resultado (/ping 192.168.30.1 );\n - /auth solicita autorização para executar os comandos")

@dp.message_handler(commands=['dados'])
async def infos(message: types.Message):
    await message.reply(message)
@dp.message_handler(commands=['teste'])
async def teste(message: types.Message):
    await bot.send_poll(1016560417,'Qual a boa?',['Supimpa','Tranquilo','Só desgraça','Irineu'],disable_notification=None,reply_to_message_id='962')


@dp.message_handler(commands=['con'])
async def test_con(message: types.Message):
    ips = ['192.168.30.1','192.168.30.250','192.168.30.10', '192.168.33.254','192.168.33.250','10.1.30.11','10.1.30.12','10.1.30.13','10.1.30.14','10.1.30.15']
    if message.chat.id in autorizados:
        [await message.reply(ping(ip)) for ip in ips]
        os.remove("ping.txt")
        if message.chat.id != 1021953062:
            await bot.send_message(1021953062,"O usuário {} executou o comando /con".format(message.chat.first_name))
    else:
        await message.reply("Ta tentando me invadir? Me respeita!")
        info = "Execução do comando /con!!\nUsuario: {} \nNome: {} {} \n".format(message.chat.username,message.chat.first_name,message.chat.last_name)
        await bot.send_message(1021953062,info)

@dp.message_handler(commands=['ping'])
async def test_con(message: types.Message):
    if message.chat.id in autorizados:
        ip = message.text[6:]
        await message.reply(ping(ip))
        file = open("ping.txt","r").read()
        await message.reply(file)
        os.remove("ping.txt")
        if message.chat.id != 1021953062:
            await bot.send_message(1021953062,"O usuário {} executou o comando {}".format(message.chat.first_name,message.text))
    else:
        await message.reply("Ta tentando me invadir? Me respeita!")
        info = "Execução do comando /ping!!\nUsuario: {} \nNome: {} {} \n".format(message.chat.username,message.chat.first_name,message.chat.last_name)
        await bot.send_message(1021953062,info)

@dp.message_handler(commands=['auth'])
async def auth(message: types.Message):
    file = open("c:\\Users\\TI\\Desktop\\Cordeiro\\Rod\\dev\\projeto\\bot_akta\\auth.txt","w")
    info = "ID: {} \nUSUARIO: {} \nNOME: {} \nSOBRENOME: {} \nCONVERSA: {}".format(message.chat.id,message.chat.username,message.chat.first_name,message.chat.last_name,message.chat.type)
    file.write(info)
    file.close()
    await message.reply(info+"\nAguarde autorização.")
    await bot.send_message(1021953062,info + "\n \n Aguardando autorização. /autorizado_{}".format(message.chat.id))

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['autorizado_([a-zA-Z0-9]*)']))
async def autorizado(message: types.Message, regexp_command):
    await bot.send_message(regexp_command.group(1),"Você foi autorizado a usar os comandos do @aktatibot.")


@dp.message_handler(commands=['entrada'])
async def entrada(message: types.Message):
    if message.chat.id == 1021953062:
        gravar('entrada')
    await message.reply("Gravada.")

@dp.message_handler(commands=['almoco'])
async def entrada(message: types.Message):
    if message.chat.id == 1021953062:
        gravar('almoco')
    await message.reply("Gravado.")

@dp.message_handler(commands=['retorno'])
async def entrada(message: types.Message):
    if message.chat.id == 1021953062:
        gravar('retorno')
    await message.reply("Gravado.")

@dp.message_handler(commands=['saida'])
async def entrada(message: types.Message):
    if message.chat.id == 1021953062:
        gravar('saida')
    await message.reply("Gravada.")

if __name__ == '__main__':
    print("""
     ___       __  ___ .___________.     ___         .___________.     __     .______     ______   .___________.
    /   \     |  |/  / |           |    /   \        |           |    |  |    |   _  \   /  __  \  |           |
   /  ^  \    |  '  /  `---|  |----`   /  ^  \       `---|  |----`    |  |    |  |_)  | |  |  |  | `---|  |----`
  /  /_\  \   |    <       |  |       /  /_\  \          |  |         |  |    |   _  <  |  |  |  |     |  |
 /  _____  \  |  .  \      |  |      /  _____  \         |  |      __ |  |    |  |_)  | |  `--'  |     |  |
/__/     \__\ |__|\__\     |__|     /__/     \__\        |__|     (__)|__|    |______/   \______/      |__|
""")
    executor.start_polling(dp, skip_updates=True)
