from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt

class ModeloSKL:
    def __init__(self)-> None:
            pass
    def setear_modelo(self,modelo,**kwargs):
        self.modelo = modelo(**kwargs)
        self.modelo.fit(self.x_train, self.y_train)
        return {"test":self.modelo.score(self.x_test,self.y_test),"train":self.modelo.score(self.x_train,self.y_train)}

    def splitear(self, a_predecir,dataset, split_train: float=0.15,datos:list =['mes','dia','hora', 'temperatura', 'humedad', 'presion','direccion_viento', 'velocidad_viento']):
        self.split_train = split_train
        self.dataset = dataset
        self.datos_cargados = datos
        self.a_predecir = a_predecir

        x = []
        y = []
        f = []
        for grupo,df in dataset.groupby("fecha"):
            x.append(df[datos].to_numpy().flatten())
            if len(x[-1]) != 24 * len(datos):
                x.pop()
                continue
            y.append(df[a_predecir].iloc[0])
            f.append(grupo)
                
        assert(len(y) == len(x) and len(x) == len(f))
        
        self.x_train, self.x_test, self.y_train, self.y_test, self.f_train, self.f_test = train_test_split(x,y,f,test_size=split_train)

    def predecir(self, x):
        return self.modelo.predict(x)

    def plotear_perf(self): 
        def plotear_datos(titulo,*vargs):
            l = list(zip(*vargs,strict=True))
            l.sort(key=lambda x: x[0])
            l = [list(t) for t in zip(*l)]
            f = l[0]
            x = l[1]
            y = l[2]
            try:
                iter(y)
                for t1,t2 in zip(zip(*y),zip(*self.modelo.predict(x))):
                    plt.figure()
                    plt.plot(f, t1, c="blue", label="data",linewidth=1)
                    plt.plot(f, t2, color="red", label="prediccion", linewidth=1)
                    plt.xlabel("data")
                    plt.ylabel("target")
                    plt.title(titulo)
                    plt.show()
            except:
                plt.figure()
                plt.plot(f, y, c="blue", label="data",linewidth=1)
                plt.plot(f, self.modelo.predict(x), color="red", label="prediccion", linewidth=1)
                plt.xlabel("data")
                plt.ylabel("target")
                plt.title(titulo)
                plt.show()
        plotear_datos("test",self.f_test,self.x_test,self.y_test)
        plotear_datos("train",self.f_train,self.x_train,self.y_train)
    
    def exportar_modelo(self,ruta="server/modelo.mod"):
        with open(ruta,"wb") as f:
            pickle.dump(self,f)
    
    def usar_metrica(self,metrica,**kwargs):
        predicciontrain = self.predecir(self.x_train)
        predicciontest = self.predecir(self.x_test)
        return {"train":metrica(self.y_train,predicciontrain,**kwargs),"test":metrica(self.y_test,predicciontest,**kwargs)}



