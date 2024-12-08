import discord, random, os, requests
from discord.ext import commands
from main import gen_pass, fetch_text_from_url, summarize_text
from bs4 import BeautifulSoup
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Membaca token dari file token.txt
with open("token.txt", "r") as f:
    token = f.read()

sampah = {
    'kertas' : 'anorganik',
    'plastik' : 'anorganik',
    'kardus' : 'anorganik',
    'sisa_makanan': 'organik',
    'daun_kering' : 'organik',
    'kulit_buah' : 'organik',
    'baterai' : 'B3',
    'oli' : 'B3',
    'deterjen' : 'B3'
} 

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Command untuk bot
@bot.command()
async def ringkas_url(ctx, url: str):
    await ctx.send("Mengambil teks dari website, mohon tunggu...")
    # Ambil teks dari URL
    text = fetch_text_from_url(url)
    
    if text.startswith("Terjadi kesalahan") or text.startswith("Tidak ada teks"):
        await ctx.send(text)
        return
    
    await ctx.send("Meringkas teks, mohon tunggu...")
    # Ringkas teks
    summary = summarize_text(text)
    await ctx.send(f"Ringkasan:\n{summary}")

@bot.command()
async def ringkas_teks(ctx, *, text: str):
    # Konfirmasi penerimaan teks
    await ctx.send("Teks diterima, sedang meringkas...")
    # Meringkas teks
    summary = summarize_text(text)
    # Mengirimkan hasil ringkasan
    await ctx.send(f"Ringkasan:\n{summary}")

@bot.event
async def on_ready():
    print(f'{bot.user} telah online!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Halo! Aku bot yang bernama {bot.user}!')

@bot.command()
async def repeat(ctx, times: 3, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def passw(ctx, panjang = 5):
    await ctx.send(gen_pass(panjang))

@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

animal = {
    'animal1.jpg': 5, #common
    'animal2.jpg': 2, #uncommon
    'animal3.jpg': 1  #rare
}

def get_weighted_random_meme(animal):
    weighted_memes = []
    for animal, rarity in animal.items():
        weighted_memes.extend([animal] * rarity)
    return random.choice(weighted_memes)

@bot.command()
async def anim(ctx):
    anim_name = get_weighted_random_meme(animal)
    with open(f'animals/{anim_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command("sampah")
async def jenis_sampah(ctx, item:str):
    if item.lower() in sampah:
        await ctx.send(f"{item.capitalize()} merupakan jenis sampah: {sampah[item.lower()]}")
    else:
        await ctx.send(f"Maaf, {item.capitalize()} tidak tercatat di dalam daftar")

@bot.command()
async def organik(ctx):
    await ctx.send(f'Sampah jenis organik dapat diolah menjadi pupuk kompos, makanan hewan, eco enzyme, dan biogas')

@bot.command()
async def anorganik(ctx):
    await ctx.send(f'Sampah jenis anorganik dapat diolah menjadi kerajinan tangan, bahan daur ulang, eco brick')

@bot.command()
async def B3(ctx):
    await ctx.send(f'Sampah jenis B3 dapat diolah dengan melakukan pemilahan, membuangnya ke pembuangan khusus')

bot.run(token)