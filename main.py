import random, requests
from bs4 import BeautifulSoup
from transformers import T5Tokenizer, T5ForConditionalGeneration

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)

    return password

# Inisialisasi model T5
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Fungsi untuk mengambil teks dari URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Ambil semua teks dari tag <p>
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text if text else "Tidak ada teks yang ditemukan di halaman ini."
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# Fungsi untuk meringkas teks
def summarize_text(text):
    try:
        # Batasi panjang input untuk menghindari kelebihan kapasitas model
        max_input_length = 512
        input_text = text[:max_input_length]

        # Tokenisasi dan rangkum teks
        inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=max_input_length, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        return f"Gagal meringkas teks: {e}"



