from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv

# Inisialisasi WebDriver
driver = webdriver.Chrome()  # Pastikan WebDriver sudah dikonfigurasi dengan benar
driver.get("https://gs.hoyoverse.com/genshin/event/e20190909gacha-v3/index.html?win_mode=fullscreen&authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=c9e7809dfc4a25fa68912425d4ee01a5d55c5764&timestamp=1728431529&lang=id&device_type=pc&game_version=OSRELWin5.1.0_R27918307_S27760956_D28057350&region=os_asia&authkey=cS3nk0t0oXQ%2f0A%2fWJljVu%2bhfeHvIkFqO0vOf6d4MK5mH3OJXdsEYZ%2faAfZd7PZrAfYwHchVZGjJT9R9CXonoEaNHfxc8BqMF6r2IEaR5YHvHPqHN%2bjGqnYM05dsKYj%2fihvlNyFg35DTH3o%2bVg6B2LHZMtjr0wBo5zNsmXW9tnrT2QLj4xqP73%2faCZATYEsX6BpP%2bhf0gyOPXOjrwFRS%2bVHSgp%2byLiSbmkNY86jrhDUgNSJGWBG2SZuHtq%2fH3sU%2by71un33FJ8ikYlvUxgoHcfv%2fvUQGQP7lIlG4AixZpFk8BjaD7u3m8PuSToIs7HBJDPXo8Xf8xCz5CDYo35klI9UhVyjmJzTvEs2y3qRzlk9s77QKO45Lfy4umfzKW3SRtJzF3%2fYrZiNRjSEmYIGFyvJqsCXROhUY1YjDwr0mnJ5snzOGvYGH59reaXkAMV6dIQIoIASP2w561Rh0IZ8lcLfs%2buyG9hcgs8g57boPTGaRjUwXjeIwpj4ESunN3L5g5RxAGNX9w7fxQbyt1GPmvHSquYV8r6eA6zYDtJesKBG3hXSp4R8dOK1%2bq9Q%2bDkbvVGzJHXp5S4tmt3eZ2D7mbcMVmWY6P3gMWnHZRal6TRvhcLxNrUQYzaEuuXDTJNASXX1jZuXJqHdKXPQZFBxzfmgvdGOoi8hnN9Iqy9YLYJKOem7efumgmEANTuTjIwS6wHhW%2fJbG1oyyf4Z4J2wq%2fBID28zVk9epFVigdARMxe%2f9c72GBbN7qfFrPSpGTfpoJjORRrAkoR35ybACR2qPZFm%2f5HrqIlHfU74Q3PPS3vda9WkMxC2HYv6Sgr%2fGJyej7Il4a5zsW00DpCZCiZKNUCnKv3V4mqoaL%2bLP1dBCx6%2fVnOxBvg7Cekw0QfQECJUs03XNSV5DwLIfWOjECuPZ4Pw789JyuWC6K%2fYZfdbjSbxx2O8SuMjz87dZJrdqGOEdR1HxB5ORyYdkFMsF3dMc9LZGG6NW5fToyo1QR0xwvkKSB%2b9Z7axw%2bsPM3PAkCsKD4kh1UG7f0oaxGSaQr1VRf6IleUa%2ftNpRozDHSOVGWbSnJ9SjWga%2bxJojkQKIOC2ZIk4iK5uvbtB12d1j9EfFZN%2fIIOOc9er0F8J%2bByYhM5f71rtgdxOdOm0zz7gvjGE%2f2KUTfR%2f8ggjU%2fRoBv%2bWyaUg61iMcQ0P0oSZIKyhQ449%2bzfZ3Y9H%2bwaoQ5K%2bFIvHdqcueGxGZNFxPOjJmTagnNbhmttWlcqEK0zDuKbE%2bxHzYa82N%2bIkL5IEAJudER3Pw9qdc5VaYvY1RHmkKr4M4UENdf%2b42wknA6QsY5j6aCLhn8KoXxixVVbk9MMLRwu%2bjy8J2nS3rtwB%2bSz%2fUQAvaFIQ%3d%3d&game_biz=hk4e_global#/log")  # Ganti dengan URL halaman yang ingin di-scrape

