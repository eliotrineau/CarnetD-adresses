import sqlite3
from tkinter import *
from tkinter import filedialog
import customtkinter
import re

# Macros pour les couleurs :
vert = '#9BB370'
bleu = '#2D5366'
bleufonce = '#3668A0'

fenetre = customtkinter.CTk()
fenetre.attributes('-fullscreen',True)
fenetre.title("Carnet d'adresses")
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")
fenetre.resizable(height=False,width=False)

# Macros pour la taille de l'écran :
screenX = fenetre.winfo_screenwidth()
screenY = fenetre.winfo_screenheight()

conn = sqlite3.connect('BDDCarnet.db')

cursor = conn.cursor() # permet de manipuler la bdd

cursor.execute("""CREATE TABLE IF NOT EXISTS carnetAdresse (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            prenom TEXT,
            email TEXT,
            telephone TEXT
            )""")

#<-------------------------------Fonctions pour l'actualisation de l'affichage----------------------------------------->

def supprimerContactLabels():
    for label in labelsContacts:
        label.destroy()

def actualiserAffichage():
    supprimerContactLabels() 
    afficherContacts()
    
#<-------------------------------Fonctions pour chercher un contact dans la base de données----------------------------------------->

def chercherC(nom, prenom):
    with conn:
        recherche = "SELECT * FROM carnetAdresse WHERE nom = ? AND prenom = ?"
        cursor.execute(recherche, (nom, prenom))
    return cursor.fetchone()

def boutonChercherC():
    divChercherContact = customtkinter.CTkFrame(fenetre)
    divChercherContact.place(x=screenX-screenX/3.35, y=screenY-screenY/2.45)

    labelzonesNomPrenomEmailTelephone = customtkinter.CTkLabel(divChercherContact, text='Remplir les informations du contact à chercher')
    labelzonesNomPrenomEmailTelephone.grid(row=0, column=0, columnspan=2, pady=5, padx=20)

    inputNom = StringVar()
    zoneDeTexteNom = customtkinter.CTkEntry(divChercherContact, textvariable=inputNom)
    zoneDeTexteNom.grid(row=1, column=0, padx=10, pady=5)
    zoneDeTexteNom.insert(0, "Nom")
    
    inputPrenom = StringVar()
    zoneDeTextePrenom = customtkinter.CTkEntry(divChercherContact, textvariable=inputPrenom)
    zoneDeTextePrenom.grid(row=1, column=1, padx=10, pady=5)
    zoneDeTextePrenom.insert(0, "Prénom")
    
    labelTrouver = customtkinter.CTkLabel(divChercherContact, text="Le contact existe")
    labelPasTrouver = customtkinter.CTkLabel(divChercherContact, text="Le contact n'existe pas")
    erreurLabel = customtkinter.CTkLabel(divChercherContact, text='Veuillez remplir correctement les champs de caractère !')
    
    def chercherContactInput():
        nonlocal erreurLabel
        erreurLabel.grid_forget()
        nonlocal labelTrouver
        labelTrouver.grid_forget()
        nonlocal labelPasTrouver
        labelPasTrouver.grid_forget()
        
        nom = inputNom.get().strip()
        prenom = inputPrenom.get().strip()
        
        if (nom != "Nom" and prenom != "Prénom") and (nom.strip() != "" and prenom.strip() != ""):
            contact = chercherC(nom, prenom)  # Passage de nom et prénom à la fonction chercherC
            if contact:
                zoneDeTexteNom.delete(0, 'end')
                zoneDeTexteNom.insert(0, "Nom")
                zoneDeTextePrenom.delete(0, 'end')
                zoneDeTextePrenom.insert(0, "Prénom")
                afficherContacts()
                labelTrouver.grid(row=3, column=0, columnspan=2, pady=5)
            else:
                labelPasTrouver.grid(row=3, column=0, columnspan=2, pady=5)
        else:
            erreurLabel.grid(row=3, column=0, columnspan=2, pady=5)
    
    boutonValidation = customtkinter.CTkButton(divChercherContact, text='Chercher le contact', command=chercherContactInput)
    boutonValidation.grid(row=2, column=0, columnspan=2, pady=10)



