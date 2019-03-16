#TPM'i oluşturur(random walk ile).
class TPM:
    '''Burada TPM'i oluşturuyoruz. TPM binary çıkış üretir(tau).
    Parametreler :
    
    k - Gizli katman sayısı
    n - Her bir gizli nörona bağlı giriş nöronlarının sayısı
    d - Başlangıç için ağırlık değer aralığı ({-D, ..., -2, -1, 0, 1, 2, ..., +D })
    W - k*n boyutlu ağırlık matrisi
    '''
#ilklendirme (ağ topolojisi burada belirlenir)
    def __init__(self, k=3, n=4, d=6):
        
        self.k = k
        self.n = n
        self.d = d
        self.W = np.random.randint(-d, d + 1, [k, n])
    def get_output(self, X):
        '''
        X - Rastgele giriş vektörü
        Buradaki işlem {-1,1} değerlerini döndürür
        '''
        k = self.k
        n = self.n
        W = self.W
        X = X.reshape([k, n])
        sigma = np.sign(np.sum(X * W, axis=1)) # sigmayı hesaplar
        tau = np.prod(sigma) # çıkışa götürür
        self.X = X
        self.sigma = sigma
        self.tau = tau
        return tau

    def __call__(self, X):
        return self.get_output(X)

    def update(self, tau2, rule='random_walk'):
        
        '''
        Burada kullandığımız öğrenme kuralına göre ağırlıkları güncelliyoruz.
        tau2 - diğer makinenin çıkışına götürür
        
        '''
        X = self.X
        tau1 = self.tau
        sigma = self.sigma
        W = self.W
        d = self.d

        if (tau1 == tau2):
            if rule == 'random_walk':
                random_walk(W, X, sigma, tau1, tau2, d)            
            else:
                raise Exception("Invalid update rule. Valid update rule is:" +  
                    "\'random_walk\'.")
