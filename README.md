# Matrice de chiffrage ESI - V15 Render / Supabase ready

Version web prete pour depot GitHub puis deploiement Render.

## Inclus

- Application web Python servie par `app.py`.
- Calculs actifs deja integres : T1, T1-T6, MRT, T1-T3 MRT, T a Glissieres, T Separations mousse, Objet 1.
- Notices PDF integrees avec apercus.
- Bouton **Generer fiche PDF interne** sur une seule page.
- Configuration Render : `render.yaml`, `Procfile`, `runtime.txt`.
- Preparation Supabase : `.env.example` et `supabase_schema.sql`.

## Deploiement GitHub + Render

1. Creer un nouveau repo GitHub.
2. Envoyer tout le contenu de ce dossier a la racine du repo.
3. Sur Render : **New > Web Service**.
4. Connecter le repo GitHub.
5. Render detectera `render.yaml`.
6. Verifier :
   - Build command : `pip install -r requirements.txt`
   - Start command : `python app.py`

L'application utilise automatiquement la variable `PORT` fournie par Render.

## Variables d'environnement Render

A renseigner plus tard quand on branchera vraiment Supabase :

```text
SUPABASE_URL
SUPABASE_ANON_KEY
```

Pour le moment, les calculs fonctionnent sans Supabase. Supabase est prepare pour l'historique et la sauvegarde des fiches.

## Test local

```bash
pip install -r requirements.txt
python app.py
```

Puis ouvrir :

```text
http://127.0.0.1:5000
```

## Health check

```text
/health
```