wish_data = []
jenis_permohonan = {"301": "Event Permohonan Karakter dan Event Permohonan Karakter - 2","302" : "Event Permohonan Senjata","200":"Permohonan Standar"}
page_number = 1  # Counter halaman untuk log

for jenis_id, jenis_name in jenis_permohonan.items():
    time.sleep(2)

    try:
        menu_type_button = driver.find_element(By.CLASS_NAME, "menu_type")
        print("Mengklik menu untuk menampilkan daftar kategori...")
        menu_type_button.click()
        time.sleep(1)  # Tunggu sebentar agar menu muncul
    except NoSuchElementException:
        print("Menu utama untuk memilih jenis permohonan tidak ditemukan.")
        driver.quit()
        exit()

    try:
        items = driver.find_elements(By.CLASS_NAME, "item")
        for item in items:
            if item.get_attribute("data-id") == jenis_id:
                print(f"Mengklik kategori {jenis_name} dengan ID {jenis_id}...")
                item.click()  # Klik kategori
                time.sleep(2)  # Tunggu sebentar agar data termuat
                break
    except NoSuchElementException:
        print(f"Kategori dengan ID {jenis_id} tidak ditemukan.")
        continue  # Jika tidak ditemukan, lanjut ke kategori beriku


    # Loop untuk mengumpulkan data dari setiap halaman
    while True:
        # Tunggu beberapa detik untuk memastikan halaman termuat sepenuhnya
        time.sleep(2)

        # Parsing halaman saat ini dengan BeautifulSoup
        print(f"\nMengambil data dari halaman {page_number}...")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.find_all("div", class_="log-item-row")

        # Ekstrak data dari setiap log-item-row
        for row in rows:
            item_type = row.find("span", class_="type").get_text(strip=True)
            item_name = row.find("span", class_="name").get_text(strip=True)
            wish_type = row.find("span", class_="wish").get_text(strip=True)
            time_obtained = row.find("span", class_="time").get_text(strip=True)

            # Simpan data sebagai dictionary
            wish_data.append({
                "Jenis Item": item_type,
                "Nama Item": item_name,
                "Jenis Permohonan": wish_type,
                "Waktu Perolehan": time_obtained
            })

        print(f"Berhasil mengumpulkan {len(rows)} item dari halaman {page_number}.")

        # Cek tombol 'next' dan status disable-nya
        try:
            next_button = driver.find_element(By.CLASS_NAME, "wrapper-icon_r")
            
            # Cek apakah tombol disable
            if "wrapper-icon_disable-r" in next_button.get_attribute("class"):
                print("Tidak ada halaman berikutnya, proses selesai. lanjut ke kategori berikutnya.")
                break  # Keluar dari loop karena sudah di halaman terakhir
            
            # Klik tombol untuk pindah ke halaman berikutnya jika tidak disable
            print("Memuat halaman berikutnya...")
            next_button.click()
            page_number += 1  # Tingkatkan nomor halaman untuk log berikutnya
        
        except NoSuchElementException:
            print("Tombol 'next' tidak ditemukan. Proses berhenti.")
            break

# Tutup browser setelah selesai
driver.quit()

# Cetak hasil data yang telah dikumpulkan
print("\nProses scraping selesai. Berikut adalah data yang berhasil dikumpulkan:")
for data in wish_data:
    print(data)


# Cetak atau simpan data
with open("wishData.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Jenis Item", "Nama Item", "Jenis Permohonan", "Waktu Perolehan"])
    writer.writeheader()
    writer.writerows(wish_data)

print("Data telah disimpan ke wish_data.csv")