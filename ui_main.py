import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QFormLayout, QGroupBox, QMessageBox, QTabWidget, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QLocale

# Importer le gestionnaire d'API
from api_handler import ApiHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MedDiag App - Diagnostic Chirurgical Intelligent")
        self.setGeometry(100,100, 700, 550)

        # Définir la locale pour QDoubleSpinBox (utilise '.' comme séparateur décimal)
        self.setLocale(QLocale(QLocale.C))

        # Initialiser le gestionnaire d'API
        self.api_handler = ApiHandler()

        # --- Création du QTabWidget ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- Création des onglets ---
        self.tab_accueil = QFrame() # Utiliser QFrame comme conteneur simple
        self.tab_patient = QFrame()
        self.tab_diagnostic = QFrame()
        self.tab_recherche_info = QFrame()

        # Ajouter les onglets au QTabWidget
        self.tabs.addTab(self.tab_accueil, "Accueil")
        self.tabs.addTab(self.tab_patient, "Informations Patient")
        self.tabs.addTab(self.tab_diagnostic, "Diagnostic")
        self.tabs.addTab(self.tab_recherche_info, "Recherche Info")

        # Créer le contenu de chaque onglet
        self._create_accueil_tab()
        self._create_patient_tab()
        self._create_diagnostic_tab()
        self._create_recherche_info_tab()

    def _create_accueil_tab(self):
        """Crée le contenu de l'onglet Accueil (version améliorée)."""
        layout = QVBoxLayout(self.tab_accueil)
        layout.setContentsMargins(20, 20, 20, 20) # Ajouter des marges
        layout.setAlignment(Qt.AlignTop) # Aligner en haut

        # Titre principal
        title_label = QLabel("<h1>Bienvenue sur MedDiag App</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("margin-bottom: 25px;") # Espace après le titre

        # Message d'introduction
        intro_text = ("<p>Votre assistant intelligent pour le pré-diagnostic chirurgical.</p>"
                      "<p>Veuillez naviguer à travers les onglets pour fournir les informations nécessaires :</p>")
        intro_label = QLabel(intro_text)
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignLeft)
        intro_label.setStyleSheet("font-size: 11pt; margin-bottom: 15px;")

        # Instructions (un peu plus structurées)
        instructions_text = ("<ul>"
                             "<li><b>Informations Patient</b> : Renseignez les détails démographiques et les antécédents médicaux pertinents.</li>"
                             "<li><b>Diagnostic</b> : Entrez les identifiants des symptômes observés (conformément à la nomenclature Infermedica) pour lancer l'analyse.</li>"
                             "</ul>"
                             "<p><i>Assurez-vous que vos clés API sont correctement configurées pour utiliser les fonctionnalités de diagnostic.</i></p>")
        instructions_label = QLabel(instructions_text)
        instructions_label.setWordWrap(True)
        instructions_label.setAlignment(Qt.AlignLeft)
        instructions_label.setStyleSheet("font-size: 10pt;")

        layout.addWidget(title_label)
        layout.addWidget(intro_label)
        layout.addWidget(instructions_label)
        layout.addStretch() # Pousse le contenu vers le haut

        self.tab_accueil.setLayout(layout)


    def _create_patient_tab(self):
        """Crée le contenu de l'onglet Informations Patient."""
        main_layout = QVBoxLayout(self.tab_patient)

        # --- Section Informations Générales ---
        general_group = QGroupBox("Informations Générales")
        general_layout = QFormLayout()

        self.age_input = QSpinBox()
        self.age_input.setRange(0, 120)
        self.age_input.setValue(30)
        general_layout.addRow("Âge (ans) :", self.age_input)

        self.sex_input = QComboBox()
        self.sex_input.addItems(["male", "female"])
        general_layout.addRow("Sexe Biologique :", self.sex_input)

        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(0.0, 500.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.setValue(70.0)
        general_layout.addRow("Poids :", self.weight_input)

        self.blood_group_input = QComboBox()
        self.blood_group_input.addItems(["Non spécifié", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        general_layout.addRow("Groupe Sanguin :", self.blood_group_input)

        general_group.setLayout(general_layout)
        main_layout.addWidget(general_group)

        # --- Section Antécédents ---
        history_group = QGroupBox("Antécédents Médicaux")
        history_layout = QVBoxLayout()

        history_layout.addWidget(QLabel("Maladies génétiques ou chroniques connues :"))
        self.genetic_history_input = QTextEdit()
        self.genetic_history_input.setPlaceholderText("Listez ici les conditions préexistantes pertinentes...")
        self.genetic_history_input.setFixedHeight(80) # Limiter la hauteur initiale
        history_layout.addWidget(self.genetic_history_input)

        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)

        main_layout.addStretch() # Pousse les éléments vers le haut
        self.tab_patient.setLayout(main_layout)


    def _create_diagnostic_tab(self):
        """Crée le contenu de l'onglet Diagnostic."""
        main_layout = QVBoxLayout(self.tab_diagnostic)

        # --- Section Symptômes ---
        symptoms_group = QGroupBox("Symptômes Actuels (IDs Infermedica)")
        symptoms_layout = QVBoxLayout()
        self.symptoms_input = QTextEdit()
        self.symptoms_input.setPlaceholderText(
             "Entrez les ID de symptômes/observations (ex: s_1193, s_13, p_8) séparés par des virgules.\n"
             "Consultez la documentation Infermedica pour les IDs valides."
        )
        symptoms_layout.addWidget(QLabel("Entrez les IDs des symptômes observés (séparés par des virgules) :"))
        symptoms_layout.addWidget(self.symptoms_input)
        symptoms_group.setLayout(symptoms_layout)
        main_layout.addWidget(symptoms_group)

        # --- Bouton Diagnostic ---
        self.diagnose_button = QPushButton("Lancer le Diagnostic")
        self.diagnose_button.setStyleSheet("QPushButton { background-color: #007bff; color: white; padding: 10px 20px; border-radius: 5px; font-size: 12pt;} QPushButton:hover { background-color: #0056b3; } QPushButton:pressed { background-color: #004085; }")
        self.diagnose_button.clicked.connect(self.handle_diagnosis) # La méthode handle_diagnosis sera mise à jour ensuite
        # Utiliser QHBoxLayout pour centrer le bouton
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.diagnose_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout) # Ajouter le layout du bouton au layout principal

        # --- Section Résultats ---
        results_group = QGroupBox("Résultats du Diagnostic")
        results_layout = QVBoxLayout()
        self.results_output = QTextEdit()
        self.results_output.setObjectName("results_output") # Pour ciblage QSS
        self.results_output.setReadOnly(True)
        self.results_output.setPlaceholderText("Le diagnostic de l'API apparaîtra ici...")
        results_layout.addWidget(self.results_output)
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group) # Ajouté au QVBoxLayout principal

        self.tab_diagnostic.setLayout(main_layout)


    def _create_recherche_info_tab(self):
        """Crée le contenu de l'onglet Recherche Info."""
        layout = QVBoxLayout(self.tab_recherche_info)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignTop)

        # --- AVERTISSEMENT IMPORTANT ---
        warning_label = QLabel(
            "<font color='orange'><b>AVERTISSEMENT :</b> Les réponses fournies ici proviennent d'un modèle linguistique général "
            "et <b>NE constituent PAS un avis médical</b>. Les informations peuvent être inexactes, incomplètes ou obsolètes. "
            "Consultez TOUJOURS un professionnel de santé qualifié pour toute question médicale.</font>"
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("padding: 10px; border: 1px solid orange; background-color: #404040; margin-bottom: 15px;")
        layout.addWidget(warning_label)

        # Zone de recherche
        search_layout = QHBoxLayout()
        self.search_term_input = QLineEdit()
        self.search_term_input.setPlaceholderText("Entrez un terme médical (ex: diabète, aspirine)...")
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.handle_info_search)

        search_layout.addWidget(QLabel("Terme :"))
        search_layout.addWidget(self.search_term_input)
        search_layout.addWidget(self.search_button)

        # Zone de résultat
        self.info_results_output = QTextEdit()
        self.info_results_output.setReadOnly(True)
        self.info_results_output.setPlaceholderText("Les informations de MedlinePlus apparaîtront ici...")
        # Permettre à la zone de texte de s'étendre verticalement
        self.info_results_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addLayout(search_layout)
        layout.addWidget(QLabel("Résultats :"), alignment=Qt.AlignLeft)
        layout.addWidget(self.info_results_output)

        self.tab_recherche_info.setLayout(layout)

    def handle_diagnosis(self):
        """
        Récupère les entrées des différents onglets, appelle l'API et affiche les résultats.
        """
        # Récupération depuis l'onglet Patient
        age_value = self.age_input.value()
        sex_value = self.sex_input.currentText()
        weight_value = self.weight_input.value()
        blood_group = self.blood_group_input.currentText()
        genetic_history = self.genetic_history_input.toPlainText().strip()

        # Récupération depuis l'onglet Diagnostic
        symptoms_text = self.symptoms_input.toPlainText().strip()

        # Afficher les infos supplémentaires récupérées (pour débogage, ne sont pas envoyées à l'API pour l'instant)
        print("--- Informations Patient Supplémentaires (Non envoyées à l'API actuellement) ---")
        print(f"Poids: {weight_value} kg")
        print(f"Groupe Sanguin: {blood_group}")
        print(f"Antécédents: {genetic_history if genetic_history else 'Non spécifiés'}")
        print("--------------------------------------------------------------------------")


        # Validation simple des symptômes
        if not symptoms_text:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer au moins un ID de symptôme dans l'onglet 'Diagnostic'.")
            # Changer d'onglet pour montrer où est l'erreur
            self.tabs.setCurrentWidget(self.tab_diagnostic)
            self.symptoms_input.setFocus()
            return

        # Afficher un message de chargement
        self.results_output.setText("Diagnostic en cours, veuillez patienter...")
        self.tabs.setCurrentWidget(self.tab_diagnostic) # Assurer que l'onglet diagnostic est visible
        QApplication.processEvents() # Forcer la mise à jour de l'UI

        # --- Préparation des données 'evidence' pour l'API (inchangé pour l'instant) ---
        symptom_ids = [s.strip() for s in symptoms_text.split(',') if s.strip()]
        evidence = []
        valid_ids = True
        for symptom_id in symptom_ids:
            # Vérification simple du format de l'ID
            if symptom_id.startswith(('s_', 'p_', 'c_')):
                 evidence.append({"id": symptom_id, "choice_id": "present", "source": "initial"})
            else:
                 QMessageBox.warning(self, "Erreur de format", f"L'ID '{symptom_id}' ne semble pas être un ID de symptôme/facteur valide (devrait commencer par s_, p_, ou c_).")
                 self.results_output.setText("Erreur dans le format des IDs de symptômes.")
                 self.tabs.setCurrentWidget(self.tab_diagnostic)
                 self.symptoms_input.setFocus()
                 valid_ids = False
                 break # Sortir de la boucle si un ID est invalide

        if not valid_ids:
            return # Arrêter si un ID était invalide

        if not evidence:
             QMessageBox.warning(self, "Erreur de saisie", "Aucun ID de symptôme/facteur valide trouvé après traitement.")
             self.results_output.setText("Aucun symptôme/facteur valide fourni.")
             self.tabs.setCurrentWidget(self.tab_diagnostic)
             self.symptoms_input.setFocus()
             return

        age_struct = {"value": age_value, "unit": "year"}

        # --- Appel de l'API (inchangé) ---
        try:
            diagnostic_result = self.api_handler.get_diagnosis(sex_value, age_struct, evidence)

            # --- Affichage des résultats (inchangé) ---
            if diagnostic_result:
                output_text = f"--- Diagnostic Possible ---\n\n"
                if diagnostic_result.get("should_stop"):
                     output_text += "INFO: L'API suggère d'arrêter l'interrogatoire.\n\n"
                conditions = diagnostic_result.get("conditions", [])
                if conditions:
                    output_text += "Conditions Probables:\n"
                    for condition in conditions:
                        output_text += f"- {condition.get('common_name', 'Nom inconnu')} (ID: {condition.get('id', 'inconnu')}, Probabilité: {condition.get('probability', 0):.2f})\n"
                else:
                    output_text += "Aucune condition spécifique retournée par l'API.\n"
                # Optionnel: Afficher la réponse brute pour le débogage
                # output_text += "\n--- Réponse API brute ---\n"
                # output_text += json.dumps(diagnostic_result, indent=2, ensure_ascii=False)
                self.results_output.setText(output_text)
            else:
                # L'ApiHandler a déjà dû afficher une erreur dans la console
                self.results_output.setText("Échec de la récupération du diagnostic depuis l'API.\nVérifiez la console pour les détails (clés API, connexion, etc.).")

        except Exception as e: # Ajout de l'indentation correcte et de la clause except
            self.results_output.setText(f"Une erreur inattendue est survenue lors du traitement: {e}")
            print(f"Erreur inattendue dans handle_diagnosis: {e}")

        # Assurer que l'onglet diagnostic reste visible après traitement
        self.tabs.setCurrentWidget(self.tab_diagnostic)


    def handle_info_search(self):
        """Gère la recherche d'informations médicales via l'API LLM (Replicate)."""
        search_term = self.search_term_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un terme ou une question à rechercher.")
            return

        self.info_results_output.setText(f"Recherche d'une réponse pour '{search_term}' en cours (cela peut prendre quelques secondes)...")
        QApplication.processEvents() # Mettre à jour l'UI

        # --- Appel API LLM (Replicate) --- 
        try:
            # Utiliser la nouvelle méthode pour appeler le LLM
            result_text = self.api_handler.get_llm_answer(search_term)
            self.info_results_output.setText(result_text if result_text else "Aucune réponse obtenue du modèle.")
        except Exception as e:
            # Gérer les erreurs inattendues non capturées dans ApiHandler
            print(f"Erreur inattendue lors de la recherche LLM: {e}")
            self.info_results_output.setText(f"Une erreur inattendue est survenue : {e}")
        
        # S'assurer que l'onglet de recherche reste actif
        self.tabs.setCurrentWidget(self.tab_recherche_info)


if __name__ == '__main__':
    # Nécessaire si on lance ui_main.py directement pour tester
    app = QApplication(sys.argv)

    # Charger et appliquer le style QSS (si on teste ui_main.py seul)
    # Note: Normalement, le chargement se fait dans main.py
    style_path = "styles.qss"
    try:
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Attention: {style_path} non trouvé pour le test direct.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
