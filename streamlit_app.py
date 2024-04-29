import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
def load_data():
    # Load your dataset here, replace 'your_dataset.csv' with your actual dataset file
    #data = pd.read_excel('C:/Users/X1 Carbon/Desktop/LatihanStreamlit2/datasumbersampah.xlsx')
    data = pd.read_excel('datasumbersampah.xlsx')
    return data

# Load the dataset
datasampah = load_data()

#datasampah
#st.dataframe(datasampah)

#membuat field baru (Total)
datasampah['total']=datasampah['rumahtangga']+datasampah['perkantoran']+datasampah['pasar']+datasampah['perniagaan'] \
                    +datasampah['fasilitaspublik']+datasampah['kawasan']+datasampah['lainnya']
#datasampah

#mau diBreakDown/diFilter by province
attributProvince = datasampah['provinsi'].unique().tolist()
#st.write(attributProvince)

row1_left, row1_middle, row1_right = st.columns((0.1, 3, 0.1))
with row1_middle:
    st.title('Jumlah Sampah Provinsi Berdasarkan Sumber Sampah Tahun 2021')
    st.subheader('Streamlit App by [Endy Ramadian](https://linkedin.com/in/endy-ramadian-993316106)')
    st.markdown('Sampah merupakan masalah yang dihadapi hampir seluruh Negara di dunia. Tidak hanya di Negara negara berkembang, tetapi juga di\
                 negara - negara maju, sampah selalu menjadi masalah. Rata-rata setiap harinya kota-kota besar di Indonesia menghasilkan puluhan ton sampah.\
                 Pada dashboard berikut akan ditampilkan jumlah sampah (dalam satuan Ton) pada tiap provinsi di Indonesia berdasarkan sumber sampah.')
    st.markdown('Data yang digunakan bersumber dari https://sipsn.menlhk.go.id/sipsn/public/data/sumber')

#sidebar
st.sidebar.markdown("**Isikan parameter berikut :**")   
provinsiygdipilih = st.sidebar.selectbox('Pilih Provinsi', attributProvince)
#st.write(provinsiygdipilih)

datasampahprovinsi = datasampah.loc[datasampah['provinsi'] == provinsiygdipilih].reset_index(drop = True)
#print(datasampahprovinsi)
#st.dataframe(datasampahprovinsi)

row2_left, row2_middle, row2_right = st.columns((.1, 3, .1))
with row2_middle:
    st.subheader('Data yang digunakan')     
    st.dataframe(datasampahprovinsi)

sektorsumbersampah = ['rumahtangga', 'perkantoran', 'pasar', 'perniagaan', 'fasilitaspublik', 'kawasan', 'lainnya']
#st.write(sektorsumbersampah)

datasampahrumahtangga = datasampahprovinsi['rumahtangga'].sum()
#print(datasampahrumahtangga)
st.write('datasampahrumahtangga: ', datasampahrumahtangga)

#bikin dataframe baru
jumlahsampah = pd.DataFrame(columns=['provinsi', 'jumlahsampah', 'kategorisampah'])
for sektor in sektorsumbersampah:
    jumlah = datasampahprovinsi.groupby(['provinsi']).agg(jumlahsampah = (sektor, pd.Series.sum))
    jumlah['kategorisampah'] = 'Sampah ' + sektor.capitalize()
    jumlah = jumlah.reset_index()
    jumlahsampah = pd.concat([jumlahsampah, jumlah])

jumlahsampah = jumlahsampah.reset_index(drop=True)
#print(jumlahsampah)
#st.dataframe(jumlahsampah)

#function tampilkan chart (visualisasi data)
import numpy as np
import matplotlib.pyplot as plt
def plotBar(data, x, y, color):
    #Definisikan kolom yang akan di plot
    x, y = data[x], data[y]
    #Buat 1 Fugure and 1 subplot
    fig, ax = plt.subplots()
        
    #Bersihkan terlebih dahulu axes
    ax.clear()
    
    #Atur warna
    color = plt.get_cmap(color)(np.linspace(0.25, 0.85, len(data)))
    
    #Atur ukuran figure
    fig.set_size_inches(10, 6)
    
    #Plot data
    ax.barh(x, y, color = color)

    #Beri label pada sumbu (labelpad = memberi jarak label terhadap grafik)
    ax.set_xlabel(xlabel = 'Jumlah Sampah (Ton)', labelpad = 12)
    
    #Memberi anotasi pada grafik
    j = 0
    for i in plt.gca().patches:
        ax.text(i.get_width()+.5, i.get_y()+.4, str(round(y[j],2)), fontsize = 8, color='black')
        j = j + 1
        
    #Hapus garis pada frame bagian kanan dan atas (atau dapat disesuaikan kebutuhan)
    frame = ['right', 'top']
    for i in frame:
        ax.spines[i].set_visible(False)
    
    return fig, ax

#jumlahsampah = jumlahsampah.sort_values(by = ['jumlahsampah'])
#jumlahsampah = jumlahsampah.reset_index(drop=True)
#fig1, ax1 = plotBar(data=jumlahsampah, x='kategorisampah', y='jumlahsampah', color='Purples')
fig1, ax1 = plotBar(data=jumlahsampah, x='kategorisampah', y='jumlahsampah', color='Greens')
#-> di Spyder muncul di atas kanan, bagian plot

#tampilkan plot grafik di streamlit
row3_left, row3_middle, row3_right = st.columns((0.1, 3, 0.1))
with row3_middle:
    st.subheader('Jumlah Sampah Provinsi {} Tiap Sektor'.format(provinsiygdipilih))
    st.markdown('Berikut Ditampilkan Hasil Visualisasi Dari Data Sampah Provinsi Tersebut:')
    st.pyplot(fig1)

