# LAB 1 - Durcissement du stockage distribué

Nom : ALLAGLO Kossiko

## Objectif

Dans ce lab, nous partons d'un cluster Big Data déjà fonctionnel et nous renforçons la sécurité de la partie stockage distribuée autour de MinIO.

L'idée n'est pas de redéployer toute la plateforme, mais de modifier progressivement l'existant pour observer :

- ce qui circule en clair avant le durcissement ;
- ce qui change après l'activation de TLS ;
- comment MinIO peut s'intégrer avec une identité externe via OIDC ;
- ce que nous pouvons prouver avec les captures et les commandes.

## 1. Sauvegarde de l'existant

A compléter après la sauvegarde du `docker-compose.yml` et du volume MinIO.

## 2. Interception avant durcissement

A compléter après la capture réseau avant TLS.

## 3. Activation de TLS sur MinIO

A compléter après la génération des certificats et le redémarrage de MinIO en HTTPS.

## 4. Intégration OIDC avec Keycloak

A compléter après la création du realm, du client et du test STS.

## 5. Interception après durcissement

A compléter après la capture réseau en HTTPS et la vérification que les données sensibles ne sont plus lisibles.

## Conclusion

A compléter en fin de lab.
