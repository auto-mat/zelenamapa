Sorry, no english info at moment. Please contact kontakt@zelenamapa.cz with any questions.

Zelená mapa
==========

Django aplikace Zelená mapa Prahy http://www.zelenamapa.cz

Zelená mapa představuje zcela nový pohled na město. Nejde o mapu dopravní, ale plán příjemných tras pro chodce, rodiče s dětmi, seniory a cyklisty, odpovědných obchodů a míst pro trávení volného času.

Instalace
============

Ke zprovoznění je zapotřebí následující

* Postgres 8.4 + postgis 1.5

Aplikace se nainstaluje do prostředí virtualenv pomocí následujících příkazů:

* virtualenv --no-site-packages env
* env/bin/pip install distribute --upgrade
* env/bin/pip install -r requirements.txt

Vzorová konfigurace je v pnk/sample_settings.py, stačí přejmenovat na settings.py a doplnit přístup k DB a SECRET_KEY.
