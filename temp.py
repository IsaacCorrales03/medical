from database import DataBaseManager

# Inicializar el gestor de base de datos
db = DataBaseManager()
db.create_tables()  # Asegurarse de que las tablas existan

# Lista de 40 medicamentos adicionales con sus datos
medicamentos_adicionales = [
    {
        "nombre": "Amoxicilina",
        "uso": "Antibiótico para infecciones bacterianas.",
        "dosis": "500 mg cada 8 horas por 7-10 días.",
        "efectos_secundarios": "Diarrea, náuseas, erupciones cutáneas.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Ibuprofeno",
        "uso": "Antiinflamatorio, analgésico y antipirético.",
        "dosis": "400-600 mg cada 6-8 horas.",
        "efectos_secundarios": "Dolor estomacal, acidez, riesgo cardiovascular.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Paracetamol",
        "uso": "Analgésico y antipirético.",
        "dosis": "500-1000 mg cada 6-8 horas, máximo 4g/día.",
        "efectos_secundarios": "Toxicidad hepática en sobredosis.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Omeprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "efectos_secundarios": "Dolor de cabeza, diarrea, deficiencia de B12 a largo plazo.",
        "recomendaciones_alimenticias": "Tomar en ayunas, 30 minutos antes del desayuno."
    },
    {
        "nombre": "Loratadina",
        "uso": "Antihistamínico para alergias.",
        "dosis": "10 mg una vez al día.",
        "efectos_secundarios": "Somnolencia leve, boca seca.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Metformina",
        "uso": "Control de glucosa en diabetes tipo 2.",
        "dosis": "500-1000 mg dos veces al día.",
        "efectos_secundarios": "Molestias gastrointestinales, acidosis láctica (rara).",
        "recomendaciones_alimenticias": "Tomar con las comidas para reducir efectos gastrointestinales."
    },
    {
        "nombre": "Losartán",
        "uso": "Antihipertensivo, bloqueador del receptor de angiotensina.",
        "dosis": "50-100 mg una vez al día.",
        "efectos_secundarios": "Mareos, hipotensión, hipercalemia.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Simvastatina",
        "uso": "Reductor de colesterol.",
        "dosis": "20-40 mg una vez al día por la noche.",
        "efectos_secundarios": "Dolores musculares, elevación de enzimas hepáticas.",
        "recomendaciones_alimenticias": "Evitar consumo de jugo de toronja."
    },
    {
        "nombre": "Alprazolam",
        "uso": "Ansiolítico para trastornos de ansiedad.",
        "dosis": "0.25-0.5 mg tres veces al día.",
        "efectos_secundarios": "Somnolencia, dependencia, efecto rebote.",
        "recomendaciones_alimenticias": "Evitar alcohol y jugo de toronja."
    },
    {
        "nombre": "Levotiroxina",
        "uso": "Reemplazo hormonal para hipotiroidismo.",
        "dosis": "25-200 mcg diarios según necesidad.",
        "efectos_secundarios": "Taquicardia, nerviosismo si sobredosis.",
        "recomendaciones_alimenticias": "Tomar en ayunas, esperar 30-60 minutos antes de desayunar."
    },
    {
        "nombre": "Diclofenaco",
        "uso": "Antiinflamatorio, analgésico.",
        "dosis": "50 mg cada 8-12 horas.",
        "efectos_secundarios": "Úlceras, sangrado digestivo, riesgo cardiovascular.",
        "recomendaciones_alimenticias": "Tomar con alimentos para proteger el estómago."
    },
    {
        "nombre": "Ciprofloxacino",
        "uso": "Antibiótico de amplio espectro.",
        "dosis": "500 mg cada 12 horas.",
        "efectos_secundarios": "Tendinitis, ruptura de tendón, neuropatía.",
        "recomendaciones_alimenticias": "Evitar lácteos, antiácidos y suplementos minerales durante la toma."
    },
    {
        "nombre": "Fluoxetina",
        "uso": "Antidepresivo ISRS para depresión y ansiedad.",
        "dosis": "20 mg una vez al día por la mañana.",
        "efectos_secundarios": "Náuseas, insomnio, disfunción sexual.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Enalapril",
        "uso": "Antihipertensivo, inhibidor de la ECA.",
        "dosis": "5-40 mg al día en una o dos tomas.",
        "efectos_secundarios": "Tos seca, angioedema, hipercalemia.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Ranitidina",
        "uso": "Antiácido, antagonista H2 para úlceras y reflujo.",
        "dosis": "150 mg dos veces al día o 300 mg al acostarse.",
        "efectos_secundarios": "Dolor de cabeza, estreñimiento.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Clonazepam",
        "uso": "Anticonvulsivante, ansiolítico.",
        "dosis": "0.5-2 mg dos o tres veces al día.",
        "efectos_secundarios": "Somnolencia, dependencia, problemas de memoria.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Warfarina",
        "uso": "Anticoagulante oral.",
        "dosis": "Variable según INR objetivo, usualmente 2-10 mg diarios.",
        "efectos_secundarios": "Sangrado, hematomas, necrosis cutánea.",
        "recomendaciones_alimenticias": "Mantener constante ingesta de alimentos con vitamina K."
    },
    {
        "nombre": "Metoclopramida",
        "uso": "Antiemético, procinético gástrico.",
        "dosis": "10 mg tres veces al día antes de las comidas.",
        "efectos_secundarios": "Efectos extrapiramidales, somnolencia.",
        "recomendaciones_alimenticias": "Tomar 30 minutos antes de las comidas."
    },
    {
        "nombre": "Furosemida",
        "uso": "Diurético de asa para edema e hipertensión.",
        "dosis": "20-80 mg una o dos veces al día.",
        "efectos_secundarios": "Desequilibrio electrolítico, deshidratación.",
        "recomendaciones_alimenticias": "Tomar por la mañana para evitar nicturia."
    },
    {
        "nombre": "Amlodipino",
        "uso": "Bloqueador de canales de calcio para hipertensión.",
        "dosis": "5-10 mg una vez al día.",
        "efectos_secundarios": "Edema en extremidades, enrojecimiento facial.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Metronidazol",
        "uso": "Antibiótico y antiparasitario.",
        "dosis": "500 mg cada 8 horas por 7-10 días.",
        "efectos_secundarios": "Sabor metálico, náuseas, efecto antabus con alcohol.",
        "recomendaciones_alimenticias": "Evitar alcohol durante el tratamiento y 48h después."
    },
    {
        "nombre": "Hidroclorotiazida",
        "uso": "Diurético tiazídico para hipertensión.",
        "dosis": "12.5-25 mg una vez al día.",
        "efectos_secundarios": "Hipopotasemia, hiperuricemia, fotosensibilidad.",
        "recomendaciones_alimenticias": "Considerar alimentos ricos en potasio."
    },
    {
        "nombre": "Prednisona",
        "uso": "Corticosteroide antiinflamatorio e inmunosupresor.",
        "dosis": "Variable, típicamente 5-60 mg/día con reducción gradual.",
        "efectos_secundarios": "Aumento de peso, osteoporosis, hiperglucemia.",
        "recomendaciones_alimenticias": "Tomar con alimentos, dieta baja en sodio y rica en potasio."
    },
    {
        "nombre": "Ácido Acetilsalicílico",
        "uso": "Antiinflamatorio, analgésico, antiagregante plaquetario.",
        "dosis": "100 mg diarios como antiagregante; 500-1000 mg cada 4-6h como analgésico.",
        "efectos_secundarios": "Sangrado gastrointestinal, tinnitus en dosis altas.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Gabapentina",
        "uso": "Antiepiléptico, dolor neuropático.",
        "dosis": "300-1200 mg tres veces al día.",
        "efectos_secundarios": "Somnolencia, mareos, aumento de peso.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Bisoprolol",
        "uso": "Betabloqueante para hipertensión e insuficiencia cardíaca.",
        "dosis": "2.5-10 mg una vez al día.",
        "efectos_secundarios": "Fatiga, bradicardia, broncoespasmo.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Claritromicina",
        "uso": "Antibiótico macrólido.",
        "dosis": "500 mg cada 12 horas por 7-14 días.",
        "efectos_secundarios": "Alteración del gusto, malestar gastrointestinal.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Venlafaxina",
        "uso": "Antidepresivo IRSN para depresión y ansiedad.",
        "dosis": "75-225 mg una vez al día (liberación prolongada).",
        "efectos_secundarios": "Náuseas, hipertensión, sudoración.",
        "recomendaciones_alimenticias": "Tomar con alimentos."
    },
    {
        "nombre": "Insulina",
        "uso": "Hormona para control de glucemia en diabetes.",
        "dosis": "Variable según tipo y necesidades del paciente.",
        "efectos_secundarios": "Hipoglucemia, aumento de peso, lipodistrofia.",
        "recomendaciones_alimenticias": "Coordinar con ingesta de carbohidratos."
    },
    {
        "nombre": "Tamsulosina",
        "uso": "Bloqueador alfa para hiperplasia prostática benigna.",
        "dosis": "0.4 mg una vez al día.",
        "efectos_secundarios": "Mareos, eyaculación retrógrada.",
        "recomendaciones_alimenticias": "Tomar después del desayuno."
    },
    {
        "nombre": "Sildenafilo",
        "uso": "Inhibidor de PDE5 para disfunción eréctil.",
        "dosis": "50 mg 1 hora antes de la actividad sexual.",
        "efectos_secundarios": "Dolor de cabeza, enrojecimiento facial, congestión nasal.",
        "recomendaciones_alimenticias": "Evitar comidas grasas que reducen absorción."
    },
    {
        "nombre": "Pantoprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "efectos_secundarios": "Similar a omeprazol pero menos interacciones.",
        "recomendaciones_alimenticias": "Tomar en ayunas."
    },
    {
        "nombre": "Pregabalina",
        "uso": "Antiepiléptico, dolor neuropático, ansiedad.",
        "dosis": "75-300 mg dos veces al día.",
        "efectos_secundarios": "Mareos, somnolencia, aumento de peso.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Risperidona",
        "uso": "Antipsicótico para esquizofrenia y trastorno bipolar.",
        "dosis": "2-6 mg al día en una o dos tomas.",
        "efectos_secundarios": "Aumento de peso, hiperprolactinemia, síndrome metabólico.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Montelukast",
        "uso": "Antileucotrieno para asma y rinitis alérgica.",
        "dosis": "10 mg una vez al día por la noche.",
        "efectos_secundarios": "Dolor de cabeza, cambios de humor.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Escitalopram",
        "uso": "Antidepresivo ISRS para depresión y ansiedad.",
        "dosis": "10-20 mg una vez al día.",
        "efectos_secundarios": "Náuseas, insomnio, disfunción sexual.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Esomeprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "efectos_secundarios": "Dolor de cabeza, diarrea.",
        "recomendaciones_alimenticias": "Tomar en ayunas."
    },
    {
        "nombre": "Azatioprina",
        "uso": "Inmunosupresor para enfermedades autoinmunes y trasplantes.",
        "dosis": "1-3 mg/kg/día.",
        "efectos_secundarios": "Mielosupresión, hepatotoxicidad, aumento riesgo de infecciones.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir náuseas."
    },
    {
        "nombre": "Espironolactona",
        "uso": "Diurético ahorrador de potasio, antagonista de aldosterona.",
        "dosis": "25-100 mg al día.",
        "efectos_secundarios": "Hiperpotasemia, ginecomastia en hombres.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Amiodarona",
        "uso": "Antiarrítmico para arritmias ventriculares y auriculares.",
        "dosis": "200-400 mg al día tras dosis de carga.",
        "efectos_secundarios": "Toxicidad pulmonar, tiroidea y hepática.",
        "recomendaciones_alimenticias": "Tomar con alimentos."
    }
]

# Añadir cada medicamento adicional a la base de datos
for med in medicamentos_adicionales:
    db.add_medicamento(
        nombre=med["nombre"],
        uso=med["uso"],
        dosis=med["dosis"],
        efectos_secundarios=med["efectos_secundarios"],
        recomendaciones_alimenticias=med["recomendaciones_alimenticias"]
    )

print("Se han añadido 40 medicamentos adicionales correctamente.")

# Cerrar la conexión cuando hayamos terminado
db.close_connection()