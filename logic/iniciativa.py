import pandas as pd
import random

def rolar_d20():
    return random.randint(1, 20)

def calcular_iniciativa(df_personagens, df_inimigos, inimigos_extra):
    resultados = []
    
    for _, row in df_personagens.iterrows():
        d20 = rolar_d20()
        resultados.append({
            "Nome": row["Nome"],
            "Tipo": "Jogador",
            "Total": d20 + row["Iniciativa"],
            "DEX": row.get("DEX", 0),
            "IniBase": row["Iniciativa"],
            "HP": row.get("HP", 0),
            "CA": row.get("CA", 0)
        })

    for _, row in df_inimigos.iterrows():
        d20 = rolar_d20()
        resultados.append({
            "Nome": row["Nome"],
            "Tipo": "Inimigo",
            "Total": d20 + row["Iniciativa"],
            "DEX": row.get("DEX", 0),
            "IniBase": row["Iniciativa"],
            "HP": row.get("HP", 0),
            "CA": row.get("CA", 0)
        })

    for inimigo in inimigos_extra:
        d20 = rolar_d20()
        resultados.append({
            "Nome": inimigo["Nome"],
            "Tipo": "Inimigo",
            "Total": d20 + inimigo["Iniciativa"],
            "DEX": inimigo["DEX"],
            "IniBase": inimigo["Iniciativa"],
            "HP": inimigo["HP"],
            "CA": inimigo["CA"]
        })

    df_final = pd.DataFrame(resultados)\
        .sort_values(by=["Total", "DEX", "IniBase"], ascending=[False, False, False])\
        .reset_index(drop=True)
        
    return df_final