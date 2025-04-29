import requests
import os
import json
import xml.etree.ElementTree as ET
import replicate

class ApiHandler:
    """Gère les interactions avec les différentes API."""

    def __init__(self):
        # Pour Infermedica (existant)
        self.infermedica_app_id = os.environ.get('INFERMEDICA_APP_ID')
        self.infermedica_app_key = os.environ.get('INFERMEDICA_APP_KEY')
        self.infermedica_base_url = "https://api.infermedica.com/v3"

        # Pour MedlinePlus (commenté car remplacé)
        # self.medline_base_url = "https://wsearch.nlm.nih.gov/ws/query"

        # Pour Replicate
        self.replicate_api_token = os.environ.get('REPLICATE_API_TOKEN')

        # --- Vérifications des clés API ---
        if not self.infermedica_app_id or not self.infermedica_app_key:
            print("ATTENTION : Les clés API Infermedica (INFERMEDICA_APP_ID, INFERMEDICA_APP_KEY) ne sont pas définies.")
            print("La fonctionnalité de diagnostic ne fonctionnera pas.")

        if not self.replicate_api_token:
            print("ATTENTION : Le token API Replicate (REPLICATE_API_TOKEN) n'est pas défini.")
            print("La fonctionnalité de recherche avancée ne fonctionnera pas.")

    # --- Méthodes pour Infermedica --- (inchangées)
    def get_diagnosis(self, sex, age_struct, evidence):
        """Interroge l'API Infermedica pour obtenir un diagnostic."""
        if not self.infermedica_app_id or not self.infermedica_app_key:
            print("Erreur: Clés API Infermedica manquantes.")
            return None

        url = f"{self.infermedica_base_url}/diagnosis"
        headers = {
            'App-Id': self.infermedica_app_id,
            'App-Key': self.infermedica_app_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "sex": sex.lower(),
            "age": age_struct, # Attendu comme {'value': 50, 'unit': 'year'}
            "evidence": evidence,
             # Optionnel : ajouter des paramètres supplémentaires ici si nécessaire
             # "extras": {"disable_groups": True}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20) # Timeout ajouté
            response.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx, 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'appel à l'API Infermedica: {e}")
            if response is not None:
                print(f"Réponse API ({response.status_code}): {response.text}")
            return None
        except json.JSONDecodeError:
            print("Erreur: La réponse de l'API Infermedica n'est pas un JSON valide.")
            print(f"Réponse brute: {response.text}")
            return None

    # --- Méthodes pour MedlinePlus --- (commentée)
    # def get_medline_info(self, search_term):
    #     """Interroge l'API MedlinePlus Health Topics pour obtenir des informations."""
    #     params = {
    #         'db': 'healthTopics',
    #         'term': search_term,
    #         'retmax': 1 # On ne veut que le premier résultat le plus pertinent
    #     }
    #
    #     try:
    #         response = requests.get(self.medline_base_url, params=params, timeout=15)
    #         response.raise_for_status()
    #
    #         # Analyser le XML
    #         try:
    #             root = ET.fromstring(response.content)
    #             # Trouver le premier élément 'document'
    #             document = root.find('.//document')
    #             if document is not None:
    #                 # Extraire le titre et le snippet (résumé)
    #                 title_elem = document.find(".//content[@name='title']")
    #                 snippet_elem = document.find(".//content[@name='snippet']")
    #                 url_elem = document.find(".//content[@name='url']")
    #
    #                 title = title_elem.text if title_elem is not None and title_elem.text else "Titre non trouvé"
    #                 snippet = snippet_elem.text if snippet_elem is not None and snippet_elem.text else "Résumé non disponible."
    #                 url = url_elem.text if url_elem is not None and url_elem.text else None
    #
    #                 result_text = f"**{title}**\n\n{snippet}"
    #                 if url:
    #                      result_text += f"\n\n_Source : {url}_"
    #                 return result_text
    #             else:
    #                 return f"Aucun résultat trouvé sur MedlinePlus pour '{search_term}'."
    #
    #         except ET.ParseError:
    #             print(f"Erreur lors de l'analyse XML de la réponse MedlinePlus pour '{search_term}'.")
    #             print(f"Réponse brute: {response.text}")
    #             return "Erreur: Impossible d'analyser la réponse de l'API MedlinePlus."
    #
    #     except requests.exceptions.RequestException as e:
    #         print(f"Erreur lors de l'appel à l'API MedlinePlus pour '{search_term}': {e}")
    #         return "Erreur: Impossible de contacter l'API MedlinePlus. Vérifiez votre connexion internet."


    # --- Méthode pour Replicate (LLM) --- (nouvelle)
    def get_llm_answer(self, question):
        """Interroge un LLM via Replicate pour obtenir une réponse à une question."""
        if not self.replicate_api_token:
            return "Erreur: Le token API Replicate n'est pas configuré. Impossible d'utiliser la recherche avancée."

        try:
            # Définir le modèle à utiliser (peut être changé)
            model_ref = "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e"
            
            # Exécuter le modèle
            # Note: Le format 'input' dépend du modèle choisi sur Replicate.
            # Pour llama-2-chat, on utilise souvent un prompt structuré.
            output_iterator = replicate.run(
                model_ref,
                input={
                    "prompt": f"Question: {question}\nAnswer:", # Prompt simple, peut être amélioré
                    "temperature": 0.75, # Contrôle la créativité/aléatoire
                    "max_new_tokens": 500 # Limite la longueur de la réponse
                }
            )
            
            # Concaténer les morceaux de la réponse (car Replicate peut streamer la sortie)
            full_response = "".join(output_iterator)
            
            return full_response if full_response else "Le modèle n'a pas fourni de réponse."

        except replicate.exceptions.ReplicateError as e:
            print(f"Erreur de l'API Replicate: {e}")
            return f"Erreur lors de la communication avec l'API Replicate: {e}"
        except Exception as e:
            print(f"Erreur inattendue lors de l'appel à Replicate: {e}")
            return "Une erreur inattendue est survenue lors de la recherche avancée."


# Exemple d'utilisation (pour tester directement si besoin)
if __name__ == '__main__':
    # Charger les variables d'env pour tester
    from dotenv import load_dotenv
    load_dotenv()

    handler = ApiHandler()

    # --- Test Replicate --- (nécessite REPLICATE_API_TOKEN)
    print("--- Test Replicate LLM --- (nécessite REPLICATE_API_TOKEN)")
    if handler.replicate_api_token:
        llm_question = "What are the common symptoms of type 2 diabetes?"
        print(f"Question: {llm_question}")
        llm_answer = handler.get_llm_answer(llm_question)
        print(f"Réponse: {llm_answer}")
    else:
        print("Skipping Replicate test: REPLICATE_API_TOKEN non trouvé.")
    print("\n---")

    # --- Test Infermedica --- (nécessite des clés API)
    print("--- Test Infermedica --- (nécessite des clés API)")
    if handler.infermedica_app_id and handler.infermedica_app_key:
        evidence_test = [
            {"id": "s_21", "choice_id": "present"}, # Fever
            {"id": "s_98", "choice_id": "present"}  # Headache
        ]
        age_test = {"value": 30, "unit": "year"}
        sex_test = "male"
        diag = handler.get_diagnosis(sex_test, age_test, evidence_test)
        if diag:
            print("Diagnostic Infermedica reçu:")
            print(json.dumps(diag, indent=2))
        else:
            print("Échec de la réception du diagnostic Infermedica.")
    else:
        print("Skipping Infermedica test: Clés API non trouvées.")
