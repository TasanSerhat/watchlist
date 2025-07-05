import sqlite3

def diziEkle():
    
    name = input("Dizi adı: ").strip()
    print("""\n
      Korku
      Aksiyon
      Animasyon
      Komedi
      Bilim Kurgu
      Gerilim
      Dram
      Aşk""")
    category = input("Dizi Kategorisi: ").strip()
    
    try:
        season = int(input("Kaçıncı sezondasın?: "))
        episode = int(input("Kaçıncı bölümdesin?: "))
    except ValueError:
        print("❌ Sezon ve bölüm sayısal olmalıdır!")
        return

    note = input("Not (isteğe bağlı): ").strip()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO series (name, category, season, episode, note)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, season, episode, note))

    conn.commit()
    conn.close()

    print("✅ Dizi başarıyla eklendi!")
    
def diziListeleTum():
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, season, episode, note FROM series")
    diziler = cursor.fetchall()
    
    if not diziler:
        print("Henüz dizi eklenmemiş.")
    else:
        print("\n---- Dizi Listesi ----")
        for dizi in diziler:
            ad, kategori, sezon, bolum, not_ = dizi
            not_text = not_ if not_ else "-"
            print(f"📺 {ad} | Kategori: {kategori} | {sezon}. Sezon {bolum}. Bölüm | Not: {not_text}")
    
    conn.close()
    
def diziArama():
    
    aranan = input("Aramak istediğiniz dizinin adını giriniz: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, season, episode, note FROM series WHERE LOWER(name) LIKE ?", (f"%{aranan}%",))
    diziler = cursor.fetchall()
    
    if not diziler:
        print("🔍 Uygun dizi bulunamadı.")
    else:
        print("\n--- Arama Sonuçları ---")
        for dizi in diziler:
            ad, kategori, sezon, bolum, not_ = dizi
            not_text = not_ if not_ else "-"
            print(f"📺 {ad} | Kategori: {kategori} | {sezon}. Sezon {bolum}. Bölüm | Not: {not_text}")

    conn.close()
    
def diziListele():
    while True:
    
        print("\nDizi Listeleme Menüsü: ")
        print("1-Tüm dizileri listele")
        print("2-Dizi adıyla arama")
        print("3-Geri dön")
        
        secim = input("\nSeçiminiz (1-3): ")
        
        if secim == "1":
            diziListeleTum()
            break
        elif secim == "2":
            diziArama()
            break
        elif secim == "3":
            return
        else:
            print("❌ Hatalı seçim yaptınız lütfen tekrar deneyin.")
            
def diziGuncelle():
    
    aranan = input("Güncellemek istediğiniz dizinin adını girin: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, category, season, episode, note FROM series WHERE LOWER(name) LIKE ?", (f"%{aranan}%",))
    diziler = cursor.fetchall()
    
    if not diziler:
        print("Dizi bulunamadı.")
        conn.close()
        return

    print("\n--- Eşleşen Diziler ---")
    for dizi in diziler:
        id_, ad, kategori, sezon, bolum, not_ = dizi
        not_text = not_ if not_ else "-"
        print(f"[{id_}] {ad} | Kategori: {kategori} | {sezon}. Sezon {bolum}. Bölüm | Not: {not_text}")
        
    try:
        secilen_id = int(input("\nGüncellemek istediğiniz dizinin ID'sini girin: "))
    except ValueError:
        print("Geçersiz giriş.")
        conn.close()
        return
    
    cursor.execute("SELECT name, category, season, episode, note FROM series WHERE id = ?", (secilen_id,))
    sonuc = cursor.fetchone()

    if not sonuc:
        print("Belirtilen ID'ye ait dizi bulunamadı.")
        conn.close()
        return

    eski_ad, eski_kategori, eski_sezon, eski_bolum, eski_not = sonuc

    print("\n--- Alanları güncelleyin (boş bırakırsanız eski değer korunur) ---")
    yeni_ad = input(f"Yeni ad ({eski_ad}): ").strip()
    yeni_kategori = input(f"Yeni kategori ({eski_kategori}): ").strip()

    try:
        yeni_sezon_input = input(f"Yeni sezon ({eski_sezon}): ").strip()
        yeni_sezon = int(yeni_sezon_input) if yeni_sezon_input else eski_sezon

        yeni_bolum_input = input(f"Yeni bölüm ({eski_bolum}): ").strip()
        yeni_bolum = int(yeni_bolum_input) if yeni_bolum_input else eski_bolum
    except ValueError:
        print("Sezon ve bölüm sayısal olmalı.")
        conn.close()
        return

    yeni_not = input(f"Yeni not ({eski_not if eski_not else '-' }): ").strip()

    if not yeni_ad:
        yeni_ad = eski_ad
    if not yeni_kategori:
        yeni_kategori = eski_kategori
    if not yeni_not:
        yeni_not = eski_not

    cursor.execute("""
        UPDATE series
        SET name = ?, category = ?, season = ?, episode = ?, note = ?
        WHERE id = ?
    """, (yeni_ad, yeni_kategori, yeni_sezon, yeni_bolum, yeni_not, secilen_id))

    conn.commit()
    conn.close()

    print("✅ Dizi başarıyla güncellendi.")
    
def diziSilme():
    
    aranan = input("Silmek istediğiniz dizi adını girin: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, category, season, episode, note
        FROM series
        WHERE LOWER(name) LIKE ?
    """, (f"%{aranan}%",))

    diziler = cursor.fetchall()

    if not diziler:
        print("Hiçbir eşleşen dizi bulunamadı.")
        conn.close()
        return

    print("\n--- Eşleşen Diziler ---")
    for dizi in diziler:
        id_, ad, kategori, sezon, bolum, not_ = dizi
        not_text = not_ if not_ else "-"
        print(f"[{id_}] {ad} | {kategori} | {sezon}. Sezon {bolum}. Bölüm | Not: {not_text}")

    try:
        secilen_id = int(input("\nSilmek istediğiniz dizinin ID'sini girin: "))
    except ValueError:
        print("Geçersiz ID girdiniz.")
        conn.close()
        return

    cursor.execute("SELECT name FROM series WHERE id = ?", (secilen_id,))
    secilen_dizi = cursor.fetchone()

    if not secilen_dizi:
        print("Bu ID'ye sahip bir dizi bulunamadı.")
        conn.close()
        return

    onay = input(f"{secilen_dizi[0]} adlı dizi silinecek. Emin misiniz? (evet/hayır): ").lower()
    if onay != "evet":
        print("Silme işlemi iptal edildi.")
        conn.close()
        return

    cursor.execute("DELETE FROM series WHERE id = ?", (secilen_id,))
    conn.commit()
    conn.close()

    print("✅ Dizi başarıyla silindi.")
    