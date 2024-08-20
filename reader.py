import exifread as er
import pyfiglet
import colorama
colorama.init(autoreset=True)


app_name = pyfiglet.figlet_format('Python EXIF Reader')


def get_data(path):
    with open(path,'rb') as file:
        data = er.process_file(file)
    
    return data

def get_gps_info(data):
    lat = data.get('GPS GPSLatitude')
    lat_ref = data.get('GPS GPSLatitudeRef')
    lon = data.get('GPS GPSLongitude')
    lon_ref = data.get('GPS GPSLongitudeRef')

    if lat and lon and lat_ref and lon_ref:
        lat = [float(x.num) / float(x.den) for x in lat.values]
        lon = [float(x.num) / float(x.den) for x in lon.values]

        lat = lat[0] + lat[1] / 60 + lat[2] / 3600
        lon = lon[0] + lon[1] / 60 + lon[2] / 3600

        if lat_ref.values[0] != 'N':
            lat = -lat
        if lon_ref.values[0] != 'E':
            lon = -lon

        return lat, lon
    else:
        return None
    
def get_datetime(data):
    datetime_tag = data.get('EXIF DateTimeOriginal')
    if datetime_tag:
        return datetime_tag.values
    else:
        return None
    
    
print(colorama.Fore.CYAN+app_name)
print(colorama.Fore.YELLOW+'Yapımcı: github.com/yigitYildiz1807')
print('*')

while True:
    print("")

    img_path = input(colorama.Fore.RED+'Lütfen okumak istediğiniz fotoğrafın uzantısı ile beraber ismini giriniz:')
    
    try:
        data = get_data(img_path)
        coordinates = get_gps_info(data)
        datetime = get_datetime(data)

        print('')

        if coordinates:
            print(colorama.Fore.GREEN+f'İşte fotoğrafın çekildiği konum: ENLEM:{coordinates[0]} |   BOYLAM:{coordinates[1]}')
            print(colorama.Fore.RED+f'Google Maps Linki: https://www.google.com/maps?q={coordinates[0]},{coordinates[1]}')
        else:
            print('GPS Bilgisi Alınamadı')

        print('')

        if datetime:
            print(colorama.Fore.GREEN+f'İşte fotoğrafın çekildiği tarih ve saat: {datetime}')
        else:
            print('Tarih ve Saat Bilgisi Alınamadı')

        print('')
    
    except:
        print('Okumaya Çalıştığınız dosya bulunamadı')

    option = input(colorama.Fore.BLUE+'Devam etmek istiyor musunuz? (y/N):')
    if option.strip().lower() != 'y':
        print('Program sonlandırıldı')
        break
