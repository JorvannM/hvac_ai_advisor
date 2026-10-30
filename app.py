import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

st.set_page_config(page_title="HVAC AI Advisor | Portfolio Edition", page_icon="⚡", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {
  --navy:#10243A; --navy2:#173A56; --teal:#087F8C; --mint:#8CE5D2;
  --paper:#F3F7FA; --ink:#172B3D; --muted:#6B7D8D; --line:#E2EAF0;
}
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#F5F8FB 0%,#EDF3F7 100%); color:var(--ink); }
.block-container { max-width:1500px; padding-top:1.4rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0C1D30 0%,#12354D 58%,#0E5660 100%); border-right:1px solid rgba(255,255,255,.08); }
[data-testid="stSidebar"] * { color:#EAF4F8; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:.55rem .65rem; border-radius:10px; margin:.12rem 0; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.09); }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.18); }
.brand-mark { display:flex; align-items:center; gap:12px; padding:.5rem 0 1rem; }
.brand-icon { display:flex; align-items:center; justify-content:center; width:45px; height:45px; border-radius:14px; background:linear-gradient(135deg,#8CE5D2,#21A6A5); color:#10243A!important; font-size:1.45rem; font-weight:900; box-shadow:0 8px 22px rgba(0,0,0,.18); }
.brand-title { font-family:'Manrope',sans-serif; font-size:1.08rem; line-height:1.2; font-weight:800; letter-spacing:-.03em; }
.brand-sub { font-size:.68rem; letter-spacing:.13em; color:#9FC8D4!important; margin-top:4px; }
.hero { position:relative; overflow:hidden; background:linear-gradient(118deg,#10243A 0%,#16445B 56%,#087F8C 100%); border-radius:24px; padding:32px 34px; color:white; margin:0 0 25px; box-shadow:0 18px 45px rgba(16,36,58,.15); }
.hero:after { content:''; position:absolute; right:-55px; top:-115px; width:330px; height:330px; border:1px solid rgba(255,255,255,.16); border-radius:50%; box-shadow:0 0 0 28px rgba(255,255,255,.035),0 0 0 58px rgba(255,255,255,.025); }
.hero h1 { color:white; font-family:'Manrope',sans-serif; font-size:clamp(2rem,4vw,3rem); letter-spacing:-.05em; line-height:1.08; margin:.45rem 0 .55rem; }
.hero p { color:#D8E9F0; font-size:1rem; max-width:760px; margin-bottom:0; }
.hero-kicker { color:#8CE5D2; letter-spacing:.16em; font-size:.72rem; font-weight:800; }
.section-label { color:#087F8C; font-size:.72rem; letter-spacing:.13em; font-weight:800; text-transform:uppercase; margin-bottom:.3rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif!important; letter-spacing:-.035em; color:#10243A; }
h2 { font-size:1.6rem!important; }
h3 { font-size:1.18rem!important; }
.kpi { background:linear-gradient(145deg,#FFFFFF 0%,#F9FBFD 100%); border:1px solid #E2EAF0; border-radius:18px; padding:18px 19px; min-height:116px; box-shadow:0 6px 18px rgba(19,48,71,.035); }
.label { color:#718294; font-size:.78rem; font-weight:600; letter-spacing:.02em; }
.value { font-family:'Manrope',sans-serif; font-size:clamp(1.25rem,2vw,1.7rem); line-height:1.4; font-weight:800; color:#10243A; margin-top:6px; }
.card { background:rgba(255,255,255,.88); border:1px solid #E2EAF0; border-radius:16px; padding:16px 18px; margin-bottom:11px; box-shadow:0 5px 16px rgba(19,48,71,.035); }
div[data-testid="stMetric"] { background:#fff; padding:16px 18px; border:1px solid var(--line); border-radius:16px; box-shadow:0 5px 18px rgba(16,36,58,.035); }
div[data-testid="stMetricLabel"] { color:#6B7D8D; }
div[data-testid="stMetricValue"] { font-family:'Manrope',sans-serif; color:#10243A; }
.stButton > button, .stDownloadButton > button, button[kind="primary"] { border-radius:11px; border:1px solid #D9E5EC; min-height:2.7rem; font-weight:700; transition:all .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#087F8C; color:#087F8C; transform:translateY(-1px); }
button[kind="primary"] { background:linear-gradient(100deg,#087F8C,#10A6A0); border:0; color:white; }
button[kind="primary"]:hover { background:linear-gradient(100deg,#066B76,#0C8B88); color:white; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #E2EAF0; border-radius:12px; overflow:hidden; }
[data-testid="stAlert"] { border-radius:13px; }
[data-testid="stExpander"] { border:1px solid #E2EAF0; border-radius:13px; background:rgba(255,255,255,.65); }
[data-baseweb="tab-list"] { gap:8px; }
[data-baseweb="tab"] { border-radius:10px 10px 0 0; }
input, textarea, [data-baseweb="select"] > div { border-radius:10px!important; }
.footer-note { text-align:center; color:#7B8D9C; font-size:.78rem; padding:1.1rem 0 .3rem; }
@media(max-width:700px) {
 .hero { padding:24px 22px; border-radius:18px; }
 .kpi { padding:13px; min-height:95px; }
 .value { font-size:1.2rem; }
}
</style>""", unsafe_allow_html=True)

defaults = {
 "nom":"Bâtiment tertiaire — Démonstrateur","site":"À renseigner","usage":"Bureaux","surface":2500,
 "annee":2005,"isolation":"Moyenne","chauffage":"Chaudière gaz","ventilation":"VMC simple flux",
 "donnees_connues":True,"elec_kwh":120000,"gaz_kwh":180000,"reseau_kwh":0,
 "elec_eur":30000.0,"gaz_eur":30000.0,"reseau_eur":0.0,"budget":100000,
 "facteur_elec":0.052,"facteur_gaz":0.227,"facteur_reseau":0.100,"source_facteurs":"Valeurs de démonstration"
}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v
if "parc_batiments" not in st.session_state:
    st.session_state.parc_batiments = []

def fmt(n): return f"{n:,.0f}".replace(","," ")
def eur(n): return f"{n:,.0f} €".replace(","," ")
def energie():
    return pd.DataFrame([
      {"Énergie":"Électricité","kWh/an":st.session_state.elec_kwh,"Dépense €/an":st.session_state.elec_eur,"Facteur kgCO₂e/kWh":st.session_state.facteur_elec},
      {"Énergie":"Gaz","kWh/an":st.session_state.gaz_kwh,"Dépense €/an":st.session_state.gaz_eur,"Facteur kgCO₂e/kWh":st.session_state.facteur_gaz},
      {"Énergie":"Réseau de chaleur","kWh/an":st.session_state.reseau_kwh,"Dépense €/an":st.session_state.reseau_eur,"Facteur kgCO₂e/kWh":st.session_state.facteur_reseau},
    ])
def totaux():
    d=energie()
    return d, float(d["kWh/an"].sum()), float(d["Dépense €/an"].sum()), float((d["kWh/an"]*d["Facteur kgCO₂e/kWh"]).sum())
def reference():
    return st.session_state.surface*{"Bonne":55,"Moyenne":100,"Faible":155}[st.session_state.isolation]
def scenarios():
    d,total,cost,_=totaux()
    base=total if st.session_state.donnees_connues else reference()
    cost_known = st.session_state.donnees_connues and total > 0 and cost > 0
    specs=[
      ("Référence",0,0,"Situation de référence"),
      ("Optimisation / régulation",.08,min(cost*.4,15000),"Horaires, consignes, régulation"),
      ("Amélioration de l'enveloppe",.18 if st.session_state.isolation!="Bonne" else .08,st.session_state.surface*(55 if st.session_state.isolation=="Faible" else 30),"Isolation et étanchéité à étudier"),
      ("Modernisation du chauffage",.20,st.session_state.surface*85,"Étude de remplacement du générateur"),
      ("Plan combiné",.30 if st.session_state.isolation!="Bonne" else .23,st.session_state.surface*(110 if st.session_state.isolation=="Faible" else 80),"Combinaison d'actions"),
    ]
    rows=[]
    for name,gain,invest,levier in specs:
      saved_kwh=base*gain
      saved_eur=cost*gain if cost_known else None
      payback=invest/saved_eur if saved_eur and saved_eur>0 and invest>0 else (0 if invest==0 else None)
      rows.append({
        "Scénario":name,
        "Consommation après scénario (kWh/an)":round(base-saved_kwh),
        "Gain hypothétique (%)":round(gain*100,1),
        "Énergie évitée (kWh/an)":round(saved_kwh),
        "Économie annuelle indicative (€)":round(saved_eur) if saved_eur is not None else None,
        "Investissement indicatif (€)":round(invest),
        "Temps de retour simple (ans)":round(payback,1) if payback is not None else None,
        "Budget":"Oui" if invest<=st.session_state.budget else "À arbitrer",
        "Levier":levier
      })
    return pd.DataFrame(rows),base
def recos():
    r=[]
    if st.session_state.isolation=="Faible": r.append(("Enveloppe","Examiner isolation, ponts thermiques et étanchéité avant de redimensionner les équipements."))
    r.extend([
      ("Factures","Vérifier une période complète de 12 mois, les unités et les éventuelles estimations de facturation."),
      ("Chauffage","Comparer réglage et remplacement selon températures de départ, émetteurs, horaires et besoins réels."),
      ("Ventilation","Contrôler les débits, horaires, filtres, entretien et récupération de chaleur selon l'usage.")
    ])
    return r


def creer_rapport_pdf():
    """Construit un rapport PDF synthétique à partir des données de session."""
    data, total_kwh, total_cost, _ = totaux()
    tab, base = scenarios()
    data = data.copy()
    data["Émissions estimées (kgCO₂e/an)"] = data["kWh/an"] * data["Facteur kgCO₂e/kWh"]
    total_co2 = float(data["Émissions estimées (kgCO₂e/an)"].sum())

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=1.6*cm, leftMargin=1.6*cm,
        topMargin=1.6*cm, bottomMargin=1.6*cm,
        title="HVAC AI Advisor - Rapport de pré-analyse - Noël Moukoko"
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=24, leading=29, textColor=colors.HexColor("#10243A"),
                              alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="SubTitleCustom", parent=styles["Normal"], fontSize=10,
                              leading=15, textColor=colors.HexColor("#526579"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="SectionCustom", parent=styles["Heading2"], fontSize=13,
                              leading=17, textColor=colors.HexColor("#087F8C"), spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="SmallCustom", parent=styles["Normal"], fontSize=8,
                              leading=11, textColor=colors.HexColor("#526579")))
    story = []
    story += [Spacer(1, 2.0*cm), Paragraph("HVAC AI ADVISOR", styles["CoverTitle"]),
              Paragraph("Rapport de pré-analyse énergétique et CVC", styles["SubTitleCustom"]),
              Spacer(1, 0.6*cm), Paragraph(escape(str(st.session_state.nom)), styles["Heading1"]),
              Paragraph(f"Site : {escape(str(st.session_state.site))} · Usage : {escape(str(st.session_state.usage))}", styles["Normal"]),
              Paragraph(f"Rapport généré le {date.today().strftime('%d/%m/%Y')}", styles["SmallCustom"]),
              Paragraph("Conçu et développé par Noël Moukoko", styles["SmallCustom"]),
              Spacer(1, 1.0*cm)]

    def add_section(title):
        story.append(Paragraph(escape(title), styles["SectionCustom"]))

    def add_table(rows, widths=None):
        tbl = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#10243A")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
            ("FONTSIZE", (0,0), (-1,-1), 7.5),
            ("LEADING", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#D8E1EA")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F6FA")]),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(tbl)

    add_section("1. Synthèse du bâtiment")
    building_rows = [
        ["Indicateur", "Valeur"],
        ["Surface chauffée", f"{fmt(st.session_state.surface)} m²"],
        ["Année de construction", str(st.session_state.annee)],
        ["Isolation estimée", str(st.session_state.isolation)],
        ["Chauffage", str(st.session_state.chauffage)],
        ["Ventilation", str(st.session_state.ventilation)],
        ["Budget déclaré", eur(st.session_state.budget)],
    ]
    add_table(building_rows, [6.5*cm, 10.5*cm])

    add_section("2. Indicateurs énergétiques")
    if st.session_state.donnees_connues:
        intensity = total_kwh / st.session_state.surface if st.session_state.surface else 0
        energy_rows = [["Énergie", "Consommation (kWh/an)", "Dépense (€/an)"]]
        for _, row in data.iterrows():
            energy_rows.append([str(row["Énergie"]), fmt(float(row["kWh/an"])), eur(float(row["Dépense €/an"]))])
        energy_rows.append(["TOTAL", fmt(total_kwh), eur(total_cost)])
        add_table(energy_rows, [5.0*cm, 6.0*cm, 6.0*cm])
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"Intensité énergétique : {intensity:.1f} kWh/m²/an · Dépense : {total_cost/st.session_state.surface:.1f} €/m²/an", styles["Normal"]))
        story.append(Paragraph(f"Émissions estimées des vecteurs renseignés : {total_co2/1000:.2f} tCO₂e/an", styles["Normal"]))
    else:
        story.append(Paragraph("Les consommations réelles ne sont pas renseignées. Les indicateurs de consommation et les économies financières ne sont donc pas considérés comme mesurés.", styles["Normal"]))

    add_section("3. Scénarios de rénovation")
    scenario_rows = [["Scénario", "Gain hypothétique", "Investissement indicatif", "Économie/an", "Retour simple"]]
    for _, row in tab.iterrows():
        gain = f"{row['Gain hypothétique (%)']}%"
        invest = eur(float(row["Investissement indicatif (€)"]))
        saving = "Non calculée" if pd.isna(row["Économie annuelle indicative (€)"]) else eur(float(row["Économie annuelle indicative (€)"]))
        payback = "Non calculé" if pd.isna(row["Temps de retour simple (ans)"]) else f"{float(row['Temps de retour simple (ans)']):.1f} ans"
        scenario_rows.append([str(row["Scénario"]), gain, invest, saving, payback])
    add_table(scenario_rows, [4.0*cm, 2.3*cm, 3.5*cm, 3.0*cm, 3.2*cm])

    add_section("4. Recommandations à étudier")
    for title, description in recos():
        story.append(Paragraph(f"<b>{escape(title)} :</b> {escape(description)}", styles["Normal"]))
        story.append(Spacer(1, 0.12*cm))

    add_section("5. Hypothèses, facteurs carbone et limites")
    limitations = [
        f"Statut des facteurs carbone : {st.session_state.source_facteurs if 'source_facteurs' in st.session_state else 'Valeurs de démonstration'}.",
        f"Facteurs utilisés (kgCO₂e/kWh) : électricité {st.session_state.facteur_elec}, gaz {st.session_state.facteur_gaz}, réseau de chaleur {st.session_state.facteur_reseau}.",
        "Les gains énergétiques, économies et coûts d'investissement sont des hypothèses de démonstration, pas des performances garanties.",
        "Le temps de retour est simple : il ne tient pas compte de l'actualisation, de la maintenance, des remplacements, de l'évolution des prix ni des interactions entre actions.",
        "Les émissions calculées couvrent uniquement les vecteurs énergétiques renseignés et les facteurs saisis ; elles ne constituent pas un bilan carbone complet.",
        "Ce document est une pré-analyse et ne remplace pas un audit réglementaire, une étude thermique, un devis ou une validation par un professionnel.",
    ]
    for item in limitations:
        story.append(Paragraph("• " + escape(item), styles["SmallCustom"]))
        story.append(Spacer(1, 0.08*cm))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D8E1EA"))
        canvas.line(1.6*cm, 1.25*cm, A4[0]-1.6*cm, 1.25*cm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#526579"))
        canvas.drawString(1.6*cm, 0.85*cm, "HVAC AI Advisor · Noël Moukoko")
        canvas.drawRightString(A4[0]-1.6*cm, 0.85*cm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    return buffer.getvalue()

with st.sidebar:
    st.markdown("""
    <div class="brand-mark">
      <div class="brand-icon">H+</div>
      <div><div class="brand-title">HVAC AI Advisor</div><div class="brand-sub">ENERGY INTELLIGENCE</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Une plateforme de pré-analyse énergétique pour les bâtiments.")
    page=st.radio("NAVIGATION",["Tableau de bord","Parc immobilier","Audit énergétique","Scénarios de rénovation","Comparateur CVC","Analyse carbone","Rapport"])
    st.markdown("---")
    st.markdown("**Conçu & développé par**")
    st.markdown("### Noël Moukoko")
    st.caption("Portfolio project · Version 1.0")
st.markdown(f"""<div class="hero"><div class="hero-kicker">ENERGY PERFORMANCE&nbsp;&nbsp;•&nbsp;&nbsp;HVAC&nbsp;&nbsp;•&nbsp;&nbsp;DECARBONIZATION</div><h1>HVAC AI Advisor</h1><p>Comprendre les consommations, comparer les scénarios de rénovation et piloter la performance énergétique de vos bâtiments.</p></div>""",unsafe_allow_html=True)

if page=="Tableau de bord":
    d,total,cost,co2=totaux()
    st.markdown('<div class="section-label">VUE D’ENSEMBLE · PERFORMANCE DU SITE</div>', unsafe_allow_html=True)
    st.markdown(f"### {st.session_state.nom}")
    st.caption(f"{st.session_state.site} · {st.session_state.usage} · Mis à jour le {date.today().strftime('%d/%m/%Y')}")
    if not st.session_state.donnees_connues: st.warning("Consommations réelles non confirmées : les scénarios utilisent un proxy simplifié.")
    vals=[("Surface",f"{fmt(st.session_state.surface)} m²"),("Consommation",f"{fmt(total)} kWh/an" if st.session_state.donnees_connues else "À renseigner"),("Intensité",f"{total/st.session_state.surface:.0f} kWh/m²/an" if st.session_state.donnees_connues else "—"),("Dépense",eur(cost) if st.session_state.donnees_connues else "—")]
    cols=st.columns(4)
    for c,(label,val) in zip(cols,vals): c.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{val}</div></div>',unsafe_allow_html=True)
    left,right=st.columns([1.1,.9])
    with left:
        st.markdown("#### Répartition des consommations")
        if st.session_state.donnees_connues and total>0:
            st.bar_chart(d.set_index("Énergie")["kWh/an"])
            st.dataframe(d[["Énergie","kWh/an","Dépense €/an"]],hide_index=True,use_container_width=True)
        else: st.info("Complète les données de l'audit pour visualiser la répartition.")
    with right:
        st.markdown("#### Points d'attention")
        for titre,desc in recos(): st.markdown(f'<div class="card"><strong>{titre}</strong><br>{desc}</div>',unsafe_allow_html=True)

elif page=="Parc immobilier":
    st.markdown("### Gestion multi-bâtiments")
    st.write("Enregistre des instantanés de bâtiments pour comparer leurs consommations et repérer les sites prioritaires.")
    st.info("Les données sont conservées dans la session de l'application. Elles ne sont pas encore enregistrées dans une base de données permanente : télécharge le CSV pour garder une copie.")
    d,total,cost,co2=totaux()
    st.markdown("#### Ajouter le bâtiment actuellement ouvert au parc")
    st.write(f"**{st.session_state.nom}** · {st.session_state.site} · {fmt(st.session_state.surface)} m²")
    if st.button("＋ Enregistrer ce bâtiment dans le parc", type="primary"):
        record = {
            "Bâtiment": str(st.session_state.nom),
            "Site": str(st.session_state.site),
            "Usage": str(st.session_state.usage),
            "Surface (m²)": float(st.session_state.surface),
            "Consommation connue": "Oui" if st.session_state.donnees_connues else "Non",
            "Consommation (kWh/an)": round(total) if st.session_state.donnees_connues else None,
            "Intensité (kWh/m²/an)": round(total/st.session_state.surface, 1) if st.session_state.donnees_connues and st.session_state.surface else None,
            "Dépense (€/an)": round(cost) if st.session_state.donnees_connues else None,
            "Émissions estimées (tCO₂e/an)": round(co2/1000, 2) if st.session_state.donnees_connues else None,
            "Budget (€)": float(st.session_state.budget),
            "Date de capture": date.today().isoformat()
        }
        st.session_state.parc_batiments.append(record)
        st.success("Bâtiment enregistré dans le parc pour cette session.")
    st.markdown("#### Parc enregistré")
    if st.session_state.parc_batiments:
        portfolio_df = pd.DataFrame(st.session_state.parc_batiments)
        k1,k2,k3=st.columns(3)
        k1.metric("Bâtiments enregistrés",len(portfolio_df))
        k2.metric("Surface totale",f"{fmt(portfolio_df['Surface (m²)'].sum())} m²")
        known = portfolio_df[portfolio_df["Consommation connue"]=="Oui"]
        k3.metric("Consommation cumulée connue",f"{fmt(known['Consommation (kWh/an)'].fillna(0).sum())} kWh/an")
        st.dataframe(portfolio_df,hide_index=True,use_container_width=True)
        if not known.empty:
            st.markdown("#### Intensité énergétique par bâtiment")
            st.bar_chart(known.set_index("Bâtiment")[["Intensité (kWh/m²/an)"]])
            st.markdown("#### Priorisation indicative")
            ranked=known.sort_values("Intensité (kWh/m²/an)",ascending=False)
            st.dataframe(ranked[["Bâtiment","Site","Surface (m²)","Intensité (kWh/m²/an)","Dépense (€/an)"]],hide_index=True,use_container_width=True)
            st.caption("Un classement par intensité aide à repérer les sites à examiner, mais ne suffit pas à conclure qu'un bâtiment est moins performant : comparer des usages, climats, horaires et niveaux de service similaires.")
        st.download_button("Télécharger le parc (CSV)",portfolio_df.to_csv(index=False).encode("utf-8-sig"),"parc_immobilier_hvac_v09.csv","text/csv")
        if st.button("Vider le parc de cette session"):
            st.session_state.parc_batiments=[]
            st.rerun()
    else:
        st.info("Le parc est vide. Enregistre le bâtiment actuel pour commencer.")
    st.markdown("#### Conseils pour comparer correctement")
    st.markdown("- Compare des périodes de consommation de 12 mois identiques ou comparables.\n- Vérifie que les surfaces et les usages sont cohérents.\n- Distingue les consommations mesurées des estimations.\n- Ne traite pas le classement automatique comme un audit énergétique.")

elif page=="Audit énergétique":
    st.markdown("### Données du bâtiment")
    st.write("Saisis les consommations à partir des factures, en kWh, sur la même période de 12 mois.")
    with st.form("audit"):
        a,b=st.columns(2)
        with a:
            nom=st.text_input("Nom du bâtiment",st.session_state.nom)
            site=st.text_input("Ville / site",st.session_state.site)
            usage=st.selectbox("Usage",["Bureaux","Enseignement","Commerce","Hôtel","Industrie","Logements collectifs","Autre"],index=["Bureaux","Enseignement","Commerce","Hôtel","Industrie","Logements collectifs","Autre"].index(st.session_state.usage))
            surface=st.number_input("Surface chauffée (m²)",1,1000000,int(st.session_state.surface),step=100)
            annee=st.number_input("Année de construction",1800,date.today().year,int(st.session_state.annee))
            isolation=st.selectbox("Isolation estimée",["Bonne","Moyenne","Faible"],index=["Bonne","Moyenne","Faible"].index(st.session_state.isolation))
            budget=st.number_input("Budget d'investissement (€)",0,1000000000,int(st.session_state.budget),step=5000)
        with b:
            chauffage=st.selectbox("Chauffage principal",["Chaudière gaz","Chauffage électrique","Pompe à chaleur","Réseau de chaleur","Chaudière biomasse","Autre / inconnu"],index=["Chaudière gaz","Chauffage électrique","Pompe à chaleur","Réseau de chaleur","Chaudière biomasse","Autre / inconnu"].index(st.session_state.chauffage))
            ventilation=st.selectbox("Ventilation",["VMC simple flux","VMC double flux","CTA avec récupération","Aucune / naturelle","Autre / inconnu"],index=["VMC simple flux","VMC double flux","CTA avec récupération","Aucune / naturelle","Autre / inconnu"].index(st.session_state.ventilation))
            connues=st.checkbox("Consommations annuelles connues",st.session_state.donnees_connues)
            st.markdown("**Consommations et dépenses par énergie**")
            elec=st.number_input("Électricité (kWh/an)",0,100000000000,int(st.session_state.elec_kwh),step=1000,disabled=not connues)
            gaz=st.number_input("Gaz (kWh/an)",0,100000000000,int(st.session_state.gaz_kwh),step=1000,disabled=not connues)
            reseau=st.number_input("Réseau de chaleur (kWh/an)",0,100000000000,int(st.session_state.reseau_kwh),step=1000,disabled=not connues)
            elece=st.number_input("Dépense électricité (€)",0.0,1000000000.0,float(st.session_state.elec_eur),step=500.0,disabled=not connues)
            gaze=st.number_input("Dépense gaz (€)",0.0,1000000000.0,float(st.session_state.gaz_eur),step=500.0,disabled=not connues)
            reseau_e=st.number_input("Dépense réseau de chaleur (€)",0.0,1000000000.0,float(st.session_state.reseau_eur),step=500.0,disabled=not connues)
        save=st.form_submit_button("Enregistrer les données",type="primary",use_container_width=True)
    if save:
        for k,v in {"nom":nom,"site":site,"usage":usage,"surface":surface,"annee":annee,"isolation":isolation,"budget":budget,"chauffage":chauffage,"ventilation":ventilation,"donnees_connues":connues,"elec_kwh":elec,"gaz_kwh":gaz,"reseau_kwh":reseau,"elec_eur":elece,"gaz_eur":gaze,"reseau_eur":reseau_e}.items(): st.session_state[k]=v
        st.success("Données enregistrées dans cette session.")
    d,total,cost,co2=totaux()
    st.markdown("### Indicateurs calculés")
    c1,c2,c3=st.columns(3)
    c1.metric("Consommation totale",f"{fmt(total)} kWh/an" if st.session_state.donnees_connues else "—")
    c2.metric("Coût moyen pondéré",f"{cost/total:.3f} €/kWh" if st.session_state.donnees_connues and total>0 else "—")
    c3.metric("Dépense par surface",f"{cost/st.session_state.surface:.1f} €/m²/an" if st.session_state.donnees_connues else "—")
    st.caption("Ces indicateurs dépendent du périmètre des factures, des abonnements, des taxes et de la cohérence des unités.")

elif page=="Scénarios de rénovation":
    st.markdown("### Simulateur technico-économique")
    st.write("Compare des trajectoires de rénovation selon les hypothèses de gain, les coûts estimatifs et le budget disponible.")
    if st.session_state.donnees_connues:
        st.info("La référence utilise la somme des consommations saisies. Les gains sont des hypothèses de démonstration, pas des économies garanties.")
    else:
        st.warning("Sans consommations réelles, la référence est un proxy surface/isolation. Les économies financières et le temps de retour ne sont pas calculés.")
    tab,base=scenarios()
    c1,c2,c3=st.columns(3)
    c1.metric("Référence énergétique",f"{fmt(base)} kWh/an")
    c2.metric("Budget disponible",eur(st.session_state.budget))
    affordable=int((tab["Budget"]=="Oui").sum())
    c3.metric("Scénarios dans le budget",f"{affordable}/{len(tab)}")
    st.markdown("#### Comparaison des consommations")
    st.bar_chart(tab.set_index("Scénario")[["Consommation après scénario (kWh/an)"]])
    st.markdown("#### Comparaison économique")
    economic_cols=["Scénario","Investissement indicatif (€)","Économie annuelle indicative (€)","Temps de retour simple (ans)","Budget"]
    st.dataframe(tab[economic_cols],hide_index=True,use_container_width=True)
    st.markdown("#### Détail complet des scénarios")
    st.dataframe(tab,hide_index=True,use_container_width=True)
    st.caption("Le temps de retour simple = investissement estimatif ÷ économie annuelle estimative. Il ne tient pas compte de l'actualisation, de la maintenance, du renouvellement, de la hausse des prix ni des interactions entre actions. Il est affiché uniquement si les données de coût et de consommation sont disponibles.")
    st.markdown("#### Analyse de sensibilité")
    st.write("Teste comment les résultats changent si les gains sont plus faibles ou plus élevés. Cela montre l'influence des hypothèses, sans les valider.")
    gain_scale=st.slider("Facteur appliqué aux gains hypothétiques",min_value=0.50,max_value=1.50,value=1.00,step=0.05,format="%.2f×")
    sens=tab.copy()
    # Tolérer les variantes de libellé de colonne entre les versions du tableau.
    if "Gain hypothétique (%)" in sens.columns:
        gain_col = "Gain hypothétique (%)"
    elif "Gain hypothétique" in sens.columns:
        gain_col = "Gain hypothétique"
    else:
        st.error("La colonne de gain est absente du tableau des scénarios. Recharge la page ou vérifie la version du fichier app.py.")
        gain_col = None
    if gain_col is not None:
        sens["Gain ajusté (%)"]=(sens[gain_col].astype(float)*gain_scale).clip(upper=100)
        sens["Énergie évitée ajustée (kWh/an)"]=(base*sens["Gain ajusté (%)"]/100).round().astype(int)
        sens["Consommation ajustée (kWh/an)"]=(base-sens["Énergie évitée ajustée (kWh/an)"]).round().astype(int)
        st.dataframe(sens[["Scénario","Gain ajusté (%)","Énergie évitée ajustée (kWh/an)","Consommation ajustée (kWh/an)"]],hide_index=True,use_container_width=True)
    st.caption("Les gains et investissements sont des hypothèses fictives de démonstration. Avant décision : audit, devis, étude de faisabilité et vérification des performances.")
    st.download_button("Exporter les scénarios (CSV)",tab.to_csv(index=False).encode("utf-8-sig"),"scenarios_renovation_hvac_v06.csv","text/csv")

elif page=="Comparateur CVC":
    st.markdown("### Comparateur de solutions CVC")
    data=pd.DataFrame([
      ["PAC air/eau","Émetteurs, température de départ, puissance électrique","Électrification et rendement saisonnier potentiel","Froid, bruit, appoint, émetteurs"],
      ["PAC géothermique","Terrain/sondes, étude de sol, autorisations","Source thermique stable","Investissement et travaux"],
      ["Chaudière biomasse","Stockage et approvisionnement durable","Alternative à certains combustibles fossiles","Logistique, particules, maintenance"],
      ["VMC double flux","Réseaux et équilibrage des débits","Récupération de chaleur","Filtres, bruit, entretien"],
      ["CTA avec récupération","Traitement d'air centralisé","Récupération de chaleur et pilotage","Coût, espace, régulation"],
      ["Optimisation de l'existant","Système exploitable et réglages perfectibles","Actions parfois rapides et moins capitalistiques","Potentiel à mesurer avant/après"],
    ],columns=["Solution","Conditions à vérifier","Atouts possibles","Points de vigilance"])
    st.dataframe(data,hide_index=True,use_container_width=True)
    objectif=st.selectbox("Objectif prioritaire",["Efficacité énergétique","Décarbonation","Investissement limité","Qualité d'air"])
    if st.button("Proposer une piste à étudier",type="primary"):
        conseils={"Efficacité énergétique":"Mesurer les consommations, vérifier horaires et consignes, puis comparer les solutions sur des données observées.","Décarbonation":"Comparer optimisation et électrification ou énergie bas-carbone avec consommations séparées et facteurs adaptés.","Investissement limité":"Examiner d'abord régulation, équilibrage, horaires et maintenance.","Qualité d'air":"Vérifier les débits d'air neuf, l'occupation et l'entretien avant de choisir une solution."}
        st.success(conseils[objectif])

elif page=="Analyse carbone":
    st.markdown("### Analyse carbone opérationnelle")
    st.write("Estimation exploratoire à partir des consommations déclarées par vecteur énergétique.")
    st.warning("Les facteurs préremplis sont des valeurs de démonstration, pas des facteurs officiels garantis. Vérifie la source, l'année, le périmètre et les unités avant tout usage professionnel.")
    sources=["Valeurs de démonstration","Facteurs vérifiés manuellement","Facteurs issus d'une source officielle"]
    source=st.selectbox("Statut des facteurs d'émission",sources,index=sources.index(st.session_state.source_facteurs))
    if source=="Facteurs issus d'une source officielle":
        st.info("Pour la France, consulte la Base Empreinte de l'ADEME et sélectionne le facteur correspondant précisément à l'énergie, au périmètre et à la période. L'application ne télécharge pas automatiquement les facteurs.")
        st.markdown("Source : [Base Empreinte de l’ADEME](https://base-empreinte.ademe.fr/)")
    elif source=="Facteurs vérifiés manuellement":
        st.info("Renseigne ci-dessous les facteurs vérifiés et documente leur référence.")
    else:
        st.info("Ce mode sert à tester l'application. Ne présente pas ces résultats comme un bilan carbone professionnel.")
    st.session_state.source_facteurs=source
    a,b,c=st.columns(3)
    with a: fe=st.number_input("Électricité (kgCO₂e/kWh)",0.0,5.0,float(st.session_state.facteur_elec),step=.001,format="%.3f")
    with b: fg=st.number_input("Gaz (kgCO₂e/kWh)",0.0,5.0,float(st.session_state.facteur_gaz),step=.001,format="%.3f")
    with c: fr=st.number_input("Réseau de chaleur (kgCO₂e/kWh)",0.0,5.0,float(st.session_state.facteur_reseau),step=.001,format="%.3f")
    ref=st.text_input("Référence / année / périmètre des facteurs","À compléter")
    st.session_state.facteur_elec=fe
    st.session_state.facteur_gaz=fg
    st.session_state.facteur_reseau=fr
    d,total,cost,co2=totaux()
    if not st.session_state.donnees_connues:
        st.info("Renseigne les consommations réelles dans Audit énergétique.")
    else:
        d["Émissions estimées (kgCO₂e/an)"]=d["kWh/an"]*d["Facteur kgCO₂e/kWh"]
        total_co2=float(d["Émissions estimées (kgCO₂e/an)"].sum())
        c1,c2,c3=st.columns(3)
        c1.metric("Électricité",f"{d.iloc[0]['Émissions estimées (kgCO₂e/an)']/1000:.2f} tCO₂e/an")
        c2.metric("Gaz",f"{d.iloc[1]['Émissions estimées (kgCO₂e/an)']/1000:.2f} tCO₂e/an")
        c3.metric("Total des vecteurs saisis",f"{total_co2/1000:.2f} tCO₂e/an")
        st.bar_chart(d.set_index("Énergie")["Émissions estimées (kgCO₂e/an)"])
        st.dataframe(d,hide_index=True,use_container_width=True)
        carbon_export=d.copy()
        carbon_export["Statut facteurs"]=source
        carbon_export["Référence facteurs"]=ref
        st.download_button("Exporter l'analyse carbone (CSV)",carbon_export.to_csv(index=False).encode("utf-8-sig"),"analyse_carbone_hvac_v07.csv","text/csv")
    st.caption("Périmètre limité aux trois vecteurs saisis. Les émissions amont, fluides frigorigènes, déplacements, équipements et travaux ne sont pas automatiquement inclus.")

elif page=="Rapport":
    st.markdown("### Rapport professionnel de pré-analyse")
    st.write("Prévisualise les indicateurs et exporte un PDF partageable pour ton portfolio ou une revue de projet.")
    d,total,cost,co2=totaux()
    tab,base=scenarios()
    c1,c2,c3=st.columns(3)
    c1.metric("Surface",f"{fmt(st.session_state.surface)} m²")
    c2.metric("Consommation",f"{fmt(total)} kWh/an" if st.session_state.donnees_connues else "Non renseignée")
    c3.metric("Budget déclaré",eur(st.session_state.budget))
    st.markdown("#### Synthèse des scénarios")
    st.dataframe(tab[["Scénario","Gain hypothétique (%)","Investissement indicatif (€)","Économie annuelle indicative (€)","Temps de retour simple (ans)","Budget"]],hide_index=True,use_container_width=True)
    st.info("Le PDF indique les hypothèses et limites du démonstrateur. Vérifie les données et facteurs avant de partager les résultats comme une analyse métier.")
    try:
        pdf_bytes=creer_rapport_pdf()
        st.download_button("📄 Télécharger le rapport PDF",data=pdf_bytes,file_name="rapport_hvac_ai_advisor.pdf",mime="application/pdf",type="primary",use_container_width=True)
    except Exception as e:
        st.error("La génération du PDF a échoué. Vérifie que ReportLab est installé, puis consulte le message ci-dessous.")
        st.code(str(e))
    report_txt=[
      "HVAC AI ADVISOR — RAPPORT DE PRÉ-ANALYSE",
      "Conçu et développé par Noël Moukoko",
      f"Date : {date.today().strftime('%d/%m/%Y')}",
      f"Bâtiment : {st.session_state.nom}", f"Site : {st.session_state.site}",
      f"Usage : {st.session_state.usage}", f"Surface : {fmt(st.session_state.surface)} m²",
      "", "CONSOMMATIONS", d.to_string(index=False),
      f"Total : {fmt(total)} kWh/an" if st.session_state.donnees_connues else "Consommations réelles non renseignées",
      "", "SCÉNARIOS", tab.to_string(index=False),
      "", "LIMITES : outil de pré-analyse, gains et coûts illustratifs, facteurs carbone à vérifier."
    ]
    with st.expander("Voir l'aperçu texte"):
        st.text_area("Rapport", "\n".join(report_txt), height=300)
    col_a,col_b=st.columns(2)
    with col_a:
        st.download_button("Télécharger aussi le rapport texte", "\n".join(report_txt).encode("utf-8"), "rapport_hvac_ai_advisor.txt", "text/plain")
    with col_b:
        st.download_button("Exporter les scénarios CSV",tab.to_csv(index=False).encode("utf-8-sig"),"scenarios_renovation_hvac_v09.csv","text/csv")

st.markdown("---")
st.markdown('<div class="footer-note">HVAC AI Advisor · Conçu et développé par <strong>Noël Moukoko</strong> · Démonstrateur de portfolio — valider les hypothèses avant toute décision technique ou financière.</div>', unsafe_allow_html=True)
