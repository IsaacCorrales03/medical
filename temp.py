from database import DataBaseManager

# Inicializar el gestor de base de datos
db = DataBaseManager()
db.create_tables()  # Asegurarse de que las tablas existan

# Lista de 40 medicamentos adicionales con sus datos y categorías
medicamentos_adicionales = [
    {
        "nombre": "Hidroxicloroquina",
        "uso": "Antipalúdico y para enfermedades autoinmunes como lupus y artritis reumatoide.",
        "dosis": "200-400 mg al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Retinopatía, prolongación del QT, miopatía.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir molestias gástricas."
    },
    {
        "nombre": "Citalopram",
        "uso": "Antidepresivo ISRS para depresión y trastornos de ansiedad.",
        "dosis": "20-40 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, somnolencia, prolongación del QT.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Vancomicina",
        "uso": "Antibiótico glucopéptido para infecciones por grampositivos resistentes.",
        "dosis": "Variable según función renal y niveles séricos.",
        "categoria": "Inyectable",
        "efectos_secundarios": "Nefrotoxicidad, ototoxicidad, síndrome del hombre rojo.",
        "recomendaciones_alimenticias": "No aplica para forma inyectable."
    },
    {
        "nombre": "Levodopa + Carbidopa",
        "uso": "Precursor de dopamina para enfermedad de Parkinson.",
        "dosis": "100/25 mg tres veces al día, ajustar según respuesta.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Discinesias, náuseas, hipotensión ortostática.",
        "recomendaciones_alimenticias": "Tomar 30 minutos antes de las comidas, evitar proteínas en exceso."
    },
    {
        "nombre": "Fentanilo",
        "uso": "Analgésico opioide potente para dolor severo crónico.",
        "dosis": "Variable según presentación (parche transdérmico 12-100 mcg/h).",
        "categoria": "Parche",
        "efectos_secundarios": "Depresión respiratoria, dependencia, estreñimiento.",
        "recomendaciones_alimenticias": "No aplica para parche transdérmico."
    },
    {
        "nombre": "Donepezilo",
        "uso": "Inhibidor de acetilcolinesterasa para demencia de Alzheimer.",
        "dosis": "5-10 mg una vez al día por la noche.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, diarrea, insomnio, calambres musculares.",
        "recomendaciones_alimenticias": "Tomar por la noche para minimizar efectos adversos."
    },
    {
        "nombre": "Metotrexato",
        "uso": "Antimetabolito para artritis reumatoide, psoriasis y cáncer.",
        "dosis": "7.5-25 mg una vez por semana.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Mielosupresión, hepatotoxicidad, úlceras bucales.",
        "recomendaciones_alimenticias": "Suplementar con ácido fólico, evitar alcohol."
    },
    {
        "nombre": "Baclofen",
        "uso": "Relajante muscular para espasticidad.",
        "dosis": "5-25 mg tres veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, debilidad muscular, mareos.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir molestias gástricas."
    },
    {
        "nombre": "Trazodona",
        "uso": "Antidepresivo atípico para depresión e insomnio.",
        "dosis": "50-300 mg al día, dosis única nocturna para insomnio.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, hipotensión ortostática, priapismo (raro).",
        "recomendaciones_alimenticias": "Tomar con alimentos para mejorar absorción."
    },
    {
        "nombre": "Quetiapina",
        "uso": "Antipsicótico atípico para esquizofrenia y trastorno bipolar.",
        "dosis": "25-800 mg al día según indicación.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sedación, aumento de peso, síndrome metabólico.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Isotretinoína",
        "uso": "Retinoide oral para acné severo resistente.",
        "dosis": "0.5-2 mg/kg/día por 4-6 meses.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Teratogenicidad, sequedad cutánea, hepatotoxicidad.",
        "recomendaciones_alimenticias": "Tomar con alimentos grasos para mejorar absorción."
    },
    {
        "nombre": "Rivaroxabán",
        "uso": "Anticoagulante oral directo para fibrilación auricular y trombosis.",
        "dosis": "10-20 mg una vez al día según indicación.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sangrado, hematomas.",
        "recomendaciones_alimenticias": "Dosis de 15-20 mg tomar con alimentos."
    },
    {
        "nombre": "Lamotrigina",
        "uso": "Anticonvulsivante para epilepsia y estabilizador del ánimo.",
        "dosis": "25-400 mg al día con titulación lenta.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Síndrome de Stevens-Johnson, diplopía, ataxia.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Clozapina",
        "uso": "Antipsicótico atípico para esquizofrenia resistente al tratamiento.",
        "dosis": "25-900 mg al día con titulación gradual.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Agranulocitosis, miocarditis, convulsiones.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Duloxetina",
        "uso": "Antidepresivo IRSN para depresión, ansiedad y dolor neuropático.",
        "dosis": "30-120 mg una vez al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Náuseas, boca seca, estreñimiento, hepatotoxicidad.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Topiramato",
        "uso": "Anticonvulsivante para epilepsia y profilaxis de migraña.",
        "dosis": "25-400 mg al día en dosis divididas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Pérdida de peso, parestesias, cálculos renales.",
        "recomendaciones_alimenticias": "Aumentar ingesta de líquidos para prevenir cálculos."
    },
    {
        "nombre": "Finasterida",
        "uso": "Inhibidor de 5-alfa reductasa para hiperplasia prostática y alopecia.",
        "dosis": "1-5 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Disfunción sexual, ginecomastia, depresión.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Apixabán",
        "uso": "Anticoagulante oral directo para fibrilación auricular.",
        "dosis": "2.5-5 mg dos veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sangrado, hematomas.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Valsartán",
        "uso": "Bloqueador del receptor de angiotensina para hipertensión.",
        "dosis": "80-320 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Mareos, hipotensión, hiperpotasemia.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Olanzapina",
        "uso": "Antipsicótico atípico para esquizofrenia y trastorno bipolar.",
        "dosis": "5-20 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Aumento significativo de peso, diabetes, dislipidemia.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Atorvastatina",
        "uso": "Reductor de colesterol y triglicéridos.",
        "dosis": "10-80 mg una vez al día por la noche.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolores musculares, elevación de enzimas hepáticas, rabdomiólisis.",
        "recomendaciones_alimenticias": "Evitar consumo excesivo de jugo de toronja."
    },
    {
        "nombre": "Carbamazepina",
        "uso": "Anticonvulsivante para epilepsia y neuralgia del trigémino.",
        "dosis": "200-400 mg dos veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, ataxia, diplopía, supresión medular.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir molestias gástricas."
    },
    {
        "nombre": "Dexametasona",
        "uso": "Corticosteroide potente antiinflamatorio e inmunosupresor.",
        "dosis": "0.5-9 mg al día según condición.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hiperglucemia, osteoporosis, supresión suprarrenal.",
        "recomendaciones_alimenticias": "Tomar con alimentos, dieta baja en sodio."
    },
    {
        "nombre": "Ketoconazol",
        "uso": "Antifúngico para infecciones por hongos.",
        "dosis": "200-400 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hepatotoxicidad, náuseas, alteraciones hormonales.",
        "recomendaciones_alimenticias": "Tomar con alimentos ácidos para mejor absorción."
    },
    {
        "nombre": "Tramadol",
        "uso": "Analgésico opioide para dolor moderado a severo.",
        "dosis": "50-100 mg cada 4-6 horas, máximo 400 mg/día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, mareos, estreñimiento, dependencia.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Propranolol",
        "uso": "Betabloqueante para hipertensión, arritmias y ansiedad.",
        "dosis": "40-320 mg al día en dosis divididas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Bradicardia, fatiga, broncoespasmo, depresión.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Cetirizina",
        "uso": "Antihistamínico para alergias y urticaria.",
        "dosis": "10 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, boca seca, fatiga.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Morfina",
        "uso": "Analgésico opioide potente para dolor severo.",
        "dosis": "Variable según necesidad y tolerancia del paciente.",
        "categoria": "Inyectable",
        "efectos_secundarios": "Depresión respiratoria, estreñimiento, dependencia.",
        "recomendaciones_alimenticias": "No aplica para forma inyectable."
    },
    {
        "nombre": "Digoxina",
        "uso": "Glucósido cardíaco para insuficiencia cardíaca y fibrilación auricular.",
        "dosis": "0.125-0.25 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Toxicidad cardíaca, náuseas, alteraciones visuales.",
        "recomendaciones_alimenticias": "Mantener niveles estables de potasio en dieta."
    },
    {
        "nombre": "Salbutamol",
        "uso": "Broncodilatador para asma y EPOC.",
        "dosis": "2-4 puffs cada 4-6 horas según necesidad.",
        "categoria": "Inhalador",
        "efectos_secundarios": "Temblor, taquicardia, nerviosismo.",
        "recomendaciones_alimenticias": "Enjuagar boca después del uso."
    },
    {
        "nombre": "Clindamicina",
        "uso": "Antibiótico para infecciones por anaerobios.",
        "dosis": "150-450 mg cada 6 horas.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Colitis pseudomembranosa, diarrea, erupciones.",
        "recomendaciones_alimenticias": "Tomar con abundante agua."
    },
    {
        "nombre": "Nitroglicerina",
        "uso": "Vasodilatador para angina de pecho.",
        "dosis": "0.3-0.6 mg sublingual según necesidad.",
        "categoria": "Sublingual",
        "efectos_secundarios": "Cefalea, hipotensión, mareos.",
        "recomendaciones_alimenticias": "No masticar ni tragar la tableta."
    },
    {
        "nombre": "Fenitoína",
        "uso": "Anticonvulsivante para epilepsia.",
        "dosis": "300-400 mg al día en una o dos tomas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hiperplasia gingival, ataxia, hirsutismo.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Ondansetrón",
        "uso": "Antiemético para náuseas y vómitos.",
        "dosis": "4-8 mg cada 8 horas según necesidad.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Cefalea, estreñimiento, mareos.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Naproxeno",
        "uso": "Antiinflamatorio no esteroideo, analgésico.",
        "dosis": "250-500 mg cada 12 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Úlceras gástricas, sangrado, retención de líquidos.",
        "recomendaciones_alimenticias": "Tomar con alimentos para proteger el estómago."
    },
    {
        "nombre": "Captopril",
        "uso": "Inhibidor de la ECA para hipertensión e insuficiencia cardíaca.",
        "dosis": "25-150 mg al día en 2-3 tomas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Tos seca, hipercalemia, angioedema.",
        "recomendaciones_alimenticias": "Tomar 1 hora antes de las comidas."
    },
    {
        "nombre": "Haloperidol",
        "uso": "Antipsicótico típico para esquizofrenia y agitación.",
        "dosis": "0.5-20 mg al día según condición.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Síntomas extrapiramidales, discinesia tardía.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Aciclovir",
        "uso": "Antiviral para herpes simple y varicela zóster.",
        "dosis": "200-800 mg 5 veces al día por 5-10 días.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, diarrea, cefalea.",
        "recomendaciones_alimenticias": "Tomar con abundante agua."
    },
    {
        "nombre": "Diazepam",
        "uso": "Ansiolítico, relajante muscular, anticonvulsivante.",
        "dosis": "2-10 mg 2-4 veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, dependencia, ataxia.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Penicilina",
        "uso": "Antibiótico betalactámico para infecciones bacterianas.",
        "dosis": "250-500 mg cada 6 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Reacciones alérgicas, diarrea, náuseas.",
        "recomendaciones_alimenticias": "Tomar con el estómago vacío para mejor absorción."
    },
    {
        "nombre": "Codeína",
        "uso": "Analgésico opioide y antitusivo.",
        "dosis": "15-60 mg cada 4-6 horas según necesidad.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Estreñimiento, somnolencia, dependencia.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Lisinopril",
        "uso": "Inhibidor de la ECA para hipertensión.",
        "dosis": "10-40 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Tos seca, hipercalemia, mareos.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio."
    },
    {
        "nombre": "Nifedipino",
        "uso": "Bloqueador de canales de calcio para hipertensión y angina.",
        "dosis": "30-90 mg una vez al día (liberación prolongada).",
        "categoria": "Pastilla",
        "efectos_secundarios": "Edema, cefalea, enrojecimiento facial.",
        "recomendaciones_alimenticias": "Evitar jugo de toronja."
    },
    {
        "nombre": "Doxiciclina",
        "uso": "Antibiótico tetraciclina para diversas infecciones.",
        "dosis": "100 mg cada 12 horas.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Fotosensibilidad, náuseas, esofagitis.",
        "recomendaciones_alimenticias": "Evitar lácteos, tomar con abundante agua."
    },
    {
        "nombre": "Sucralfato",
        "uso": "Protector de mucosa gástrica para úlceras.",
        "dosis": "1 gramo 4 veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Estreñimiento, náuseas.",
        "recomendaciones_alimenticias": "Tomar 1 hora antes de las comidas y al acostarse."
    },
    {
        "nombre": "Carvedilol",
        "uso": "Betabloqueante no selectivo para hipertensión e insuficiencia cardíaca.",
        "dosis": "3.125-25 mg dos veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Mareos, fatiga, bradicardia.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir absorción rápida."
    },
    {
        "nombre": "Glibenclamida",
        "uso": "Hipoglucemiante oral para diabetes tipo 2.",
        "dosis": "2.5-20 mg al día con el desayuno.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hipoglucemia, aumento de peso.",
        "recomendaciones_alimenticias": "Tomar con el desayuno, mantener horarios regulares de comida."
    },
    {
        "nombre": "Eritromicina",
        "uso": "Antibiótico macrólido para infecciones respiratorias.",
        "dosis": "250-500 mg cada 6 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, diarrea, prolongación del QT.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir molestias gástricas."
    },
    {
        "nombre": "Lidocaína",
        "uso": "Anestésico local para procedimientos menores.",
        "dosis": "Variable según procedimiento.",
        "categoria": "Inyectable",
        "efectos_secundarios": "Reacciones alérgicas, toxicidad del SNC.",
        "recomendaciones_alimenticias": "No aplica para uso tópico/inyectable."
    },
    {
        "nombre": "Betametasona",
        "uso": "Corticosteroide potente para inflamación y alergias.",
        "dosis": "0.6-7.2 mg al día según condición.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Supresión suprarrenal, osteoporosis, hiperglucemia.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Sertralina",
        "uso": "Antidepresivo ISRS para depresión y trastornos de ansiedad.",
        "dosis": "50-200 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, diarrea, disfunción sexual, insomnio.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Budesonida",
        "uso": "Corticosteroide inhalado para asma y EPOC.",
        "dosis": "1-2 inhalaciones dos veces al día.",
        "categoria": "Inhalador",
        "efectos_secundarios": "Candidiasis oral, disfonía.",
        "recomendaciones_alimenticias": "Enjuagar boca después del uso."
    },
    {
        "nombre": "Terazosina",
        "uso": "Bloqueador alfa para hipertensión e hiperplasia prostática.",
        "dosis": "1-20 mg una vez al día al acostarse.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hipotensión ortostática, mareos, astenia.",
        "recomendaciones_alimenticias": "Tomar al acostarse para minimizar hipotensión."
    },
    {
        "nombre": "Quinidina",
        "uso": "Antiarrítmico para arritmias auriculares y ventriculares.",
        "dosis": "200-300 mg cada 6-8 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Cinconismo, arritmias, trombocitopenia.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir molestias gástricas."
    },
    {
        "nombre": "Mebendazol",
        "uso": "Antiparasitario para helmintiasis intestinales.",
        "dosis": "100 mg dos veces al día por 3 días.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Molestias abdominales, diarrea (raras).",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Ciclosporina",
        "uso": "Inmunosupresor para trasplantes y enfermedades autoinmunes.",
        "dosis": "Variable según condición y niveles séricos.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Nefrotoxicidad, hipertensión, hiperplasia gingival.",
        "recomendaciones_alimenticias": "Tomar consistentemente con o sin alimentos."
    },
    {
        "nombre": "Colchicina",
        "uso": "Antiinflamatorio específico para gota aguda.",
        "dosis": "0.6 mg cada 1-2 horas hasta alivio del dolor.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Diarrea, náuseas, mielosupresión en sobredosis.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Clorpromazina",
        "uso": "Antipsicótico típico para esquizofrenia y psicosis aguda.",
        "dosis": "25-800 mg al día según condición.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Síntomas extrapiramidales, sedación, hipotensión.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Pilocarpina",
        "uso": "Agonista colinérgico para glaucoma y xerostomía.",
        "dosis": "5 mg tres veces al día (para xerostomía).",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sudoración, náuseas, visión borrosa.",
        "recomendaciones_alimenticias": "Tomar con abundante agua."
    },
    {
        "nombre": "Indometacina",
        "uso": "AINE potente para artritis y cierre de conducto arterioso.",
        "dosis": "25-50 mg 2-3 veces al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Cefalea intensa, úlceras, efectos en SNC.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Amoxicilina",
        "uso": "Antibiótico para infecciones bacterianas.",
        "dosis": "500 mg cada 8 horas por 7-10 días.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Diarrea, náuseas, erupciones cutáneas.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Ibuprofeno",
        "uso": "Antiinflamatorio, analgésico y antipirético.",
        "dosis": "400-600 mg cada 6-8 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolor estomacal, acidez, riesgo cardiovascular.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Paracetamol",
        "uso": "Analgésico y antipirético.",
        "dosis": "500-1000 mg cada 6-8 horas, máximo 4g/día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Toxicidad hepática en sobredosis.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Omeprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Dolor de cabeza, diarrea, deficiencia de B12 a largo plazo.",
        "recomendaciones_alimenticias": "Tomar en ayunas, 30 minutos antes del desayuno."
    },
    {
        "nombre": "Loratadina",
        "uso": "Antihistamínico para alergias.",
        "dosis": "10 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia leve, boca seca.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Metformina",
        "uso": "Control de glucosa en diabetes tipo 2.",
        "dosis": "500-1000 mg dos veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Molestias gastrointestinales, acidosis láctica (rara).",
        "recomendaciones_alimenticias": "Tomar con las comidas para reducir efectos gastrointestinales."
    },
    {
        "nombre": "Losartán",
        "uso": "Antihipertensivo, bloqueador del receptor de angiotensina.",
        "dosis": "50-100 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Mareos, hipotensión, hipercalemia.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Simvastatina",
        "uso": "Reductor de colesterol.",
        "dosis": "20-40 mg una vez al día por la noche.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolores musculares, elevación de enzimas hepáticas.",
        "recomendaciones_alimenticias": "Evitar consumo de jugo de toronja."
    },
    {
        "nombre": "Alprazolam",
        "uso": "Ansiolítico para trastornos de ansiedad.",
        "dosis": "0.25-0.5 mg tres veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, dependencia, efecto rebote.",
        "recomendaciones_alimenticias": "Evitar alcohol y jugo de toronja."
    },
    {
        "nombre": "Levotiroxina",
        "uso": "Reemplazo hormonal para hipotiroidismo.",
        "dosis": "25-200 mcg diarios según necesidad.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Taquicardia, nerviosismo si sobredosis.",
        "recomendaciones_alimenticias": "Tomar en ayunas, esperar 30-60 minutos antes de desayunar."
    },
    {
        "nombre": "Diclofenaco",
        "uso": "Antiinflamatorio, analgésico.",
        "dosis": "50 mg cada 8-12 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Úlceras, sangrado digestivo, riesgo cardiovascular.",
        "recomendaciones_alimenticias": "Tomar con alimentos para proteger el estómago."
    },
    {
        "nombre": "Ciprofloxacino",
        "uso": "Antibiótico de amplio espectro.",
        "dosis": "500 mg cada 12 horas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Tendinitis, ruptura de tendón, neuropatía.",
        "recomendaciones_alimenticias": "Evitar lácteos, antiácidos y suplementos minerales durante la toma."
    },
    {
        "nombre": "Fluoxetina",
        "uso": "Antidepresivo ISRS para depresión y ansiedad.",
        "dosis": "20 mg una vez al día por la mañana.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Náuseas, insomnio, disfunción sexual.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Enalapril",
        "uso": "Antihipertensivo, inhibidor de la ECA.",
        "dosis": "5-40 mg al día en una o dos tomas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Tos seca, angioedema, hipercalemia.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Ranitidina",
        "uso": "Antiácido, antagonista H2 para úlceras y reflujo.",
        "dosis": "150 mg dos veces al día o 300 mg al acostarse.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolor de cabeza, estreñimiento.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Clonazepam",
        "uso": "Anticonvulsivante, ansiolítico.",
        "dosis": "0.5-2 mg dos o tres veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Somnolencia, dependencia, problemas de memoria.",
        "recomendaciones_alimenticias": "Evitar alcohol."
    },
    {
        "nombre": "Warfarina",
        "uso": "Anticoagulante oral.",
        "dosis": "Variable según INR objetivo, usualmente 2-10 mg diarios.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sangrado, hematomas, necrosis cutánea.",
        "recomendaciones_alimenticias": "Mantener constante ingesta de alimentos con vitamina K."
    },
    {
        "nombre": "Metoclopramida",
        "uso": "Antiemético, procinético gástrico.",
        "dosis": "10 mg tres veces al día antes de las comidas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Efectos extrapiramidales, somnolencia.",
        "recomendaciones_alimenticias": "Tomar 30 minutos antes de las comidas."
    },
    {
        "nombre": "Furosemida",
        "uso": "Diurético de asa para edema e hipertensión.",
        "dosis": "20-80 mg una o dos veces al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Desequilibrio electrolítico, deshidratación.",
        "recomendaciones_alimenticias": "Tomar por la mañana para evitar nicturia."
    },
    {
        "nombre": "Amlodipino",
        "uso": "Bloqueador de canales de calcio para hipertensión.",
        "dosis": "5-10 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Edema en extremidades, enrojecimiento facial.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Metronidazol",
        "uso": "Antibiótico y antiparasitario.",
        "dosis": "500 mg cada 8 horas por 7-10 días.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sabor metálico, náuseas, efecto antabus con alcohol.",
        "recomendaciones_alimenticias": "Evitar alcohol durante el tratamiento y 48h después."
    },
    {
        "nombre": "Hidroclorotiazida",
        "uso": "Diurético tiazídico para hipertensión.",
        "dosis": "12.5-25 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hipopotasemia, hiperuricemia, fotosensibilidad.",
        "recomendaciones_alimenticias": "Considerar alimentos ricos en potasio."
    },
    {
        "nombre": "Prednisona",
        "uso": "Corticosteroide antiinflamatorio e inmunosupresor.",
        "dosis": "Variable, típicamente 5-60 mg/día con reducción gradual.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Aumento de peso, osteoporosis, hiperglucemia.",
        "recomendaciones_alimenticias": "Tomar con alimentos, dieta baja en sodio y rica en potasio."
    },
    {
        "nombre": "Ácido Acetilsalicílico",
        "uso": "Antiinflamatorio, analgésico, antiagregante plaquetario.",
        "dosis": "100 mg diarios como antiagregante; 500-1000 mg cada 4-6h como analgésico.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Sangrado gastrointestinal, tinnitus en dosis altas.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir irritación gástrica."
    },
    {
        "nombre": "Gabapentina",
        "uso": "Antiepiléptico, dolor neuropático.",
        "dosis": "300-1200 mg tres veces al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Somnolencia, mareos, aumento de peso.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Bisoprolol",
        "uso": "Betabloqueante para hipertensión e insuficiencia cardíaca.",
        "dosis": "2.5-10 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Fatiga, bradicardia, broncoespasmo.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Claritromicina",
        "uso": "Antibiótico macrólido.",
        "dosis": "500 mg cada 12 horas por 7-14 días.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Alteración del gusto, malestar gastrointestinal.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Venlafaxina",
        "uso": "Antidepresivo IRSN para depresión y ansiedad.",
        "dosis": "75-225 mg una vez al día (liberación prolongada).",
        "categoria": "Cápsula",
        "efectos_secundarios": "Náuseas, hipertensión, sudoración.",
        "recomendaciones_alimenticias": "Tomar con alimentos."
    },
    {
        "nombre": "Insulina",
        "uso": "Hormona para control de glucemia en diabetes.",
        "dosis": "Variable según tipo y necesidades del paciente.",
        "categoria": "Inyectable",
        "efectos_secundarios": "Hipoglucemia, aumento de peso, lipodistrofia.",
        "recomendaciones_alimenticias": "Coordinar con ingesta de carbohidratos."
    },
    {
        "nombre": "Tamsulosina",
        "uso": "Bloqueador alfa para hiperplasia prostática benigna.",
        "dosis": "0.4 mg una vez al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Mareos, eyaculación retrógrada.",
        "recomendaciones_alimenticias": "Tomar después del desayuno."
    },
    {
        "nombre": "Sildenafilo",
        "uso": "Inhibidor de PDE5 para disfunción eréctil.",
        "dosis": "50 mg 1 hora antes de la actividad sexual.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolor de cabeza, enrojecimiento facial, congestión nasal.",
        "recomendaciones_alimenticias": "Evitar comidas grasas que reducen absorción."
    },
    {
        "nombre": "Pantoprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Similar a omeprazol pero menos interacciones.",
        "recomendaciones_alimenticias": "Tomar en ayunas."
    },
    {
        "nombre": "Pregabalina",
        "uso": "Antiepiléptico, dolor neuropático, ansiedad.",
        "dosis": "75-300 mg dos veces al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Mareos, somnolencia, aumento de peso.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Risperidona",
        "uso": "Antipsicótico para esquizofrenia y trastorno bipolar.",
        "dosis": "2-6 mg al día en una o dos tomas.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Aumento de peso, hiperprolactinemia, síndrome metabólico.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Montelukast",
        "uso": "Antileucotrieno para asma y rinitis alérgica.",
        "dosis": "10 mg una vez al día por la noche.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Dolor de cabeza, cambios de humor.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Escitalopram",
        "uso": "Antidepresivo ISRS para depresión y ansiedad.",
        "dosis": "10-20 mg una vez al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Náuseas, insomnio, disfunción sexual.",
        "recomendaciones_alimenticias": "Puede tomarse con o sin alimentos."
    },
    {
        "nombre": "Esomeprazol",
        "uso": "Inhibidor de la bomba de protones para reflujo y úlceras.",
        "dosis": "20-40 mg una vez al día.",
        "categoria": "Cápsula",
        "efectos_secundarios": "Dolor de cabeza, diarrea.",
        "recomendaciones_alimenticias": "Tomar en ayunas."
    },
    {
        "nombre": "Azatioprina",
        "uso": "Inmunosupresor para enfermedades autoinmunes y trasplantes.",
        "dosis": "1-3 mg/kg/día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Mielosupresión, hepatotoxicidad, aumento riesgo de infecciones.",
        "recomendaciones_alimenticias": "Tomar con alimentos para reducir náuseas."
    },
    {
        "nombre": "Espironolactona",
        "uso": "Diurético ahorrador de potasio, antagonista de aldosterona.",
        "dosis": "25-100 mg al día.",
        "categoria": "Pastilla",
        "efectos_secundarios": "Hiperpotasemia, ginecomastia en hombres.",
        "recomendaciones_alimenticias": "Evitar suplementos de potasio y sustitutos de sal."
    },
    {
        "nombre": "Amiodarona",
        "uso": "Antiarrítmico para arritmias ventriculares y auriculares.",
        "dosis": "200-400 mg al día tras dosis de carga.",
        "categoria": "Pastilla",
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
        categoria=med["categoria"],
        efectos_secundarios=med["efectos_secundarios"],
        recomendaciones_alimenticias=med["recomendaciones_alimenticias"]
    )

print("Se han añadido 40 medicamentos adicionales correctamente.")

# Cerrar la conexión cuando hayamos terminado
db.close_connection()