#<-------------------------------Fonctions pour modifier un contact dans la base de données----------------------------------------->

def modifierC(nom, prenom, email, telephone, nouveauNom=None, nouveauPrenom=None, nouvelEmail=None, nouveauTelephone=None):
    recherche = "SELECT * FROM carnetAdresse WHERE nom = ? AND prenom = ? AND email = ? AND telephone = ?"
    cursor.execute(recherche, (nom, prenom, email, telephone))
    contact = cursor.fetchone()

    if contact:
        modifier = "UPDATE carnetAdresse SET"
        nouvellesValeurs = []
        lignes = []

        if nouveauNom is not None:
            nouvellesValeurs.append(" nom = ?")
            lignes.append(nouveauNom)
        if nouveauPrenom is not None:
            nouvellesValeurs.append(" prenom = ?")
            lignes.append(nouveauPrenom)
        if nouvelEmail is not None:
            nouvellesValeurs.append(" email = ?")
            lignes.append(nouvelEmail)
        if nouveauTelephone is not None:
            nouvellesValeurs.append(" telephone = ?")
            lignes.append(nouveauTelephone)

        if nouvellesValeurs:
            modifier += ",".join(nouvellesValeurs) + " WHERE nom = ? AND prenom = ? AND email = ? AND telephone = ?"
            # Ajout des anciens paramètres pour la clause WHERE
            lignes.extend([nom, prenom, email, telephone])
            with conn:
                cursor.execute(modifier, lignes)
                actualiserAffichage()
    else:
        print("Le contact n'existe pas dans la base de données.")



