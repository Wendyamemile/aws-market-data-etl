# AWS Market Data ETL

## Description
Ce projet implémente un pipeline ETL (Extract, Transform, Load) automatisé pour extraire des données de marché, les transformer et les charger dans l'infrastructure AWS. 

## Architecture et Technologies
* **Langage :** Python 3.x
* **Cloud Provider :** AWS (S3, Lambda, Redshift, etc. - *à préciser*)
* **Bibliothèques principales :** Pandas, Boto3 (*à adapter selon vos outils*)

## Prérequis
Avant de commencer, assurez-vous d'avoir installé et configuré :
* Python 3.x et un environnement virtuel (comme Conda).
* [AWS CLI](https://aws.amazon.com/cli/) configuré avec vos identifiants (`aws configure`).
* Git.

## Installation
1. Clonez le dépôt sur votre machine locale :
   ```bash
   git clone git@github.com:Wendyamemile/aws-market-data-etl.git
   cd aws-market-data-etl