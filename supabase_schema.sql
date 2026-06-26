-- Schema de base pour la future sauvegarde des fiches de chiffrage.
-- A executer dans Supabase SQL Editor quand on activera l'historique.

create table if not exists public.chiffrages (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  type_caisse text not null,
  client text,
  responsable text,
  donnees_saisie jsonb not null default '{}'::jsonb,
  resultat jsonb not null default '{}'::jsonb,
  notice_pdf text,
  fiche_pdf_url text,
  statut text not null default 'brouillon'
);

alter table public.chiffrages enable row level security;

-- Politique volontairement non ouverte par defaut.
-- A adapter quand l'authentification sera branchee.
