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

* ./update.sh reinstall

Vzorová konfigurace je v pnk/sample_settings_local.py, stačí překopírovat na settings_local.py a doplnit přístup k DB a SECRET_KEY.
