
from movies import filmEkle, filmListele, filmGuncelle, filmSilme
from series import diziEkle, diziListele, diziGuncelle, diziSilme

def menu():
    while True:
        
        print("\n--- WATCHLIST MENÜ ---")
        print("📽️ Film İşlemleri")
        print("1. Film ekle")
        print("2. Film listele")
        print("3. Film güncelle")
        print("4. Film sil")

        print("\n📺 Dizi İşlemleri")
        print("5. Dizi ekle")
        print("6. Dizi listele")
        print("7. Dizi güncelle")
        print("8. Dizi sil")

        print("\n9. Çıkış")
        
        secim = input("\nSeçiminiz: ")
        
        if secim == "1":
            filmEkle()
        elif secim == "2":
            filmListele()
        elif secim == "3":
            filmGuncelle()
        elif secim == "4":
            filmSilme()
        elif secim == "5":
            diziEkle()
        elif secim == "6":
            diziListele()
        elif secim == "7":
            diziGuncelle()
        elif secim == "8":
            diziSilme()
        elif secim == "9":
            print("Programdan çıkılıyor...")
            break
        else:
            print("❌ Hatalı seçim yaptınız lütfen tekrar deneyin.")
            
menu()