def boutonModifierUnC():
    divModifierContact = customtkinter.CTkFrame(fenetre)
    divModifierContact.place(x=screenX-screenX/3.35,y=screenY/12+2*(screenY/24)-screenY/26)

    labelzonesNomPrenomEmailTelephone = customtkinter.CTkLabel(divModifierContact, text='Remplir les informations du contact à ajouter')
    labelzonesNomPrenomEmailTelephone.grid(row=0, column=0, columnspan=2, pady=5, padx=20)

    inputAncienNom = StringVar()
    zoneDeTexteAncienNom = customtkinter.CTkEntry(divModifierContact, textvariable=inputAncienNom)
    zoneDeTexteAncienNom.grid(row=1, column=0, padx=10, pady=20)
    zoneDeTexteAncienNom.insert(0, "ancien Nom")
    inputAncienPrenom = StringVar()
    zoneDeTexteAncienPrenom = customtkinter.CTkEntry(divModifierContact, textvariable=inputAncienPrenom)
    zoneDeTexteAncienPrenom.grid(row=2, column=0, padx=10, pady=20)
    zoneDeTexteAncienPrenom.insert(0, "ancien Prénom")
    inputAncienEmail = StringVar()
    zoneDeTexteAncienEmail = customtkinter.CTkEntry(divModifierContact, textvariable=inputAncienEmail)
    zoneDeTexteAncienEmail.grid(row=3, column=0, padx=10, pady=20)
    zoneDeTexteAncienEmail.insert(0, "ancien E-mail")
    inputAncienTelephone = StringVar()
    zoneDeTexteAncienTelephone = customtkinter.CTkEntry(divModifierContact, textvariable=inputAncienTelephone)
    zoneDeTexteAncienTelephone.grid(row=4, column=0, padx=10, pady=20)
    zoneDeTexteAncienTelephone.insert(0, "ancien Téléphone")

    inputNouveauNom = StringVar()
    zoneDeTexteNouveauNom = customtkinter.CTkEntry(divModifierContact, textvariable=inputNouveauNom)
    zoneDeTexteNouveauNom.grid(row=1, column=1, padx=10, pady=20)
    zoneDeTexteNouveauNom.insert(0, "nouveau Nom")
    inputNouveauPrenom = StringVar()
    zoneDeTexteNouveauPrenom = customtkinter.CTkEntry(divModifierContact, textvariable=inputNouveauPrenom)
    zoneDeTexteNouveauPrenom.grid(row=2, column=1, padx=10, pady=20)
    zoneDeTexteNouveauPrenom.insert(0, "nouveau Prénom")
    inputnouvelEmail = StringVar()
    zoneDeTextenouvelEmail = customtkinter.CTkEntry(divModifierContact, textvariable=inputnouvelEmail)
    zoneDeTextenouvelEmail.grid(row=3, column=1, padx=10, pady=20)
    zoneDeTextenouvelEmail.insert(0, "nouvel E-mail")
    inputNouveauTelephone = StringVar()
    zoneDeTexteNouveauTelephone = customtkinter.CTkEntry(divModifierContact, textvariable=inputNouveauTelephone)
    zoneDeTexteNouveauTelephone.grid(row=4, column=1, padx=10, pady=20)
    zoneDeTexteNouveauTelephone.insert(0, "nouveau Téléphone")

    erreurLabel = customtkinter.CTkLabel(divModifierContact, text='Veuillez remplir correctement les champs de caractère !')
    def modifierContactInput():
        nonlocal erreurLabel
        erreurLabel.grid_forget()
        ancienNom = inputAncienNom.get().strip()
        ancienPrenom = inputAncienPrenom.get().strip()
        ancienEmail = inputAncienEmail.get().strip()
        ancienTelephone = inputAncienTelephone.get().strip()
        nouveauNom = inputNouveauNom.get().strip()
        nouveauPrenom = inputNouveauPrenom.get().strip()
        nouvelEmail = inputnouvelEmail.get().strip()
        nouveauTelephone = inputNouveauTelephone.get().strip()
        nouveauNomVerif = re.match(r'^[a-zA-Z- ]+$',nouveauNom)
        nouveauPrenomVerif = re.match(r'^[a-zA-Z- ]+$',nouveauPrenom)
        nouvelEmailVerif = re.match(r'^[a-z]+\.[a-z]+@edu\.[a-z]+\.fr$',nouvelEmail)
        if nouvelEmailVerif:
            emailVerifOrdre = nouvelEmail.split('@')
            if len(emailVerifOrdre) == 2:
                domaine = emailVerifOrdre[1]
                if domaine.startswith('edu.') and domaine.endswith('.fr'):
                    prenomNom = emailVerifOrdre[0].split('.')
                    if len(prenomNom) == 2:
                        if prenomNom[0] == nouveauPrenom and prenomNom[1] == nouveauNom:
                            nouvelEmailVerif = True
                        else:
                            nouvelEmailVerif = False
                    else:
                        nouvelEmailVerif = False
                else:
                    nouvelEmailVerif = False
            else:
                nouvelEmailVerif = False
        nouveauTelephoneVerif = re.match(r'^\+33[0-9]{9}$', nouveauTelephone)
        if (ancienNom != "ancien Nom" and ancienPrenom != "ancien Prénom" and ancienEmail != "ancien E-mail" and ancienTelephone != "ancien Téléphone" and nouveauNom != "nouveau Nom" and nouveauPrenom != "nouveau Prénom" and nouvelEmail != "nouvel E-mail" and nouveauTelephone != "nouveau Téléphone" and nouveauNomVerif and nouveauPrenomVerif and nouvelEmailVerif and nouveauTelephoneVerif) and (ancienNom.strip() != "" and ancienPrenom.strip() != "" and ancienEmail.strip() != "" and ancienTelephone.strip() != "" and nouveauNom.strip() != "" and nouveauPrenom.strip() != "" and nouvelEmail.strip() != "" and nouveauTelephone.strip() != ""):
            modifierC(ancienNom,ancienPrenom,ancienEmail,ancienTelephone,nouveauNom,nouveauPrenom,nouvelEmail,nouveauTelephone)
            zoneDeTexteAncienNom.delete(0, 'end')
            zoneDeTexteAncienNom.insert(0, "ancien Nom")
            zoneDeTexteAncienPrenom.delete(0, 'end')
            zoneDeTexteAncienPrenom.insert(0, "ancien Prénom")
            zoneDeTexteAncienEmail.delete(0, 'end')
            zoneDeTexteAncienEmail.insert(0, "ancien E-mail")
            zoneDeTexteAncienTelephone.delete(0, 'end')
            zoneDeTexteAncienTelephone.insert(0, "ancien Téléphone")
            zoneDeTexteNouveauNom.delete(0, 'end')
            zoneDeTexteNouveauNom.insert(0, "nouveau Nom")
            zoneDeTexteNouveauPrenom.delete(0, 'end')
            zoneDeTexteNouveauPrenom.insert(0, "nouveau Prénom")
            zoneDeTextenouvelEmail.delete(0, 'end')
            zoneDeTextenouvelEmail.insert(0, "nouvel E-mail")
            zoneDeTexteNouveauTelephone.delete(0, 'end')
            zoneDeTexteNouveauTelephone.insert(0, "nouveau Téléphone")
            afficherContacts()
        else: erreurLabel.grid(row=7, column=0, columnspan=2, pady=10)        
    boutonValidation = customtkinter.CTkButton(divModifierContact, text='Modifier le contact', command=modifierContactInput)
    boutonValidation.grid(row=5, column=0, columnspan=2, pady=10)

