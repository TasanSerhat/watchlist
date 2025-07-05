import sqlite3

def filmEkle():
    
    name = input("Film adı: ").strip()
    print("""\n
      Korku
      Aksiyon
      Animasyon
      Komedi
      Bilim Kurgu
      Gerilim
      Dram
      Aşk""")
    category = input("Film Kategorisi: ").strip()
    
    while True:
        watchedInput = input("İzlendi mi? (evet/hayır): ").lower()
        if watchedInput == "evet":
            watched = 1
            break
        elif watchedInput == "hayır":
            watched = 0
            break
        else:
            print("❌ Hatalı seçim yaptınız lütfen tekrar deneyin.")
            
    note = input("Notunuz (isteğe bağlı): ")

    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO movies (name, category, watched, note) VALUES (?, ?, ?, ?)",
                   (name,category,watched,note))
    
    conn.commit()
    conn.close()
    
    print("✅ Film başarıyla eklendi.")
                
                
def fimListeleTum():
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, watched, note FROM movies")
    filmler = cursor.fetchall()

    if not filmler:
        print("❌ Henüz film eklenmemiş.")
    else:
        print("\n--- Tüm Filmler ---")
        for film in filmler:
            ad, kategori, izlenme, not_ = film
            durum = "İzlendi" if izlenme else "İzlenmedi"
            print(f"🎬 {ad} | Tür: {kategori} | Durum: {durum} | Not: {not_ if not_ else '-'}")

    conn.close()
    
    
def listeleKategori():
    
    print("""
      Korku
      Aksiyon
      Animasyon
      Komedi
      Bilim Kurgu
      Gerilim
      Dram
      Aşk""")
    kategori = input("Listelemek istediğiniz kategori nedir: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, watched, note FROM movies WHERE LOWER(category) = ?",(kategori,))
    filmler = cursor.fetchall()
    
    if not filmler:
        print(f"❌ '{kategori}' kategorisinde film bulunamadı.")
    else:
        print(f"\n--- {kategori} Kategorisindeki Filmler ---")
        for film in filmler:
            ad, izlenme, not_ = film
            durum = "İzlendi" if izlenme else "İzlenmedi"
            print(f"🎬 {ad} | Durum: {durum} | Not: {not_ if not_ else '-'}")

    conn.close()
    

def filmArama():
    
    aranan = input("Aramak istediğiniz filmin adını giriniz: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, watched, note FROM movies WHERE LOWER(name) LIKE ?", (f"%{aranan}%",))
    filmler = cursor.fetchall()
    
    if not filmler:
        print("❌ Aradığınız filme ait bir sonuç bulunamadı.")
    else:
        print("\n--- Arama Sonuçları ---")
        for film in filmler:
            ad, kategori, izlenme, not_ = film
            durum = "İzlendi" if izlenme else "İzlenmedi"
            print(f"🎬 {ad} | Tür: {kategori} | Durum: {durum} | Not: {not_ if not_ else '-'}")

    conn.close()
    
def listeleIzlenen():
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, note FROM movies WHERE watched = 1")
    filmler = cursor.fetchall()

    if not filmler:
        print("❌ Hiç izlenmiş film bulunamadı.")
    else:
        print("\n--- İzlenmiş Filmler ---")
        for film in filmler:
            ad, kategori, not_ = film
            print(f"🎬 {ad} | Tür: {kategori} | Not: {not_ if not_ else '-'}")

    conn.close()
    
def listeleIzlenmeyen():
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, category, note FROM movies WHERE watched = 0")
    filmler = cursor.fetchall()
    
    if not filmler:
        print("❌ Hiç izlenmemiş film bulunamadı.")
    else:
        print("\n--- İzlenmemiş Filmler ---")
        for film in filmler:
            ad, kategori, not_ = film
            print(f"🎬 {ad} | Tür: {kategori} | Not: {not_ if not_ else '-'}")

    conn.close()


def filmListele():
    while True:
        
        print("\nFilm listeleme menüsü: ")
        print("1-Tüm filmleri listele")
        print("2-Kategoriye göre listele")
        print("3-Film adıyla arama")
        print("4-Sadece izlenen filmleri listele")
        print("5-Sadece izlenmeyen filmleri listele")
        print("6-Geri dön")
        
        secim = input("\nSeçiminiz (1-6): ")
        
        if secim == "1":
            filmListeleTum()
            break
        elif secim == "2":
            listeleKategori()
            break
        elif secim == "3":
            filmArama()
            break
        elif secim == "4":
            listeleIzlenen()
            break
        elif secim == "5":
            listeleIzlenmeyen()
            break
        elif secim == "6":
            return
        else:
            print("❌ Hatalı seçim yaptınız lütfen tekrar deneyin.")
            
