[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/iVhjdzUt)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10840769&assignment_repo_type=AssignmentRepo)
---
authors:
- Ivan Mansilla Flores, Oscar de Caralt Roy

professors:
- Blai Ras Jimenez,  Eloi Puertas

date: 01/06/2023

# Pràctica 2 - FastAPI and Vue application (Software distribuït)
---

Introducció
============

# Pràctica: Pàgina web d'esdeveniments esportius

Aquest és un repositori per a la pràctica de desenvolupament d'una pàgina web capaç de mostrar informació sobre esdeveniments esportius i permetre la reserva d'entrades. Primer de tot, desenvoluparem una REST API que ens proporcionarà la informació necessària. També implementarem les funcions per gestionar aquestes dades, com ara afegir, eliminar o modificar els esdeveniments emmagatzemats.

Utilitzarem el framework FastAPI per aquest propòsit.

## Requisits

- Python 3 (recomanada la versió més recent)
- Paquets de Python instal·lats a través de pip

## Instal·lació

Per començar, segueix els passos següents per instal·lar les dependències necessàries:

1. Clona aquest repositori al teu ordinador.
2. Navega fins al directori del projecte.
3. Executa la següent comanda per instal·lar les dependències:


  <code>pip install -r requirements.txt</code>


Es recomana altament l'ús de la IDE [PyCharm Professional](https://www.jetbrains.com/pycharm/) per al desenvolupament d'aquesta pràctica

## Execució
Per executar el projecte, segueix els passos següents:

Navega fins al directori del projecte.
Executa la següent comanda:
uvicorn main:app --reload

Ara, la REST API està en funcionament i pots accedir-hi a través de l'adreça 

http://localhost:8000.

## Funcionalitats implementades:
Hem aconseguit implementar la gran majoria d'objectius i funcionalitats que se'ns proposaven setmana a setmana

## Limitacions

Hem de tenir en compte que no hem aconseguit implementar completament dues funcionalitats importants:

Desplegament a Azure (Deployment): No hem pogut completar el procés de desplegament de la pàgina web. No obstant això, pots executar el projecte localment seguint les instruccions anteriors per a l'execució.
Inici de sessió (Sign In): També hem tingut dificultats per implementar completament la funcionalitat d'inici de sessió. Per tant, en aquesta versió, no és possible iniciar sessió com a usuari.
Protecció dels endpoints: Degut a que no es pot fer login amb una account no es pot obtenir si una account és admin o no i per tant no hem pogut protegir els endpoints.
Sessió de Test: Tot i que vam venir a la sessió de test vam ser incapaços de provar amb altra gent a causa de múltiples errors que ens donava en el que aquell moment havíem fet de deployment. La part positiva és que vam poder provar la web del grup del costat i vam veure com havia de ser la funcionalitat i ens vam adonar que el nostre disseny fet en aquell moment era una mica pobre.


## Aplicacio final amb el dcoker:
![image](https://github.com/SoftwareDistribuitUB-2023/practica-2-a09/assets/72189801/2f25e1a3-95ab-4448-b04a-290a196e21b3)


Enviament dels Exercicis
------------------------
Es treballarà de la mateixa manera que a la Pràctica 1. Els exercicis i deures s'enviaran com a Pull Requests al repositori del Github Classroom. Les respostes a les preguntes 
s'enviaran com a commentaris en el Pull Requests. S'ha de fer Peer Review dels Pull Requests per part de l'altre membre del grup.

Avaluació pràctica 2.
---------------------------
- 30% Fer els pull requests setmanalment.
- 70% Lliurament final: 20% Sessió de Test, 80% codi final.

```

Sessió 1
=========
- 19 de d'abril [Sessió 1](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_1.md)

Sessió 2
=========
- 26 d'abril [Sessió 2](https://github.com/SoftwareDistribuitUB-2023/Practica2/blob/main/Sessio_2.md)

Sessió 3
=========
- 3 de Maig [Sessió 3](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_3.md)

Sessió 4
=========
- 4 de Maig [Sessió 4](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_4.md)

Sessió 5
=========
- 10 de Maig [Sessió 5](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_5.md)

Sessió 6
=========
- 18 de Maig [Sessió 6](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_6.md)

Sessió de Test
=========
- 24 de Maig [Sessió Test](https://github.com/SoftwareDistribuitUB-2023/P2/blob/main/Sessio_Test.md)