#<-------------------------------Fonctions pour ajouter un contact dans la base de données----------------------------------------->

def ajouterC(nom,prenom,email,telephone):
    with conn: 
        cursor.execute("INSERT INTO carnetAdresse (nom,prenom,email,telephone) VALUES (?,?,?,?)",(nom,prenom,email,telephone))
    actualiserAffichage()

def boutonAjouterUnC():
    divAjouter = customtkinter.CTkFrame(fenetre)
    divAjouter.place(x=40,y=screenY-screenY/5.5)
    labelzonesNomPrenomEmailTelephone = customtkinter.CTkLabel(divAjouter, text='Remplir les informations du contact à ajouter')
    labelzonesNomPrenomEmailTelephone.grid(row=0, column=0, columnspan=2, pady=5, padx=20)
    inputNom = StringVar()
    zoneDeTexteNom = customtkinter.CTkEntry(divAjouter, textvariable=inputNom)
    zoneDeTexteNom.grid(row=1, column=0, padx=21)
    zoneDeTexteNom.insert(0, "Nom")
    inputPrenom = StringVar()
    zoneDeTextePrenom = customtkinter.CTkEntry(divAjouter, textvariable=inputPrenom)
    zoneDeTextePrenom.grid(row=1, column=1, padx=21)
    zoneDeTextePrenom.insert(0, "Prénom")
    inputEmail = StringVar()
    zoneDeTexteEmail = customtkinter.CTkEntry(divAjouter, textvariable=inputEmail)
    zoneDeTexteEmail.grid(row=1, column=2, padx=21)
    zoneDeTexteEmail.insert(0, "E-mail")
    inputTelephone = StringVar()
    zoneDeTexteTelephone = customtkinter.CTkEntry(divAjouter, textvariable=inputTelephone)
    zoneDeTexteTelephone.grid(row=1, column=3, padx=21)
    zoneDeTexteTelephone.insert(0, "Téléphone")
    erreurLabel = customtkinter.CTkLabel(divAjouter, text='Veuillez remplir correctement les champs de caractère !')
    def ajouterContactInput():
        nonlocal erreurLabel
        erreurLabel.grid_forget()
        nom = inputNom.get().strip()
        nomVerif = re.match(r'^[a-zA-Z- ]+$',nom)
        prenom = inputPrenom.get().strip()
        prenomVerif = re.match(r'^[a-zA-Z- ]+$',prenom)
        email = inputEmail.get().strip()
        emailVerif = re.match(r'^[a-z]+\.[a-z]+@edu\.[a-z]+\.fr$',email)
        if emailVerif:
            emailVerifOrdre = email.split('@')
            if len(emailVerifOrdre) == 2:
                domaine = emailVerifOrdre[1]
                if domaine.startswith('edu.') and domaine.endswith('.fr'):
                    prenomNom = emailVerifOrdre[0].split('.')
                    if len(prenomNom) == 2:
                        if prenomNom[0] == prenom and prenomNom[1] == nom:
                            emailVerif = True
                        else:
                            emailVerif = False
                    else:
                        emailVerif = False
                else:
                    emailVerif = False
            else:
                emailVerif = False
        telephone = inputTelephone.get().strip()
        telephoneVerif = re.match(r'^\+33[0-9]{9}$', telephone)
        if (nom != "Nom" and prenom != "Prénom" and email != "E-mail" and telephone != "Téléphone" and nomVerif and prenomVerif and telephoneVerif and emailVerif) and ( nom.strip() != "" and prenom.strip() != "" and email.strip() != "" and telephone.strip() != ""):
            ajouterC(nom,prenom,email,telephone)
            zoneDeTexteNom.delete(0, 'end')
            zoneDeTexteNom.insert(0, "Nom")
            zoneDeTextePrenom.delete(0, 'end')
            zoneDeTextePrenom.insert(0, "Prénom")
            zoneDeTexteEmail.delete(0, 'end')
            zoneDeTexteEmail.insert(0, "E-mail")
            zoneDeTexteTelephone.delete(0, 'end')
            zoneDeTexteTelephone.insert(0, "Téléphone")
        else: erreurLabel.grid(row=0, column=2, columnspan=4, pady=5, padx=10)
    boutonValidation = customtkinter.CTkButton(divAjouter, text='Ajouter le contact', command=ajouterContactInput)
    boutonValidation.grid(row=2, column=0, columnspan=4, pady=10)


