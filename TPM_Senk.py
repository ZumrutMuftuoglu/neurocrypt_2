#2 TPM oluşturur (random walk ile)
import time
import sys

#TPM parametreleri
k = 3
n = 4
d = 6

#Öğrenme kuralını tanımlıyoruz.
rule = ['random_walk']
rule = rule[0]

#2 TPMs oluşturuyoruz : Alice and Bob.
print("TPM oluşturuluyor... k=" + str(k) + ", n=" + str(n) + ", d=" + str(n))
print("Öğrenme kuralı olarak " + rule + " kullanılıyor.")
Alice = TPM(k, n, d)
Bob = TPM(k, n, d)

#Rasgele sayı üreteci
def random():
    return np.random.randint(-d, d + 1, [k, n])
    
#İki TPM'in senkronizasyon skorunu burası veriyor.
def sync_score(m1, m2):
    return 1.0 - np.average(1.0 * np.abs(m1.W - m2.W)/(2 * d))

#Senkronizasyon ağırlıkları
sync = False # ağırlıkların senkron olup olmadığını kontrol eder
nb_updates = 0 # sayacı günceller
#nb_eve_updates = 0 # To count the number of times eve updated
start_time = time.time() # zamanlayıcıyı başlatır
sync_history = [] # her güncelleme sonrası senkronizasyon skorunu saklar

while(not sync):
    X = random() # rasgele boyutlu vektör oluşturur [k, n]
    tauA = Alice(X) # TPM1(Alice)' in çıkış değerini alır.
    tauB = Bob(X) # TPM2(Bob)' nin çıkış değerini alır.
    Alice.update(tauB, rule) # TPM1(Alice)'i TPM2(Bob)'un çıkış değeriyle günceller  
    Bob.update(tauA, rule) # TPM2(Bob)'yi TPM1(Alice)'in çıkış değeriyle günceller
    
    if tauA == tauB :
        nb_updates += 1

    score = 100 * sync_score(Alice, Bob) # İki TPM'in senkronizasyon skorunu yüzedelik olarak hesaplar.
    sync_history.append(score) # Senkronizasyon yüzdesini kaydeder.
    sys.stdout.write('\r' + "Senkronizasyon Yüzdesi = " + str(int(score)) + "%   /  Güncelleme Sayısı = " + str(nb_updates) ) 
    
    if score == 100: # Senkronizasyon yüzdesi %100 olduğunda sync'yi True değerine çeker.
        sync = True

end_time = time.time()
time_taken = end_time - start_time # Senkronizasyon için geçen süreyi hesaplar.

#Yazdırılanlar
print ('\nTPMler senkronize oldu')
print ('Geçen süre = ' + str(time_taken)+ " saniye.")
#print(X)
print('tauA='+str(tauA))#TPM1(Alice)' in çıkış değerini yazdırır.
print ('tauB='+str(tauB))#TPM2(Bob)' nin çıkış değerini yazdırır.

#Senkronizasyon geçmişini çizdirir. 
import matplotlib.pyplot as mpl
mpl.plot(sync_history)
mpl.show()

