# Définitions des KPI

Ce document décrit les indicateurs utilisés dans le dashboard Power BI.

Sauf mention contraire, les mesures sont calculées uniquement sur les commandes dont le statut est :

```text
delivered
```

---

## 1. Chiffre d’affaires

### Définition

Somme de la valeur totale des articles associés aux commandes livrées.

### Mesure DAX

```DAX
Chiffre affaires =
CALCULATE(
    SUM('public fact_sales'[total_item_value]),
    'public fact_sales'[order_status] = "delivered"
)
```

### Validation SQL

```sql
SELECT
    ROUND(SUM(total_item_value)::numeric, 2) AS chiffre_affaires
FROM public.fact_sales
WHERE order_status = 'delivered';
```

---

## 2. Nombre de commandes

### Définition

Nombre distinct de commandes livrées.

### Mesure DAX

```DAX
Nombre commandes =
CALCULATE(
    DISTINCTCOUNT('public fact_sales'[order_id]),
    'public fact_sales'[order_status] = "delivered"
)
```

### Validation SQL

```sql
SELECT
    COUNT(DISTINCT order_id) AS nombre_commandes
FROM public.fact_sales
WHERE order_status = 'delivered';
```

---

## 3. Panier moyen

### Définition

Chiffre d’affaires moyen par commande livrée.

### Mesure DAX

```DAX
Panier moyen =
DIVIDE(
    [Chiffre affaires],
    [Nombre commandes],
    0
)
```

### Validation SQL

```sql
SELECT
    ROUND(
        SUM(total_item_value)::numeric
        / COUNT(DISTINCT order_id),
        2
    ) AS panier_moyen
FROM public.fact_sales
WHERE order_status = 'delivered';
```

Résultat attendu :

```text
159,83 €
```

---

## 4. Note moyenne

### Définition

Moyenne des notes client des commandes livrées.

### Mesure DAX

```DAX
Note moyenne =
CALCULATE(
    AVERAGE('public fact_sales'[review_score]),
    'public fact_sales'[order_status] = "delivered"
)
```

### Validation SQL

```sql
SELECT
    ROUND(AVG(review_score)::numeric, 2) AS note_moyenne
FROM public.fact_sales
WHERE order_status = 'delivered';
```

Résultat validé :

```text
4,08
```

---

## 5. Délai moyen de livraison

### Définition

Nombre moyen de jours entre la commande et la livraison effective.

### Mesure DAX

```DAX
Délai moyen livraison =
CALCULATE(
    AVERAGE('public fact_sales'[delivery_time_days]),
    'public fact_sales'[order_status] = "delivered"
)
```

Format d’affichage conseillé :

```text
0,0 jours
```

La mesure doit rester numérique pour être réutilisable dans les graphiques.

---

## 6. Nombre de commandes en retard

### Définition

Nombre distinct de commandes livrées après la date prévue.

### Mesure DAX

```DAX
Nombre commandes en retard =
CALCULATE(
    DISTINCTCOUNT('public fact_sales'[order_id]),
    'public fact_sales'[order_status] = "delivered",
    'public fact_sales'[is_late_delivery] = TRUE()
)
```

---

## 7. Taux de retard

### Définition

Part des commandes livrées arrivées après la date prévue.

### Mesure DAX

```DAX
Taux retard =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT('public fact_sales'[order_id]),
        'public fact_sales'[order_status] = "delivered",
        'public fact_sales'[is_late_delivery] = TRUE()
    ),
    [Nombre commandes],
    0
)
```

### Validation SQL

```sql
SELECT
    ROUND(
        100.0
        * COUNT(
            DISTINCT CASE
                WHEN is_late_delivery = TRUE THEN order_id
            END
        )
        / COUNT(DISTINCT order_id),
        2
    ) AS taux_retard
FROM public.fact_sales
WHERE order_status = 'delivered';
```

---

## 8. Retard moyen

### Définition

Nombre moyen de jours de retard pour les commandes livrées en retard.

### Mesure DAX

```DAX
Retard moyen jours =
CALCULATE(
    AVERAGE('public fact_sales'[delivery_lateness_days]),
    'public fact_sales'[order_status] = "delivered",
    'public fact_sales'[is_late_delivery] = TRUE()
)
```

---

## 9. Nombre d’articles vendus

### Définition

Nombre de lignes de vente associées aux commandes livrées.

### Mesure DAX

```DAX
Nombre articles vendus =
CALCULATE(
    COUNTROWS('public fact_sales'),
    'public fact_sales'[order_status] = "delivered"
)
```

---

## 10. Nombre de clients

### Définition

Nombre distinct de clients ayant au moins une commande livrée.

### Mesure DAX

```DAX
Nombre clients =
CALCULATE(
    DISTINCTCOUNT('public fact_sales'[customer_key]),
    'public fact_sales'[order_status] = "delivered"
)
```

Le comptage est réalisé dans la table de faits afin que les filtres de date fonctionnent correctement.

---

## 11. Chiffre d’affaires par client

### Définition

Montant moyen de chiffre d’affaires généré par client actif.

### Mesure DAX

```DAX
Chiffre affaires par client =
DIVIDE(
    [Chiffre affaires],
    [Nombre clients],
    0
)
```

---

## 12. Commandes moyennes par client

### Définition

Nombre moyen de commandes livrées par client actif.

### Mesure DAX

```DAX
Commandes moyennes par client =
DIVIDE(
    [Nombre commandes],
    [Nombre clients],
    0
)
```

---

## 13. Clients récurrents

### Définition

Nombre de clients ayant passé plus d’une commande livrée.

### Mesure DAX

```DAX
Clients recurrents =
COUNTROWS(
    FILTER(
        VALUES('public dim_customer'[customer_unique_id]),
        CALCULATE(
            DISTINCTCOUNT('public fact_sales'[order_id]),
            'public fact_sales'[order_status] = "delivered"
        ) > 1
    )
)
```

---

## 14. Taux de clients récurrents

### Définition

Part des clients actifs ayant passé plus d’une commande livrée.

### Mesure DAX

```DAX
Taux clients recurrents =
DIVIDE(
    [Clients recurrents],
    [Nombre clients],
    0
)
```

---

## 15. Statut de livraison

### Définition

Classification d’une commande selon le respect du délai prévu.

### Colonne DAX

```DAX
Statut livraison =
IF(
    'public fact_sales'[is_late_delivery] = TRUE(),
    "En retard",
    "À temps"
)
```

---

## 16. Moyen de paiement

### Définition

Libellé traduit du moyen de paiement principal.

### Colonne DAX

```DAX
Moyen de paiement =
SWITCH(
    'public fact_sales'[main_payment_type],
    "credit_card", "Carte de crédit",
    "boleto", "Boleto",
    "voucher", "Voucher",
    "debit_card", "Carte de débit",
    "not_defined", "Non défini",
    BLANK(), "Non renseigné",
    'public fact_sales'[main_payment_type]
)
```

---

## Tableau de validation

| KPI | PostgreSQL | Power BI | Statut |
|---|---:|---:|---|
| Chiffre d’affaires | 15 419 773,75 € | 15,42 M€ | OK |
| Nombre de commandes | environ 96 K | environ 96 K | OK |
| Panier moyen | 159,83 € | 159,83 € | OK |
| Note moyenne | 4,08 | 4,08 | OK |
| Délai moyen | environ 12 jours | environ 12 jours | OK |
| Taux de retard | environ 6,77 % | environ 6,77 % | OK |
| Nombre de clients | environ 93 K | environ 93 K | OK |
| Taux clients récurrents | environ 3 % | environ 3 % | OK |