#<-------------------------------Fonctions pour supprimer un contact spécifique de la base de données----------------------------------------->

def supprimerC(nom, prenom):
    with conn:
        cursor.execute("DELETE FROM carnetAdresse WHERE nom = ? AND prenom = ?", (nom, prenom))
    actualiserAffichage()

def boutonSupprimerUnC():
    divSupprimer = customtkinter.CTkFrame(fenetre)
    divSupprimer.place(x=screenX-screenX/3.45,y=screenY-screenY/5.5)
    labelzonesNomPrenom = customtkinter.CTkLabel(divSupprimer, text='Remplir les informations du contact à supprimer')
    labelzonesNomPrenom.grid(row=0, column=0, columnspan=2, pady=5)
    inputNom = StringVar()
    zoneDeTexteNom = customtkinter.CTkEntry(divSupprimer, textvariable=inputNom)
    zoneDeTexteNom.grid(row=1, column=0, padx=10)
    zoneDeTexteNom.insert(0, "Nom")
    inputPrenom = StringVar()
    zoneDeTextePrenom = customtkinter.CTkEntry(divSupprimer, textvariable=inputPrenom)
    zoneDeTextePrenom.grid(row=1, column=1, padx=10)
    zoneDeTextePrenom.insert(0, "Prénom")
    erreurLabel = customtkinter.CTkLabel(divSupprimer, text="Le contact n'existe pas ou est mal saisi")
    def supprimerContactInput():
        nonlocal erreurLabel
        erreurLabel.grid_forget()
        nom = inputNom.get().strip()
        prenom = inputPrenom.get().strip()
        if (nom != "Nom" and prenom != "Prénom") and (nom.strip() != "" and prenom.strip() != ""):
            cursor.execute("SELECT * FROM carnetAdresse WHERE nom = ? AND prenom = ?", (nom, prenom))
            contact = cursor.fetchone()
            if contact:
                supprimerC(nom, prenom)
                zoneDeTexteNom.delete(0, 'end')
                zoneDeTexteNom.insert(0, "Nom")
                zoneDeTextePrenom.delete(0, 'end')
                zoneDeTextePrenom.insert(0, "Prénom")
                afficherContacts()
            else: erreurLabel.grid(row=3, column=0, columnspan=2, pady=5)
        else : erreurLabel.grid(row=3, column=0, columnspan=2, pady=5)
    boutonValidation = customtkinter.CTkButton(divSupprimer, text='Supprimer le contact', command=supprimerContactInput)
    boutonValidation.grid(row=2, column=0, columnspan=2, pady=10)

