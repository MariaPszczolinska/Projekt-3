from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker, MarkerMapLayer

import gpx
import math  

plik2= open('odleglosc.txt','w')
szer=40
plik2.write('-' * szer)             
plik2.write("\n| {:^10}  |\n".format("odleglosc [m]"))
plik2.write('-' * szer)

class AddLocationForm(BoxLayout):
    search_long = ObjectProperty()
    search_lat = ObjectProperty()
    my_map = ObjectProperty()
    
    def search_location(self):
        latitude = self.search_lat.text
        longitude = self.search_long.text
        self.draw_marker(latitude, longitude)
        #print(latitude, longitude)
        
    def draw_marker(self, lati, long):
        marker = MapMarker(lat = lati, lon = long)
        self.my_map.add_marker(marker)
    
    def analyse_file(self):
        #wybor pliku
        filename='chojnowski-szlak-rowerowy.gpx'
        #wczytanie pliku
        lon, lat, ele = gpx.wczytaj_plik(filename)
        #oblicz statystyk
        #sciezka
        self.draw_route(lat, lon)
        #wykres
        #pass
        
        #wspolrzedne i odleglosc
        for fi,la,h in zip(lat,lon,ele):
            a=6378245.000;
            e2=0.006693421622;
            N=a/math.sqrt(1-e2*((math.sin(fi))**2));
            X=(N+h)*math.cos(fi)*math.cos(la)
            Y=(N+h)*math.cos(fi)*math.sin(la)
            Z=((1-e2)*N+h)*math.sin(fi)
            
            #FUNKCJA LICZACA ODLEGLOSC
            def foo(it):
                it = iter(it)
                f = it.next()
                for s in it:
                    yield f, s
                    f = s
                    odleglosc=math.sqrt([x[1] - x[0] for x in foo(X)]**2+[(y[1] - y[0]) for y in foo(Y)]**2)
                    cala=sum(odleglosc)
                    plik2.write('\n| {:^10}|'.format('%.3f' %cala))
            #nie wiem jak zapisać to do pliku zewnetrznego, kiedy wyjmuje zapis poza def foo ot krzyczy ze 'cala' niezdefiniowa
                  
        #vincenty
        '''
        fa=;
        la=;
        fb=;
        lb=;

        a=6378137.000;
        e2=0.00669438002290;
        b=a*math.sqrt(1-e2);
        f=1-(b/a);
        Ua=math.atan((1-f)*math.tan(fa));
        Ub=math.atan((1-f)*math.tan(fb));
        L=lb-la;

        while 1:
            ss=math.sqrt((math.cos(Ub)*math.sin(L))^2+(math.cos(Ua)*math.sin(Ub)-math.sin(Ua)*math.cos(Ub)*math.cos(L))^2);
            cs=math.sin(Ua)*math.sin(Ub)+math.cos(Ua)*math.cos(Ub)*math.cos(L);
            s=math.atan(ss/cs);
            sa=(math.cos(Ua)*math.cos(Ub)*math.sin(L))/ss;
            c2a=1-(sa)^2;
            cos2s=cs-((2*math.sin(Ua)*math.sin(Ub))/c2a);
            c=(f/16)*c2a*(4+f*(4-3*c2a));
            Ls=L;
            L=(lb-la)+(1-c)*f*sa*(s+c*ss*(cos2s+c*cs*(-1+2*(cos2s)^2)));
            if abs(L-Ls)<(0.000001/206265):
                break

        u2=((a^2-b^2)/(b^2))*(c2a);
        A=1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)));
        B=(u2/1024)*(256+u2*(-128+u2*(74-47*u2)));
        ds=B*ss*(cos2s+(1/4)*B*(cs*(-1+2*(cos2s)^2)-(1/6)*B*cos2s*(-3+4*(ss)^2)*(-3+4*(cos2s)^2)))

        sab=b*A*(s-ds)
        print(sab,'Odleglosc miedzy punktami')
        '''
        
    def draw_route(self, lat, lon):
        # utworzenie nowej warstwy i dodanie jej do mapy
        data_layer = MarkerMapLayer()
        self.my_map.add_layer(data_layer) # my_map jest obiektem klasy MapView
        for point in zip(lat, lon):
            self.mark_point(*point , layer=data_layer)
        
    def mark_point(self, lat, lon, layer=None, markerSource="dot.png"):
        if lat != None and lon != None:
            marker = MapMarker(lat=lat, lon=lon, source=markerSource)
            self.my_map.add_marker(marker, layer=layer)
            
       
class MapViewApp(App):
    def build(self):
        return AddLocationForm()
    #pass
    
    
if __name__=='__main__':
    MapViewApp().run()  
    
plik2.close()  
    

    
