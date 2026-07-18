# Checklist avant publication GitHub

## Sécurité

- [ ] Aucun fichier `.env`
- [ ] Aucun mot de passe PostgreSQL
- [ ] Aucun secret, token ou clé
- [ ] Aucune donnée personnelle
- [ ] Aucun fichier privé

## Code

- [ ] Le pipeline Python s’exécute
- [ ] Les imports fonctionnent
- [ ] Les tests passent
- [ ] Les chemins sont relatifs
- [ ] Le code est lisible et commenté

## Base de données

- [ ] `docker-compose.yml` fonctionne
- [ ] Les scripts SQL sont présents
- [ ] Le schéma en étoile est documenté
- [ ] Les identifiants utilisés ne sont pas sensibles

## Power BI

- [ ] Le fichier `.pbix` est enregistré
- [ ] Le fichier `.pbit` est disponible
- [ ] Les 5 pages sont finalisées
- [ ] Les filtres fonctionnent
- [ ] Les KPI ont été validés
- [ ] Aucun nom technique inutile n’est visible

## Documentation

- [ ] Le README est à jour
- [ ] `docs/kpi_definitions.md` est présent
- [ ] Les captures sont dans `docs/images/`
- [ ] Les noms des images correspondent au README
- [ ] Les commandes d’installation sont testées

## Git

- [ ] `.gitignore` est présent
- [ ] Aucun fichier volumineux inutile
- [ ] Le dépôt est propre
- [ ] Le dépôt est rendu public seulement après vérification