#<-------------------------------Fonction pour supprimer la base de données de contacts----------------------------------------->

def supprimerAllC():
    with conn:
        cursor.execute("DELETE FROM carnetAdresse")
    actualiserAffichage()
    

def boutonSupprimerAllC():
    boutonSupprimerTout = customtkinter.CTkButton(fenetre, text='Supprimer tous les contacts', command=supprimerAllC)
    boutonSupprimerTout.place(x=screenX-screenX/4,y=screenY/12+screenY/24-screenY/26)
    boutonAfficherBDD()
    afficherContacts()


#<-------------------------------Fonctions pour afficher la base de données de contacts----------------------------------------->

def afficherBDD():
    cursor.execute("SELECT * FROM carnetAdresse")
    return cursor.fetchall() 


def afficherContacts():
    supprimerContactLabels()
    labelsContacts.clear() 
    contacts = afficherBDD()  
    divScrollable = customtkinter.CTkScrollableFrame(fenetre, width=screenX/2.1, height=screenY/2, label_text="Liste de contacts")
    divScrollable.place(x=screenX/28, y=screenY/6)
    for contact in contacts:
        elements = f"Nom: {contact[1]}  |  Prénom: {contact[2]}  |  E-mail: {contact[3]}  |  Téléphone: {contact[4]}"
        labelContact = customtkinter.CTkLabel(divScrollable, text=elements, bg_color=bleufonce, width=screenX/1.8)
        labelContact.pack(pady=5)
        labelsContacts.append(labelContact)

def boutonAfficherBDD():
    boutonAfficherBDD = customtkinter.CTkButton(fenetre, text="Afficher les contacts", command=afficherContacts)
    boutonAfficherBDD.place(x=screenX/4.35, y=screenY/12)

#<-------------------------------Fonction pour importer un fichier de contacts----------------------------------------->

def correction(fichier):
    lignes_corrigees = []
    with open(fichier, 'r') as file:
        lignes = file.readlines()
        for ligne in lignes:
            contact = ligne.strip().split(',')
            if len(contact) != 4:
                if len(contact) > 4:
                    corrected_line = [','.join(contact[:2]), *contact[2:]]
                    lignes_corrigees.append(','.join(corrected_line))
                elif len(contact) < 4:
                    print(f"Ignorer la ligne incomplète : {ligne.strip()}")
            else:
                lignes_corrigees.append(ligne.strip())
    fichier_temporaire = 'fichier_corrigé.txt'
    with open(fichier_temporaire, 'w') as temp_file:
        temp_file.write('\n'.join(lignes_corrigees))

    return fichier_temporaire


def choisirFichier():
    fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        fichierCorriger = correction(fichier)
        with open(fichierCorriger, 'r') as file:
            lignes = file.readlines()
            for ligne in lignes:
                contact = ligne.strip().split(',')
                cursor.execute("INSERT INTO carnetAdresse (nom,prenom,email,telephone) VALUES (?,?,?,?)", (contact[0], contact[1], contact[2], contact[3]))
        conn.commit()
        actualiserAffichage()


def boutonAjouterFichierContact():
    boutonAjouterListeContact = customtkinter.CTkButton(fenetre, text="Choisir un fichier", command=choisirFichier)
    boutonAjouterListeContact.place(x=screenX-screenX/4.25,y=screenY/12-screenY/26)

#<-------------------------------Appels des fonctions d'affichage Tkinter----------------------------------------->

labelsContacts = [] 

boutonAjouterFichierContact()
boutonModifierUnC()
boutonChercherC()
boutonAfficherBDD()
boutonSupprimerAllC()
boutonSupprimerUnC()
boutonAjouterUnC()

fenetre.mainloop()
conn.close()
