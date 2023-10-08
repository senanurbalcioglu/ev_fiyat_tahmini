import base64
import joblib as joblib
import numpy as np
import streamlit as st
import pandas as pd
import pickle

df = pd.read_excel("istanbul.xlsx", sheet_name="Sheet1")

st.set_page_config(
    page_title="Ev Fiyat Tahmini",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('resim.jpg')

st.sidebar.title("MAHALLE LISTESI")
secilen_ilce = st.sidebar.selectbox("İlçe", options=sorted(list(df["Ilce"].unique())))

mahalle_listesi = sorted(list(df[df["Ilce"]==secilen_ilce]["Mahalle"].unique()))

st.sidebar.table(mahalle_listesi)


yeni_veri ={}

with st.form("my_form"):
    st.write("ISTANBUL")
    ilce = st.selectbox("İlçe", options=sorted(list(df["Ilce"].unique())))
    mahalle = st.selectbox("Mahalle", options=sorted(list(df["Mahalle"].unique())))
    oda_sayisi = st.slider("Oda Sayısı",0 , 9)
    kat = st.slider("Bulunduğu Kat",0 , 99)
    isitma_tipi = st.selectbox("Isıtma Tipi", options=sorted(list(df["Isıtma Tipi"].unique())))
    krediye_uygunluk = st.radio("Krediye Uygunluk", ["Krediye Uygun","Krediye Uygun Değil"])
    yapi_durumu = st.radio("Yapı Durumu", ["Sıfır","Yapım Aşamasında","İkinci El"])
    tapu_durumu = st.selectbox("Tapu Durumu", options=['Kat Mülkiyeti', 'Kat İrtifakı', 'Arsa Tapulu','Müstakil Tapulu', 'Hisseli Tapu'])
    esyali = st.radio("Eşya Durumu", ["Boş","Eşyalı"])
    site_icerisinde = st.radio("Site İçerisinde", ["Evet","Hayır"])
    metrekare = st.slider("Brüt Metrekare",0 , 1000, 0, 10)
    bina_yasi = st.radio("Bina Yaşı", ["0 (Yeni)","1","2","3","4","5-10","11-15","16-20","21 Ve Üzeri"])
    bina_kat_sayisi = st.slider("Binanın Kat Sayısı",0 , 99 )
    kullanim_durumu = st.radio("Kullanım Durumu", ["Boş","Kiracı Oturuyor","Mülk Sahibi Oturuyor"])
    yatirima_uygunluk = st.radio("Yatırıma Uygunluk", ["Yatırıma Uygun","Yatırıma Uygun Değil"])
    banyo = st.selectbox("Banyo Sayısı", options=["0","1","2","3","4","5"])
    balkon = st.selectbox("Balkon Sayısı", options=["0","1","2","3","4","5"])
    wc = st.selectbox("WC Sayısı", options=["0","1","2","3","4","5"])

    # Every form must have a submit button.
    fiyat = st.form_submit_button("HESAPLA")

if fiyat:
    df2 = pd.DataFrame(columns=['Oda Sayısı', 'Bulunduğu Kat', 'Isıtma Tipi',
                                'Krediye Uygunluk', 'Yapı Durumu', 'Tapu Durumu', 'Eşya Durumu',
                                'Site İçerisinde', 'Brüt Metrekare', 'Binanın Yaşı',
                                'Binanın Kat Sayısı', 'Kullanım Durumu', 'Yatırıma Uygunluk',
                                'Banyo Sayısı', 'Balkon Sayısı', 'WC Sayısı', 'Ilce', 'Mahalle'])

    yeni_veri['Oda Sayısı'] = oda_sayisi
    yeni_veri['Bulunduğu Kat'] = kat
    yeni_veri['Isıtma Tipi'] = isitma_tipi
    yeni_veri['Krediye Uygunluk'] = krediye_uygunluk
    yeni_veri['Yapı Durumu'] = yapi_durumu
    yeni_veri['Tapu Durumu'] = tapu_durumu
    yeni_veri['Eşya Durumu'] = esyali
    yeni_veri['Site İçerisinde'] = site_icerisinde
    yeni_veri['Brüt Metrekare'] = metrekare
    yeni_veri['Binanın Yaşı'] = bina_yasi
    yeni_veri['Binanın Kat Sayısı'] = bina_kat_sayisi
    yeni_veri['Kullanım Durumu'] = kullanim_durumu
    yeni_veri['Yatırıma Uygunluk'] = yatirima_uygunluk
    yeni_veri['Banyo Sayısı'] = banyo
    yeni_veri['Balkon Sayısı'] = balkon
    yeni_veri['WC Sayısı'] = wc
    yeni_veri['Ilce'] = ilce
    yeni_veri['Mahalle'] = mahalle

    df2 = pd.concat([df2, pd.DataFrame([yeni_veri])], ignore_index=True)

    sample = df2.copy()

    with open("istanbul.pkl", "rb") as file:
        f = joblib.load(file)

        df3 = pd.read_csv("encode_istanbul.csv")
        df3.drop("Fiyat", axis=1, inplace=True)
        df3.drop("Unnamed: 0", axis=1, inplace=True)

        sutun_isimleri = df3.columns


        # one hot encoder işleminden sonraki sütunları bulsun
        indeks_isitma_tipi = sutun_isimleri.get_loc("Isıtma Tipi_" + sample["Isıtma Tipi"].values[0])
        indeks_krediye_uygunluk = sutun_isimleri.get_loc("Krediye Uygunluk_" + sample["Krediye Uygunluk"].values[0])
        indeks_yapi_durumu = sutun_isimleri.get_loc("Yapı Durumu_" + sample["Yapı Durumu"].values[0])
        indeks_tapu_durumu = sutun_isimleri.get_loc("Tapu Durumu_" + sample["Tapu Durumu"].values[0])
        indeks_esya_durumu = sutun_isimleri.get_loc("Eşya Durumu_" + sample["Eşya Durumu"].values[0])
        indeks_site_icerisinde = sutun_isimleri.get_loc("Site İçerisinde_" + sample["Site İçerisinde"].values[0])
        indeks_binanin_yasi = sutun_isimleri.get_loc("Binanın Yaşı_" + sample["Binanın Yaşı"].values[0])
        indeks_kullanim_durumu = sutun_isimleri.get_loc("Kullanım Durumu_" + sample["Kullanım Durumu"].values[0])
        indeks_yatirima_uygunluk = sutun_isimleri.get_loc("Yatırıma Uygunluk_" + sample["Yatırıma Uygunluk"].values[0])
        indeks_ilce = sutun_isimleri.get_loc("Ilce_" + sample["Ilce"].values[0])
        indeks_mahalle = sutun_isimleri.get_loc("Mahalle_" + sample["Mahalle"].values[0])

        ru = [0] * len(sutun_isimleri)
        ru[0] = int(sample["Oda Sayısı"].values[0])
        ru[1] = int(sample["Bulunduğu Kat"].values[0])
        ru[2] = int(sample["Brüt Metrekare"].values[0])
        ru[3] = int(sample["Binanın Kat Sayısı"].values[0])
        ru[4] = int(sample["Banyo Sayısı"].values[0])
        ru[5] = int(sample["Balkon Sayısı"].values[0])
        ru[6] = int(sample["WC Sayısı"].values[0])

        ru[indeks_isitma_tipi] = 1
        ru[indeks_krediye_uygunluk] = 1
        ru[indeks_yapi_durumu] = 1
        ru[indeks_tapu_durumu] = 1
        ru[indeks_esya_durumu] = 1
        ru[indeks_site_icerisinde] = 1
        ru[indeks_binanin_yasi] = 1
        ru[indeks_kullanim_durumu] = 1
        ru[indeks_yatirima_uygunluk] = 1
        ru[indeks_ilce] = 1
        ru[indeks_mahalle] = 1

        sutun_isimleri = list(sutun_isimleri)
        ru_np = np.array(ru)
        ru_reshaped = ru_np.reshape((1, len(ru_np)))
        ru_ = pd.DataFrame(ru_reshaped, columns=sutun_isimleri)

        result = f.predict(ru_)

        result = int(result)
        result = round(result, -3)
        st.markdown(
            f"""
            <div style="text-align: center;background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px;">
                <span style="font-size: 30px; color: red;">{result} TL</span>
            </div>
            """,
            unsafe_allow_html=True
        )
