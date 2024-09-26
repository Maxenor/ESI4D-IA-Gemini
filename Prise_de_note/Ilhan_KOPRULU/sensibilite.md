Le **taux de sensibilité**, ou **rappel**, est une mesure qui se concentre sur la capacité d’un modèle à identifier correctement les **vrais positifs** (VP). En d’autres termes, c'est le pourcentage des cas positifs que le modèle a réussi à prédire correctement.

### Définitions des concepts :
- **Vrais positifs (VP)** : Ce sont les instances où le modèle a correctement prédit la classe positive, c’est-à-dire les cas où la réalité et la prédiction sont toutes deux positives.
- **Faux négatifs (FN)** : Ce sont les cas où le modèle a prédit un négatif à tort, alors que la classe réelle était positive. Autrement dit, le modèle a raté un cas positif.

Taux de sensibilité = VP / (VP + FN)

### Autres catégories importantes :
- **Faux positifs (FP)** : Ce sont les cas où le modèle a prédit un positif à tort, alors que la classe réelle était négative. Cela signifie que le modèle "surprédit" la classe positive.
- **Vrais négatifs (VN)** : Ce sont les instances où le modèle a correctement prédit la classe négative, c’est-à-dire lorsque la réalité et la prédiction sont toutes deux négatives.

### Interactions avec les autres métriques :
Un modèle avec une **sensibilité élevée** identifiera la majorité des **vrais positifs**, ce qui signifie qu'il réduira les **faux négatifs**. Cependant, cela peut parfois se faire au détriment d'une augmentation des **faux positifs**, car le modèle peut devenir trop "sensible" et prédire la classe positive même quand ce n’est pas le cas.

En résumé, la sensibilité mesure la capacité d'un modèle à minimiser les **faux négatifs**, en mettant l'accent sur la détection des **vrais positifs**.