def filmGuncelle():
    
    aranan = input("Güncellemek istediğiniz film adını girin: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, category, watched, note FROM movies WHERE LOWER(name) LIKE ?", (f"%{aranan}%",))
    filmler = cursor.fetchall()
    
    if not filmler:
        print("❌ Film bulunamadı.")
        conn.close()
        return
    
    print("\n--- Eşleşem Filmler ---")
    for film in filmler:
        id_, ad, kategori, izlenme, not_ = film
        durum = "İzlendi" if izlenme else "İzlenmedi"
        print (f"[{id_}] {ad} | Tür: {kategori} | Durum: {durum} | Not: {not_ if not_ else '-'}")
        
    try:
        secilen_id = int(input("\nGüncellemek istediğiniz filmin ID numarasını girin: "))
    except ValueError:
        print("❌ Geçersiz giriş.")
        conn.close()
        return
    
    cursor.execute("SELECT name, category, watched, note FROM movies WHERE id = ?", (secilen_id,))
    sonuc = cursor.fetchone()
    
    if not sonuc:
        print("❌ Belirtilen ID'ye ait film bulunamadı.")
        conn.close()
        return
    
    eski_ad, eski_kategori, eski_izlenme, eski_not = sonuc
    
    print("\n--- Alanları güncelleyin (boş bırakırsanız eski değer korunur) ---")
    
    yeni_ad = input(f"Yeni ad ({eski_ad}): ").strip()
    yeni_kategori = input(f"Yeni kategori ({eski_kategori}): ").strip()
    yeni_durum = input(f"İzlendi mi? (evet/hayır) ({'evet' if eski_izlenme else 'hayır'}): ").strip().lower()
    yeni_not = input(f"Yeni not ({eski_not if eski_not else '-' }): ").strip()
    
    if not yeni_ad:
        yeni_ad = eski_ad
    if not yeni_kategori:
        yeni_kategori = eski_kategori
    if yeni_durum == "evet":
        yeni_izlenme = 1
    elif yeni_durum == "hayır":
        yeni_izlenme = 0
    else:
        yeni_izlenme = eski_izlenme
    if not yeni_not:
        yeni_not = eski_not
        
    cursor.execute("""
                   UPDATE movies
                   SET name = ?, category = ?, watched = ?, note = ?
                   WHERE id = ?
                   """, (yeni_ad, yeni_kategori, yeni_izlenme, yeni_not, secilen_id))
    
    conn.commit()
    conn.close()
    
    print("✅ Film başarıyla güncellendi.")
    
def filmSilme():
    
    aranan = input("Silmek istediğiniz film adını girin: ").lower()
    
    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, category, watched, note FROM movies WHERE LOWER(name) LIKE ?", (f"%{aranan}%",))
    filmler = cursor.fetchall()
    
    if not filmler:
        print("❌ Film bulunamadı.")
        conn.close()
        return
    
    print("\n--- Eşleşem Filmler ---")
    for film in filmler:
        id_, ad, kategori, izlenme, not_ = film
        durum = "İzlendi" if izlenme else "İzlenmedi"
        print (f"[{id_}] {ad} | Tür: {kategori} | Durum: {durum} | Not: {not_ if not_ else '-'}")
        
    try:
        secilen_id = int(input("\nSilmek istediğiniz filmin ID numarasını girin: "))
    except ValueError:
        print("❌ Geçersiz giriş.")
        conn.close()
        return
    
    cursor.execute("SELECT name, category, watched, note FROM movies WHERE id = ?", (secilen_id,))
    film = cursor.fetchone()

    if not film:
        print("❌ Belirtilen ID'ye ait film bulunamadı.")
        conn.close()
        return
    
    onay = input(f"{film[0]} adlı Filmi silmek istediğinizden emin misiniz? (evet/hayır): ").lower()
    
    if onay != 'evet':
        print("❌ Silme işlemi iptal edildi.")
        conn.close()
        return
    
    cursor.execute("DELETE FROM movies WHERE id = ?", (secilen_id,))
    conn.commit()
    conn.close()
    
    print("✅ Film başarıyla silindi.")
    

    
    
        